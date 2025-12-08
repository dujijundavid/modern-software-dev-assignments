#!/usr/bin/env python3
"""
MCP Server 测试脚本
直接测试 weather MCP Server 的两个工具
"""
import asyncio
import sys
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_weather_server():
    """测试 weather MCP Server"""
    
    # 配置服务器参数
    server_params = StdioServerParameters(
        command="uv",
        args=[
            "run",
            "weather.py"
        ]
    )
    
    try:
        print("🔌 正在连接 MCP Server...")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 初始化
                await session.initialize()
                print("✅ 连接成功！\n")
                
                # 列出所有工具
                print("📋 获取可用工具列表...")
                tools = await session.list_tools()
                print(f"✅ 找到 {len(tools.tools)} 个工具：\n")
                for tool in tools.tools:
                    print(f"  📌 {tool.name}")
                    print(f"     描述: {tool.description}")
                    if tool.inputSchema:
                        print(f"     参数: {json.dumps(tool.inputSchema.get('properties', {}), indent=8, ensure_ascii=False)}")
                    print()
                
                # 测试 1: get_alerts
                print("\n" + "="*60)
                print("🚨 测试1: 获取加州天气警报")
                print("="*60)
                try:
                    result1 = await session.call_tool(
                        "get_alerts",
                        arguments={"state": "CA"}
                    )
                    response_text = result1.content[0].text
                    print("✅ 响应成功：")
                    print(response_text[:500])  # 显示前500字符
                    if len(response_text) > 500:
                        print(f"... (还有 {len(response_text) - 500} 个字符)")
                except Exception as e:
                    print(f"❌ 调用失败: {e}")
                
                # 测试 2: get_forecast
                print("\n" + "="*60)
                print("🌤️  测试2: 获取旧金山天气预报 (37.7749, -122.4194)")
                print("="*60)
                try:
                    result2 = await session.call_tool(
                        "get_forecast",
                        arguments={
                            "latitude": 37.7749,
                            "longitude": -122.4194
                        }
                    )
                    response_text = result2.content[0].text
                    print("✅ 响应成功：")
                    print(response_text[:500])  # 显示前500字符
                    if len(response_text) > 500:
                        print(f"... (还有 {len(response_text) - 500} 个字符)")
                except Exception as e:
                    print(f"❌ 调用失败: {e}")
                
                # 测试 3: get_alerts 纽约州
                print("\n" + "="*60)
                print("🚨 测试3: 获取纽约州天气警报")
                print("="*60)
                try:
                    result3 = await session.call_tool(
                        "get_alerts",
                        arguments={"state": "NY"}
                    )
                    response_text = result3.content[0].text
                    print("✅ 响应成功：")
                    print(response_text[:500])
                    if len(response_text) > 500:
                        print(f"... (还有 {len(response_text) - 500} 个字符)")
                except Exception as e:
                    print(f"❌ 调用失败: {e}")
                
                print("\n" + "="*60)
                print("✨ 所有测试完成！")
                print("="*60)
                
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_weather_server())
