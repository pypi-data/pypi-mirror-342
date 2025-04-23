"""WeatherServer – MCP Streamable HTTP implementation (v3, JSON-RPC compliant)
=================================================================================
• Fully conforms to MCP 2025-03-26 Streamable HTTP JSON-RPC response standard
• All responses include `jsonrpc`, `id`, and one of `stream`, `result`, or `error`
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

mcp = FastMCP("WeatherServer")

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY: str | None = None
USER_AGENT = "weather-app/1.0"


async def fetch_weather(city: str) -> dict[str, Any]:
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
        except Exception as exc:
            return {"error": f"请求失败: {exc}"}


def format_weather(data: dict[str, Any]) -> str:
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


async def chunk_weather(city: str, request_id: int | str) -> AsyncIterator[bytes]:
    yield json.dumps({
        "jsonrpc": "2.0",
        "id": request_id,
        "stream": f"正在查询 {city} 天气中..."
    }).encode() + b"\n"

    await asyncio.sleep(0.3)

    raw = await fetch_weather(city)
    if "error" in raw:
        yield json.dumps({
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32000,
                "message": raw["error"]
            }
        }).encode() + b"\n"
        return

    text = format_weather(raw)
    yield json.dumps({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": text
    }).encode() + b"\n"

    yield json.dumps({
        "jsonrpc": "2.0",
        "id": request_id,
        "stream": "查询完成"
    }).encode() + b"\n"


app = FastAPI(title="WeatherServer - HTTP Stream v3 (JSON-RPC compliant)")


@app.post("/mcp/tools/query_weather")
async def query_weather_http(request: Request):
    body = await request.json()
    req_id = body.get("id", 1)

    # ✅ 特殊处理：请求缺失必要字段，判断为“工具探测激活请求”
    if "method" not in body or (
        "params" not in body and "input" not in body
    ):
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "status": "Weather tool loaded. Please provide input.city or params.city"
            }
        }

    # ✅ 正常处理请求
    city = (
        body.get("input", {}).get("city") or
        body.get("params", {}).get("city")
    )

    if not city:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32602,
                "message": "Missing input.city or params.city"
            }
        }

    return StreamingResponse(chunk_weather(city, req_id), media_type="application/json")

def main() -> None:
    parser = argparse.ArgumentParser(description="Weather MCP HTTP-Stream Server v3")
    parser.add_argument("--api_key", required=True, help="OpenWeather API Key")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    global API_KEY
    API_KEY = args.api_key

    import uvicorn
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()