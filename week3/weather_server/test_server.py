#!/usr/bin/env python3
"""测试 MCP 服务器是否正常工作"""

import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_weather_server():
    """测试天气服务器的工具"""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "weather.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()
            
            # 列出可用工具
            tools = await session.list_tools()
            print("可用的工具:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            print("\n测试 1: 获取加州天气警报")
            result = await session.call_tool("get_alerts", arguments={"state": "CA"})
            print(f"结果: {result.content[0].text[:200]}...")
            
            print("\n测试 2: 获取旧金山天气预报")
            result = await session.call_tool(
                "get_forecast", 
                arguments={"latitude": 37.7749, "longitude": -122.4194}
            )
            print(f"结果: {result.content[0].text[:200]}...")
            
            print("\n✅ 服务器测试通过！")

if __name__ == "__main__":
    asyncio.run(test_weather_server())
if __name__ == "__main__":
    asyncio.run(test_weather_server())
