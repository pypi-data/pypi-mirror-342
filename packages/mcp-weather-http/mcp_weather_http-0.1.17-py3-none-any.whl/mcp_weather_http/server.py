"""weather_http_server_v7.py – MCP Streamable HTTP (tools/list + tools/call)
=======================================================================
• initialize  → protocolVersion + capabilities(streaming, tools)
• tools/list  → paginated tool registry (single get_weather tool)
• tools/call  → execute get_weather and stream result
• fully backward-compatible activation probe & error handling
"""

from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any, AsyncIterator

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

# -----------------------------------------------------------------------------
# Server constants & metadata
# -----------------------------------------------------------------------------
SERVER_NAME = "WeatherServer"
SERVER_VERSION = "0.2.0"
PROTOCOL_VERSION = "2024-11-05"  

# -----------------------------------------------------------------------------
# Weather helpers
# -----------------------------------------------------------------------------
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY: str | None = None
USER_AGENT = "weather-app/1.0"


async def fetch_weather(city: str) -> dict[str, Any]:
    if not API_KEY:
        return {"error": "API_KEY 未设置，请提供有效的 OpenWeather API Key。"}

    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "zh_cn"}
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


async def stream_weather(city: str, req_id: int | str) -> AsyncIterator[bytes]:
    yield json.dumps({"jsonrpc": "2.0", "id": req_id, "stream": f"正在查询 {city} 天气…"}).encode() + b"\n"
    await asyncio.sleep(0.3)
    data = await fetch_weather(city)
    if "error" in data:
        yield json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": data["error"]}}).encode() + b"\n"
        return
    yield json.dumps({"jsonrpc": "2.0", "id": req_id, "result": {
        "content": [{"type": "text", "text": format_weather(data)}],
        "isError": False
    }}).encode() + b"\n"

# -----------------------------------------------------------------------------
# FastAPI application
# -----------------------------------------------------------------------------

app = FastAPI(title="WeatherServer HTTP-Stream v7")

# tool definition (single page)
TOOLS_PAGE = {
    "tools": [
        {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name, e.g. 'Hangzhou'"
                    }
                },
                "required": ["city"],
            }
        }
    ],
    "nextCursor": None
}

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    try:
        body = await request.json()
    except Exception:
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}

    req_id = body.get("id", 1)
    method = body.get("method")

    # 1) activation probe (no method)
    if method is None:
        return {"jsonrpc": "2.0", "id": req_id, "result": {"status": "Tool server online."}}

    # 2) initialize
    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": req_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                "capabilities": {
                    "streaming": True,
                    "tools": {"listChanged": False}
                }
            }
        }

    # 3) tools/list (pagination not used)
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": TOOLS_PAGE}

    # 4) tools/call
    if method == "tools/call":
        params = body.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name != "get_weather":
            return {"jsonrpc": "2.0", "id": req_id,
                    "error": {"code": -32602, "message": "Unknown tool"}}

        city = args.get("city")
        if not city:
            return {"jsonrpc": "2.0", "id": req_id,
                    "error": {"code": -32602, "message": "Missing city"}}

        return StreamingResponse(stream_weather(city, req_id), media_type="application/json")

    # 5) unknown method
    return {"jsonrpc": "2.0", "id": req_id,
            "error": {"code": -32601, "message": "Method not found"}}

# -----------------------------------------------------------------------------
# CLI launcher
# -----------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Weather MCP HTTP-Stream v7")
    parser.add_argument("--api_key", required=True)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    global API_KEY
    API_KEY = args.api_key

    import uvicorn
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()