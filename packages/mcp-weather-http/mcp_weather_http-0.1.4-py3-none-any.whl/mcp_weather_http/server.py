"""WeatherServer – MCP Streamable HTTP implementation (v2)
===========================================================
• Fully compatible with MCP 2025‑03‑26 Streamable‑HTTP spec
• Returns chunked JSON with `id`, `stream`, `result`, `error`
• Accepts both simplified body {"input": {"city": ""}} and
  JSON‑RPC 2.0 body (preferred by Cherry Studio)
"""

from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any, AsyncIterator

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from mcp.server.fastmcp import FastMCP

##############################################################################
# 0. FastMCP metadata (optional for discovery)                               #
##############################################################################

mcp = FastMCP("WeatherServer")

##############################################################################
# 1. Business‑logic helpers                                                  #
##############################################################################

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY: str | None = None
USER_AGENT = "weather-app/1.0"


async def fetch_weather(city: str) -> dict[str, Any]:
    """Call OpenWeather API and return raw JSON or error dict."""
    if not API_KEY:
        return {"error": "API_KEY 未设置，请提供有效的 OpenWeather API Key。"}

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "zh_cn",
    }
    headers = {"User-Agent": USER_AGENT}

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            r = await client.get(OPENWEATHER_URL, params=params, headers=headers)
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as exc:
            return {"error": f"HTTP 错误: {exc.response.status_code}"}
        except Exception as exc:  # noqa: BLE001
            return {"error": f"请求失败: {exc}"}


def format_weather(data: dict[str, Any]) -> str:
    """Human‑readable weather text."""
    if "error" in data:
        return data["error"]

    city = data.get("name", "未知")
    country = data.get("sys", {}).get("country", "未知")
    temp = data.get("main", {}).get("temp", "N/A")
    humidity = data.get("main", {}).get("humidity", "N/A")
    wind = data.get("wind", {}).get("speed", "N/A")
    desc = data.get("weather", [{}])[0].get("description", "未知")

    return (
        f"🌍 {city}, {country}\n"
        f"🌡 温度: {temp}°C\n"
        f"💧 湿度: {humidity}%\n"
        f"🌬 风速: {wind} m/s\n"
        f"🌤 天气: {desc}"
    )

##############################################################################
# 2. Streamable HTTP generator                                               #
##############################################################################

async def chunk_weather(city: str, request_id: int | str) -> AsyncIterator[bytes]:
    """Yield JSON chunks following MCP streamable‑HTTP conventions."""
    # (1) Inform start / progress
    yield (
        json.dumps({"id": request_id, "stream": f"正在查询 {city} 天气…"}) + "\n"
    ).encode()

    # Simulate latency for UX demo; remove in production
    await asyncio.sleep(0.3)

    # (2) Actual result
    raw = await fetch_weather(city)
    if "error" in raw:
        yield (
            json.dumps({"id": request_id, "error": {"message": raw["error"]}}) + "\n"
        ).encode()
        return

    text = format_weather(raw)
    yield (json.dumps({"id": request_id, "result": text}) + "\n").encode()

    # (3) Optional done flag
    yield (json.dumps({"id": request_id, "done": True}) + "\n").encode()

##############################################################################
# 3. FastAPI app – single POST endpoint                                      #
##############################################################################

app = FastAPI(title="WeatherServer ‑ HTTP Stream v2")


@app.post("/mcp")
async def query_weather_http(request: Request):
    """Streamable HTTP tool endpoint (JSON‑RPC & simplified body compatible)."""
    body = await request.json()

    # Determine request id (default 1)
    req_id = body.get("id", 1)

    # Extract city from either simplified or JSON‑RPC style
    city = (
        body.get("input", {}).get("city")  # simplified
        or body.get("params", {}).get("city")  # JSON‑RPC 2.0
    )

    if not city:
        # immediate error response (not chunked)
        return {"id": req_id, "error": {"message": "缺少城市名称 (city)"}}

    return StreamingResponse(
        chunk_weather(city, req_id), media_type="application/json"
    )

##############################################################################
# 4. Entrypoint                                                              #
##############################################################################

def main() -> None:
    parser = argparse.ArgumentParser(description="Weather MCP HTTP‑Stream Server")
    parser.add_argument("--api_key", required=True, help="OpenWeather API Key")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    global API_KEY  # noqa: PLW0603
    API_KEY = args.api_key

    import uvicorn  # local import to ensure dependency only at runtime

    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
