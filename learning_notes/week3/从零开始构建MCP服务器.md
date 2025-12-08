# AI Engineer 完整教程
## 从零开始构建 MCP 服务器

> 基于 `weather_server` 项目的系统化学习路径

---

## 目录
- [模块一：AI Agent 基础概念](#模块一ai-agent-基础概念)
- [模块二：Python 现代工程实践](#模块二python-现代工程实践)
- [模块三：异步编程核心](#模块三异步编程核心)
- [模块四：MCP 协议深度解析](#模块四mcp-协议深度解析)
- [模块五：测试与可靠性](#模块五测试与可靠性)
- [模块六：生产部署与最佳实践](#模块六生产部署与最佳实践)

---

## 模块一：AI Agent 基础概念

### 1.1 什么是 AI Agent？

**传统编程 vs AI Agent**

```
传统程序：
输入 → 固定逻辑 → 输出

AI Agent：
输入 → LLM 推理 → 调用工具 → 获取信息 → LLM 综合 → 输出
```

**核心特点**：
- **自主性**：Agent 可以决定调用哪些工具
- **动态性**：根据上下文动态选择行为
- **工具使用能力**：可以调用外部 API、数据库、文件系统等

### 1.2 Tool-use Pattern（工具使用模式）

这是 AI Agent 最核心的设计模式：

```
用户："旧金山明天天气如何？"
  ↓
LLM 分析：需要调用天气工具
  ↓
调用 get_forecast(latitude=37.77, longitude=-122.41)
  ↓
获取天气数据
  ↓
LLM 生成自然语言回复："明天旧金山晴天，最高温度 18°C..."
```

### 1.3 MCP 协议简介

**Model Context Protocol (MCP)** 是 Anthropic 推出的开放标准，用于统一 AI Agent 与工具的连接方式。

**为什么需要 MCP？**

在 MCP 之前：
```
LangChain 工具 → 只能在 LangChain 中使用
AutoGen 工具 → 只能在 AutoGen 中使用
OpenAI Function Calling → 需要手动转换格式
```

有了 MCP：
```
MCP Server → Claude Desktop ✅
           → Cursor IDE ✅
           → 任何支持 MCP 的客户端 ✅
```

**MCP 三大核心能力**：
1. **Tools**：可调用的函数（如获取天气、查询数据库）
2. **Resources**：可访问的资源（如文件、URL）
3. **Prompts**：预设的提示词模板

我们的 `weather_server` 项目主要使用 **Tools** 能力。

### 1.4 MCP 架构图

```
┌─────────────────┐
│  MCP Client     │  ← Claude Desktop / Cursor / 自定义客户端
│  (AI 模型端)    │
└────────┬────────┘
         │ JSON-RPC over stdio/HTTP
         │
┌────────▼────────┐
│  MCP Server     │  ← 我们要开发的部分
│  (工具提供端)   │
└────────┬────────┘
         │
┌────────▼────────┐
│  External APIs  │  ← 天气 API / GitHub API / 数据库等
└─────────────────┘
```

### 1.5 实践任务

**任务 1.1**：理解 AI Agent 的价值
- 思考：传统的"查天气网站"与"AI Agent 查天气"有什么区别？
- 答案提示：自然语言理解、多步骤推理、个性化回复

**任务 1.2**：探索现有 MCP 服务器
- 访问 [modelcontextprotocol.io](https://modelcontextprotocol.io)
- 查看官方示例：Filesystem、Database、GitHub 等
- 理解不同场景下 MCP 的应用

---

## 模块二：Python 现代工程实践

### 2.1 为什么选择 uv？

**传统 Python 包管理的问题**：
```bash
# pip 方式（问题多）
pip install requests    # 不会锁定版本
pip install pandas      # 依赖冲突风险高
pip freeze > requirements.txt  # 包含所有依赖，冗余

# poetry 方式（较好但慢）
poetry add requests     # 依赖解析慢
poetry install          # 安装速度慢
```

**uv 的优势**：
- ⚡ **极快**：Rust 编写，比 pip 快 10-100 倍
- 🔒 **可靠**：自动生成 `uv.lock` 锁定依赖版本
- 🎯 **简洁**：统一的命令接口，无需记忆多个工具

### 2.2 uv 核心命令速查

```bash
# 初始化项目
uv init --name my_project

# 创建虚拟环境
uv venv

# 激活虚拟环境
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows

# 安装包
uv add httpx               # 添加生产依赖
uv add --dev pytest        # 添加开发依赖

# 运行脚本（自动使用虚拟环境）
uv run my_script.py

# 同步依赖（根据 pyproject.toml）
uv sync
```

### 2.3 pyproject.toml 深度解析

以 `weather_server` 项目为例：

```toml
[project]
name = "weather"                    # 项目名称
version = "0.1.0"                   # 版本号
description = "Weather MCP Server"  # 简短描述
readme = "README.md"                # 文档文件
requires-python = ">=3.13"          # 最低 Python 版本

dependencies = [                    # 生产依赖
    "httpx>=0.27.2",               # HTTP 客户端
    "mcp[cli]>=1.1.2",             # MCP SDK
]

[build-system]
requires = ["hatchling"]            # 构建工具
build-backend = "hatchling.build"   # 构建后端
```

**关键理解**：
- `dependencies`：运行时必需的包
- `requires-python`：限制 Python 版本，避免兼容性问题
- `[build-system]`：定义如何打包项目为 wheel

### 2.4 虚拟环境原理

**为什么需要虚拟环境？**

```
系统 Python (全局)：
/usr/bin/python3
└── 所有项目共用，容易冲突

虚拟环境（隔离）：
项目A/.venv/bin/python → httpx 0.27.0
项目B/.venv/bin/python → httpx 0.30.0
                      ↑ 互不干扰
```

**uv venv 做了什么？**
1. 复制 Python 解释器到 `.venv/`
2. 创建独立的 `site-packages` 目录
3. 修改 `PATH` 环境变量，优先使用 `.venv/bin/python`

### 2.5 项目结构规范

```
weather_server/
├── .venv/              # 虚拟环境（不提交到 Git）
├── .python-version     # 固定 Python 版本（3.13）
├── pyproject.toml      # 项目配置
├── uv.lock             # 依赖锁文件（确保可复现）
├── README.md           # 项目文档
├── weather.py          # 主程序
└── test_server.py      # 测试脚本
```

**重要文件解释**：
- `.python-version`：uv 自动使用此版本的 Python
- `uv.lock`：记录所有依赖的精确版本，确保团队成员环境一致

### 2.6 实践任务

**任务 2.1**：从零搭建项目
```bash
# 1. 创建项目目录
mkdir my-mcp-server && cd my-mcp-server

# 2. 初始化 uv 项目
uv init --name my-server

# 3. 创建虚拟环境
uv venv

# 4. 安装依赖
uv add "mcp[cli]" httpx

# 5. 验证安装
uv run python -c "import mcp; print('MCP installed')"
```

**任务 2.2**：理解依赖管理
- 打开 `pyproject.toml`，查看 `dependencies` 部分
- 运行 `uv add pytest`，观察文件变化
- 打开 `uv.lock`，找到 `httpx` 的精确版本号

**任务 2.3**：探索虚拟环境
```bash
# 查看虚拟环境中的 Python
ls .venv/bin/

# 查看已安装的包
uv pip list
```

---

## 模块三：异步编程核心

### 3.1 为什么需要异步编程？

**同步 vs 异步的区别**：

```python
# 同步方式（阻塞）
import requests

def get_weather_sync():
    response1 = requests.get("https://api.weather.gov/...")  # 等待 2 秒
    response2 = requests.get("https://api.weather.gov/...")  # 等待 2 秒
    # 总耗时：4 秒

# 异步方式（非阻塞）
import httpx
import asyncio

async def get_weather_async():
    async with httpx.AsyncClient() as client:
        task1 = client.get("https://api.weather.gov/...")
        task2 = client.get("https://api.weather.gov/...")
        response1, response2 = await asyncio.gather(task1, task2)
        # 总耗时：2 秒（并发执行）
```

**适用场景**：
- ✅ I/O 密集型：网络请求、文件读写、数据库查询
- ❌ CPU 密集型：数学计算、图像处理（应使用多进程）

### 3.2 async/await 语法详解

**基础语法**：

```python
# 定义异步函数
async def fetch_data():
    # await 会暂停当前函数，等待结果
    result = await some_async_operation()
    return result

# 调用异步函数
asyncio.run(fetch_data())
```

**关键规则**：
1. `async def` 定义的函数返回一个 **协程对象**（Coroutine）
2. `await` 只能在 `async def` 内部使用
3. `asyncio.run()` 用于启动异步程序的入口点

### 3.3 httpx 异步客户端

**为什么选择 httpx？**
- ✅ 原生支持 `async/await`
- ✅ 自动处理连接池
- ✅ 支持 HTTP/2
- ✅ API 设计与 `requests` 相似

**标准用法**：

```python
import httpx

async def make_request():
    # 使用上下文管理器自动关闭连接
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.example.com/data",
            headers={"User-Agent": "my-app/1.0"},
            timeout=30.0  # 30秒超时
        )
        response.raise_for_status()  # 4xx/5xx 抛出异常
        return response.json()
```

### 3.4 weather_server 中的异步设计

**核心函数剖析**：

```python
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """带错误处理的 NWS API 请求
    
    返回值：
    - 成功：返回 JSON 字典
    - 失败：返回 None（而不是抛出异常）
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    
    # 异步上下文管理器：自动管理连接
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            # await 等待 HTTP 响应
            response = await client.get(url, headers=headers, timeout=30.0)
            
            # 检查状态码（4xx/5xx 会抛出异常）
            response.raise_for_status()
            
            return response.json()
        except Exception:
            # 捕获所有异常，返回 None
            # 生产环境应该记录日志：logging.error(f"Request failed: {e}")
            return None
```

**设计亮点**：
1. **follow_redirects=True**：自动处理 301/302 重定向
2. **timeout=30.0**：避免无限等待
3. **异常处理**：优雅返回 None，而不是让程序崩溃
4. **类型提示**：`dict[str, Any] | None` 明确返回值可能是字典或 None

### 3.5 常见错误与解决方案

**错误 1：忘记 await**
```python
# ❌ 错误
result = make_nws_request(url)  # result 是协程对象，不是数据

# ✅ 正确
result = await make_nws_request(url)
```

**错误 2：在同步函数中使用 await**
```python
# ❌ 错误
def sync_function():
    data = await async_function()  # SyntaxError

# ✅ 正确
async def async_function_wrapper():
    data = await async_function()
```

**错误 3：未处理超时**
```python
# ❌ 危险（可能无限等待）
response = await client.get(url)

# ✅ 安全（30秒超时）
response = await client.get(url, timeout=30.0)
```

### 3.6 实践任务

**任务 3.1**：编写第一个异步函数
```python
import httpx
import asyncio

async def fetch_github_user(username: str):
    """获取 GitHub 用户信息"""
    url = f"https://api.github.com/users/{username}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# 运行
asyncio.run(fetch_github_user("torvalds"))
```

**任务 3.2**：并发请求
```python
async def fetch_multiple_users(usernames: list[str]):
    """并发获取多个用户信息"""
    async with httpx.AsyncClient() as client:
        tasks = [client.get(f"https://api.github.com/users/{u}") for u in usernames]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]

asyncio.run(fetch_multiple_users(["torvalds", "gvanrossum"]))
```

**任务 3.3**：错误处理
- 修改任务 3.1，添加 `try/except` 捕获网络错误
- 测试：故意使用无效的 URL，观察程序行为

---

## 模块四：MCP 协议深度解析

### 4.1 MCP 核心概念回顾

**三大能力**：
1. **Tools**：函数调用（本项目重点）
2. **Resources**：资源访问（文件、URL）
3. **Prompts**：提示词模板

**传输模式**：
- **stdio**：通过标准输入/输出通信（本地使用）
- **HTTP**：通过 HTTP 协议通信（远程部署）

### 4.2 FastMCP 框架详解

**什么是 FastMCP？**

FastMCP 是 MCP 官方提供的 Python 框架，类似于 FastAPI：
- 使用装饰器定义工具
- 自动推断参数类型
- 自动生成工具描述

**基础用法**：

```python
from mcp.server.fastmcp import FastMCP

# 1. 初始化服务器
mcp = FastMCP("weather")  # "weather" 是服务器名称

# 2. 定义工具
@mcp.tool()
async def my_tool(param1: str, param2: int) -> str:
    """这是工具的描述，会显示给 AI 模型
    
    Args:
        param1: 参数1的说明
        param2: 参数2的说明
    """
    return f"Received {param1} and {param2}"

# 3. 启动服务器
mcp.run(transport='stdio')
```

### 4.3 工具定义最佳实践

**示例：get_alerts 工具**

```python
@mcp.tool()
async def get_alerts(state: str) -> str:
    """获取美国某州的天气警报
    
    Args:
        state: 两位州代码（如 CA, NY, TX）
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)
    
    # 错误处理：API 失败
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."
    
    # 边缘情况：无警报
    if not data["features"]:
        return "No active alerts for this state."
    
    # 格式化输出
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)
```

**设计要点**：
1. **清晰的 Docstring**：AI 模型会读取这些描述来决定何时调用工具
2. **参数类型提示**：`state: str` 会自动转换为 JSON Schema
3. **错误处理**：永远不要让工具抛出未捕获的异常
4. **友好的输出**：返回人类可读的字符串，而不是原始 JSON

### 4.4 参数类型自动推断

FastMCP 支持的类型：

```python
# 基础类型
@mcp.tool()
async def example(
    text: str,           # 字符串
    count: int,          # 整数
    price: float,        # 浮点数
    active: bool,        # 布尔值
) -> str:
    pass

# 可选参数
@mcp.tool()
async def example(
    required: str,              # 必需参数
    optional: str = "default"   # 可选参数（有默认值）
) -> str:
    pass

# 联合类型（Python 3.10+）
@mcp.tool()
async def example(
    value: str | int  # 可以是字符串或整数
) -> str:
    pass
```

**生成的 JSON Schema**：
```json
{
  "name": "example",
  "parameters": {
    "type": "object",
    "properties": {
      "text": {"type": "string"},
      "count": {"type": "integer"},
      "price": {"type": "number"},
      "active": {"type": "boolean"}
    },
    "required": ["text", "count", "price", "active"]
  }
}
```

### 4.5 stdio 传输模式深度解析

**为什么不能用 print()？**

```python
# ❌ 错误示例
@mcp.tool()
async def my_tool():
    print("Debug info")  # 这会破坏 JSON-RPC 协议！
    return "result"
```

**原因**：
- MCP 通过 **标准输出（stdout）** 传输 JSON-RPC 消息
- `print()` 会输出到 stdout，导致消息格式错误
- 客户端会收到无效的 JSON，连接失败

**正确的日志方式**：
```python
import logging
import sys

# 配置日志输出到 stderr（不是 stdout）
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,  # 关键！
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@mcp.tool()
async def my_tool():
    logging.info("Tool called")  # ✅ 正确
    return "result"
```

### 4.6 JSON-RPC 通信示例

**客户端请求**（stdin）：
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_alerts",
    "arguments": {
      "state": "CA"
    }
  }
}
```

**服务器响应**（stdout）：
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "No active alerts for this state."
      }
    ]
  }
}
```

### 4.7 实践任务

**任务 4.1**：添加新工具
为 `weather_server` 添加第三个工具：
```python
@mcp.tool()
async def get_observation_stations(latitude: float, longitude: float) -> str:
    """获取某地附近的气象观测站
    
    Args:
        latitude: 纬度
        longitude: 经度
    """
    # 实现提示：
    # 1. 先调用 /points/{lat},{lon} 获取 gridpoint
    # 2. 再调用 observationStations endpoint
    pass
```

**任务 4.2**：理解工具描述的重要性
- 修改 `get_alerts` 的 docstring，删除参数说明
- 重启服务器，观察 Claude 是否仍能正确使用该工具
- 结论：清晰的描述对 AI 模型非常重要

**任务 4.3**：调试 JSON-RPC 通信
```bash
# 手动测试 MCP 服务器
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | uv run weather.py
```
观察输出的 JSON 格式。

---

## 模块五：测试与可靠性

### 5.1 为什么测试 MCP 服务器很重要？

**常见故障场景**：
1. **API 超时**：外部 API 响应慢或不可用
2. **参数错误**：用户输入无效的州代码（如 "ZZ"）
3. **数据格式变化**：天气 API 修改了返回格式
4. **网络问题**：无法连接到外部服务

**测试的价值**：
- ✅ 在开发阶段发现问题
- ✅ 确保修改不会破坏现有功能
- ✅ 提高代码信心

### 5.2 MCP 客户端测试架构

**核心组件**：

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 1. 定义服务器参数
server_params = StdioServerParameters(
    command="uv",              # 启动命令
    args=["run", "weather.py"], # 参数
    env=None                   # 环境变量
)

# 2. 启动服务器并建立连接
async with stdio_client(server_params) as (read, write):
    # 3. 创建会话
    async with ClientSession(read, write) as session:
        # 4. 初始化连接
        await session.initialize()
        
        # 5. 调用工具
        result = await session.call_tool("get_alerts", arguments={"state": "CA"})
```

**工作原理**：
1. `stdio_client` 启动子进程运行服务器
2. `ClientSession` 管理 JSON-RPC 通信
3. `session.initialize()` 握手协议
4. `session.call_tool()` 调用工具并等待响应

### 5.3 完整测试代码解析

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_weather_server():
    """测试天气服务器的所有工具"""
    
    # Step 1: 配置服务器启动参数
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "weather.py"],
        env=None  # 如果需要 API Key，在这里设置环境变量
    )
    
    # Step 2: 启动服务器（自动管理生命周期）
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # Step 3: 初始化连接（必需）
            await session.initialize()
            
            # Step 4: 列出可用工具（验证服务器响应）
            tools = await session.list_tools()
            print("可用的工具:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Step 5: 测试工具 1 - 天气警报
            print("\n测试 1: 获取加州天气警报")
            result = await session.call_tool(
                "get_alerts",
                arguments={"state": "CA"}
            )
            # result.content 是一个列表，通常包含一个 TextContent 对象
            print(f"结果: {result.content[0].text[:200]}...")
            
            # Step 6: 测试工具 2 - 天气预报
            print("\n测试 2: 获取旧金山天气预报")
            result = await session.call_tool(
                "get_forecast",
                arguments={
                    "latitude": 37.7749,
                    "longitude": -122.4194
                }
            )
            print(f"结果: {result.content[0].text[:200]}...")
            
            print("\n✅ 服务器测试通过！")

if __name__ == "__main__":
    asyncio.run(test_weather_server())
```

### 5.4 错误处理策略

**策略 1：优雅降级**
```python
async def get_alerts(state: str) -> str:
    data = await make_nws_request(url)
    
    # 而不是抛出异常，返回友好的错误消息
    if not data:
        return "Unable to fetch alerts. The weather service may be temporarily unavailable."
```

**策略 2：超时保护**
```python
async with httpx.AsyncClient() as client:
    response = await client.get(url, timeout=30.0)
    # 30秒后自动抛出 TimeoutError
```

**策略 3：重试机制（高级）**
```python
async def make_nws_request_with_retry(url: str, max_retries: int = 3) -> dict | None:
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            if attempt == max_retries - 1:
                return None
            await asyncio.sleep(2 ** attempt)  # 指数退避
```

### 5.5 边缘情况处理

**示例 1：空结果**
```python
if not data["features"]:
    return "No active alerts for this state."  # 而不是返回空字符串
```

**示例 2：缺失字段**
```python
def format_alert(feature: dict) -> str:
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}  # 使用 .get() 提供默认值
Area: {props.get('areaDesc', 'Unknown')}
"""
```

**示例 3：无效输入**
```python
@mcp.tool()
async def get_alerts(state: str) -> str:
    # 验证州代码格式
    if len(state) != 2 or not state.isalpha():
        return "Invalid state code. Please use 2-letter codes like CA, NY, TX."
    
    # 转换为大写
    state = state.upper()
    # ...
```

### 5.6 实践任务

**任务 5.1**：运行测试
```bash
cd week3/weather_server
uv run test_server.py
```
观察输出，确保两个工具都正常工作。

**任务 5.2**：测试错误处理
修改 `test_server.py`，添加以下测试：
```python
# 测试无效州代码
result = await session.call_tool("get_alerts", arguments={"state": "ZZ"})
print(f"无效州代码结果: {result.content[0].text}")

# 测试无效坐标
result = await session.call_tool("get_forecast", arguments={
    "latitude": 999,
    "longitude": 999
})
print(f"无效坐标结果: {result.content[0].text}")
```

**任务 5.3**：添加日志
在 `weather.py` 中添加日志记录：
```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@mcp.tool()
async def get_alerts(state: str) -> str:
    logging.info(f"get_alerts called with state={state}")
    # ...
```

---

## 模块六：生产部署与最佳实践

### 6.1 Claude Desktop 集成

**配置步骤**：

**Step 1**：找到配置文件路径
```bash
# macOS
~/Library/Application Support/Claude/claude_desktop_config.json

# Windows
%APPDATA%\Claude\claude_desktop_config.json
```

**Step 2**：编辑配置文件
```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/David/Desktop/github_repos/modern-software-dev-assignments/week3/weather_server",
        "run",
        "weather.py"
      ]
    }
  }
}
```

**关键参数**：
- `--directory`：指定项目目录（使用绝对路径）
- `uv run weather.py`：uv 会自动激活虚拟环境

**Step 3**：重启 Claude Desktop
- 完全退出 Claude Desktop
- 重新启动应用

**Step 4**：验证连接
在 Claude Desktop 中输入：
```
请帮我查询加州的天气警报
```

如果配置正确，Claude 会调用 `get_alerts` 工具。

### 6.2 日志记录最佳实践

**为什么不能用 print()？**
- stdio 模式下，stdout 用于 JSON-RPC 通信
- `print()` 会破坏协议，导致连接失败

**正确的日志配置**：

```python
import logging
import sys

# 配置日志输出到 stderr
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,  # 关键！
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@mcp.tool()
async def get_alerts(state: str) -> str:
    logger.info(f"Fetching alerts for state: {state}")
    
    data = await make_nws_request(url)
    
    if not data:
        logger.error(f"Failed to fetch alerts for {state}")
        return "Unable to fetch alerts."
    
    logger.info(f"Successfully fetched {len(data['features'])} alerts")
    return format_alerts(data)
```

**查看日志**：
```bash
# 日志会输出到终端的 stderr
uv run weather.py 2> weather.log  # 重定向到文件
```

### 6.3 安全性考量

**6.3.1 API Key 管理**

**❌ 错误做法**：
```python
# 硬编码 API Key（危险！）
API_KEY = "sk-1234567890abcdef"
```

**✅ 正确做法**：
```python
import os

# 从环境变量读取
API_KEY = os.getenv("WEATHER_API_KEY")

if not API_KEY:
    raise ValueError("WEATHER_API_KEY environment variable not set")
```

**配置环境变量**：
```bash
# 方法 1：临时设置
export WEATHER_API_KEY="your_key_here"
uv run weather.py

# 方法 2：.env 文件（推荐）
echo "WEATHER_API_KEY=your_key_here" > .env
uv run weather.py  # uv 自动加载 .env
```

**Claude Desktop 配置**：
```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": ["--directory", "/path/to/project", "run", "weather.py"],
      "env": {
        "WEATHER_API_KEY": "your_key_here"
      }
    }
  }
}
```

**6.3.2 .gitignore 配置**
```
# .gitignore
.env
.venv/
*.log
__pycache__/
*.pyc
```

### 6.4 HTTP 传输模式（高级）

**适用场景**：
- 远程部署（Cloudflare Workers、Vercel）
- 团队共享服务器
- 需要 OAuth2 认证

**代码示例**：
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

# ... 定义工具 ...

if __name__ == "__main__":
    # HTTP 模式
    mcp.run(transport='sse', host="0.0.0.0", port=8000)
```

**客户端配置**（Claude Desktop）：
```json
{
  "mcpServers": {
    "weather": {
      "url": "https://your-server.com/sse"
    }
  }
}
```

### 6.5 性能优化

**6.5.1 连接池复用**
```python
# ❌ 每次请求创建新客户端（低效）
@mcp.tool()
async def get_alerts(state: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

# ✅ 使用全局客户端（高效）
client = httpx.AsyncClient()

@mcp.tool()
async def get_alerts(state: str) -> str:
    response = await client.get(url)
```

**6.5.2 缓存结果**
```python
from functools import lru_cache
import time

# 简单的缓存（5分钟）
cache = {}

async def get_alerts_cached(state: str) -> str:
    now = time.time()
    if state in cache:
        result, timestamp = cache[state]
        if now - timestamp < 300:  # 5分钟缓存
            return result
    
    result = await get_alerts(state)
    cache[state] = (result, now)
    return result
```

### 6.6 部署检查清单

在部署到生产环境前，确保：

- [ ] 所有 API Key 都通过环境变量配置
- [ ] `.env` 文件已添加到 `.gitignore`
- [ ] 日志输出到 `stderr`，而不是 `stdout`
- [ ] 所有工具都有清晰的 docstring
- [ ] 错误处理覆盖所有边缘情况
- [ ] 测试脚本运行通过
- [ ] README 包含完整的安装和使用说明
- [ ] `pyproject.toml` 中的依赖版本已固定

### 6.7 实践任务

**任务 6.1**：完成 Claude Desktop 集成
按照 6.1 节步骤，将 `weather_server` 集成到 Claude Desktop。

**任务 6.2**：添加日志
在 `weather.py` 中添加完整的日志记录，运行后查看 `stderr` 输出。

**任务 6.3**：环境变量配置
1. 创建 `.env` 文件
2. 添加一个自定义配置项（如 `USER_AGENT`）
3. 修改代码读取该配置

**任务 6.4**：性能测试
使用 `time` 模块测量 `get_forecast` 的响应时间：
```python
import time

start = time.time()
result = await get_forecast(37.7749, -122.4194)
elapsed = time.time() - start
print(f"耗时: {elapsed:.2f} 秒")
```

---

## 附录：常见问题与解决方案

### Q1: 运行 `uv run weather.py` 没有任何输出？

**A**: 这是正常的！MCP 服务器使用 stdio 模式，它会：
1. 启动后等待客户端连接
2. 不会主动输出任何内容
3. 只响应 JSON-RPC 请求

**验证方法**：
```bash
# 方法 1：运行测试脚本
uv run test_server.py

# 方法 2：连接到 Claude Desktop
# （参见模块六）
```

### Q2: Claude Desktop 无法找到工具？

**检查步骤**：
1. 验证配置文件路径正确
2. 检查 JSON 格式是否有效（使用 jsonlint.com）
3. 确保使用绝对路径
4. 重启 Claude Desktop（必须完全退出）
5. 查看 Claude Desktop 的日志：
   ```bash
   # macOS
   tail -f ~/Library/Logs/Claude/mcp*.log
   ```

### Q3: `httpx.ConnectError` 或超时错误？

**原因**：
- 网络问题
- API 不可用
- 防火墙阻止

**解决方案**：
```python
# 增加超时时间
response = await client.get(url, timeout=60.0)

# 添加重试逻辑
for attempt in range(3):
    try:
        response = await client.get(url, timeout=30.0)
        break
    except httpx.TimeoutException:
        if attempt == 2:
            return None
        await asyncio.sleep(2)
```

### Q4: 如何调试 JSON-RPC 通信？

**方法 1：手动测试**
```bash
# 发送 tools/list 请求
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | uv run weather.py
```

**方法 2：使用 MCP Inspector**
```bash
npx @modelcontextprotocol/inspector uv run weather.py
```

### Q5: Python 版本冲突？

**错误信息**：
```
error: Python 3.13 is required but not found
```

**解决方案**：
```bash
# 安装指定 Python 版本
uv python install 3.13

# 或修改 .python-version 文件
echo "3.12" > .python-version
uv sync
```

---

## 总结：AI Engineer 技能树

通过本教程，你已经掌握：

### ✅ 基础层
- AI Agent 工作原理
- MCP 协议架构
- Python 异步编程

### ✅ 工程层
- uv 包管理
- 项目结构规范
- 虚拟环境管理

### ✅ 实战层
- FastMCP 框架使用
- 工具定义与测试
- 错误处理策略

### ✅ 生产层
- Claude Desktop 集成
- 日志与监控
- 安全性最佳实践

### 🚀 下一步学习方向

1. **扩展工具能力**
   - 添加更多天气 API（OpenWeatherMap、AccuWeather）
   - 实现 Resources 和 Prompts 能力

2. **高级架构**
   - 学习 HTTP 传输模式
   - 实现 OAuth2 认证
   - 部署到 Cloudflare Workers

3. **真实项目**
   - GitHub API MCP Server
   - Database Query MCP Server
   - File System MCP Server

4. **探索其他框架**
   - LangChain MCP 集成
   - AutoGen + MCP
   - 自定义 MCP 客户端

---

## 参考资源

- [MCP 官方文档](https://modelcontextprotocol.io)
- [FastMCP GitHub](https://github.com/modelcontextprotocol/mcp)
- [uv 官方文档](https://docs.astral.sh/uv/)
- [httpx 文档](https://www.python-httpx.org)
- [National Weather Service API](https://www.weather.gov/documentation/services-web-api)

---

**版本**: 1.0.0  
**最后更新**: 2025-12-08  
**作者**: AI Engineering Course  
**许可**: MIT License
