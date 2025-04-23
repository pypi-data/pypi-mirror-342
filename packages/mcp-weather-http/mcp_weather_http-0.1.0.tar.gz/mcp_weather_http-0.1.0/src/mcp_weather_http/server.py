# weather_http_server.py  ——  Streamable HTTP (chunk) 版
import argparse
import asyncio
import json
from typing import Any, AsyncIterator

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from mcp.server.fastmcp import FastMCP

##############################################################################
#                    0. FastMCP ── 只用来声明“工具”签名                       #
##############################################################################
mcp = FastMCP("WeatherServer")

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY: str | None = None
USER_AGENT = "weather-app/1.0"


async def fetch_weather(city: str) -> dict[str, Any] | None:
    """真正向 OpenWeather 拉数据"""
    if not API_KEY:
        return {"error": "❌ 未设置 API_KEY"}
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "zh_cn"}
    headers = {"User-Agent": USER_AGENT}
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            r = await client.get(OPENWEATHER_URL, params=params, headers=headers)
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP 错误: {e.response.status_code}"}
        except Exception as e:  # noqa: BLE001
            return {"error": f"请求失败: {e}"}


def format_weather(d: dict[str, Any] | str) -> str:
    """把 API JSON → 可读文本"""
    if isinstance(d, str):
        try:
            d = json.loads(d)
        except Exception as e:
            return f"无法解析天气数据: {e}"
    if "error" in d:
        return d["error"]

    city = d.get("name", "未知")
    country = d.get("sys", {}).get("country", "未知")
    temp = d.get("main", {}).get("temp", "N/A")
    humidity = d.get("main", {}).get("humidity", "N/A")
    wind = d.get("wind", {}).get("speed", "N/A")
    desc = d.get("weather", [{}])[0].get("description", "未知")
    return (
        f"🌍 {city}, {country}\n🌡 温度: {temp}°C\n💧 湿度: {humidity}%\n"
        f"🌬 风速: {wind} m/s\n🌤 天气: {desc}"
    )


@mcp.tool()  # <= 仍保留 FastMCP 元数据（对 MCP 客户端可见）
async def query_weather(city: str) -> str:  # noqa: D401
    """返回格式化后的今日天气"""
    data = await fetch_weather(city)
    return format_weather(data)


##############################################################################
#                     1. FastAPI ── “Streamable HTTP” 实现                    #
##############################################################################
app = FastAPI(title="WeatherServer-HTTP-Stream")


async def chunk_weather(city: str) -> AsyncIterator[bytes]:
    """
    Streamable HTTP 生成器：
    每 `yield` 一个 JSON 块，换行分隔，客户端边到边处理。
    """
    # 1) 先推送 ack / 进度
    yield json.dumps({"status": "fetching", "city": city}).encode() + b"\n"

    # 2) 真正抓天气
    data = await fetch_weather(city)

    # 3) 最终结果
    yield json.dumps({"result": format_weather(data)}).encode() + b"\n"

    # 4) 结束标记（可选）
    yield json.dumps({"done": True}).encode() + b"\n"


@app.post("/mcp/tools/query_weather")  # ← HTTP Streamable 端点
async def query_weather_http(req: Request):
    body = await req.json()
    # Streamable HTTP 的惯例：body = {"input": {...}, ...}
    city = body.get("input", {}).get("city") or body.get("params", {}).get("city")
    if not city:
        return {"error": "请在 input.city 中提供城市名称"}
    return StreamingResponse(chunk_weather(city), media_type="application/json")


##############################################################################
#                               启动脚本                                     #
##############################################################################
def main() -> None:
    parser = argparse.ArgumentParser(description="Weather HTTP-Stream MCP Server")
    parser.add_argument("--api_key", required=True, help="OpenWeather API Key")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    global API_KEY  # noqa: PLW0603
    API_KEY = args.api_key

    import uvicorn  # 延迟导入，避免无谓依赖
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
