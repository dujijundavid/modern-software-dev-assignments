# Weather MCP Server

## 项目概述
这是一个基于 Model Context Protocol (MCP) 的天气服务器，提供两个工具：
- `get_alerts`: 获取美国各州的天气警报
- `get_forecast`: 获取指定经纬度的天气预报

数据来源：美国国家气象局 API (National Weather Service)

## 环境配置过程（详细思路讲解）

### 步骤1: 清理环境
**思路**: 官方教程推荐使用 `uv` 工具统一管理项目，不需要额外的 conda 环境。

### 步骤2: 初始化 uv 项目
**思路**: `uv` 需要 `pyproject.toml` 来管理依赖，使用 `uv init` 创建标准项目结构。
```bash
cd weather_server
uv init --name weather --no-readme --no-workspace
```
- `--name weather`: 项目名称
- `--no-readme`: 不生成 README（我们自己创建）
- `--no-workspace`: 独立项目，不与父目录形成工作区

### 步骤3: 创建虚拟环境
**思路**: uv 虚拟环境隔离项目依赖，避免污染系统 Python。
```bash
uv venv
```
这会创建 `.venv` 目录，包含独立的 Python 解释器和包。

### 步骤4: 安装依赖
**思路**: MCP SDK 提供服务器框架，httpx 用于异步 HTTP 请求天气 API。
```bash
source .venv/bin/activate
uv add "mcp[cli]" httpx
```
安装的关键包：
- `mcp[cli]`: MCP 官方 SDK，包含 FastMCP 类
- `httpx`: 现代异步 HTTP 客户端
- 自动安装的依赖：pydantic（数据验证）、starlette（ASGI框架）等

### 步骤5: 实现服务器代码
**思路**: 按照官方文档结构组织代码
```python
# 1. 导入依赖
from mcp.server.fastmcp import FastMCP
import httpx

# 2. 初始化 MCP 服务器实例
mcp = FastMCP("weather")

# 3. 定义工具函数（用 @mcp.tool() 装饰器）
@mcp.tool()
async def get_alerts(state: str) -> str:
    # 工具逻辑...
    pass

# 4. 启动服务器
def main():
    mcp.run(transport='stdio')  # 使用标准输入/输出通信
```

**关键设计点**:
- 使用 `async/await` 异步模式提高性能
- 工具函数的文档字符串会自动生成工具描述
- `transport='stdio'` 表示通过标准输入输出与客户端通信（适合 Claude Desktop）

## 运行服务器

### ⚠️ 重要说明
**直接运行 `uv run weather.py` 不会有任何输出！这是正常的！**

原因：MCP 服务器使用 `stdio` (标准输入/输出) 传输模式，它会：
1. 启动后等待来自客户端的 JSON-RPC 消息
2. 不会主动输出任何内容（根据 MCP 规范，stdio 模式下禁止使用 `print()`）
3. 只有当客户端（如 Claude Desktop）连接时才会响应

### 方式1: 通过 Claude Desktop 使用（推荐）
这是 MCP 服务器的设计用途，见下方"连接到 Claude for Desktop"章节。

### 方式2: 使用测试脚本验证服务器
```bash
uv run test_server.py
```
这会模拟客户端连接，测试服务器的两个工具是否正常工作。

## 连接到 Claude for Desktop

### 配置步骤
1. 打开 Claude for Desktop 配置文件：
```bash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. 添加服务器配置：
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

3. 重启 Claude for Desktop

### 测试工具
在 Claude for Desktop 中尝试：
- "What's the weather in Sacramento?"
- "What are the active weather alerts in Texas?"

## 代码结构说明

### 1. 常量定义
```python
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"
```
**思路**: API 基础 URL 和用户代理，便于维护和符合 API 使用规范。

### 2. 辅助函数
```python
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """发送请求到 NWS API 并处理错误"""
```
**思路**: 封装 HTTP 请求逻辑，统一错误处理，提高代码复用性。

### 3. 工具函数
```python
@mcp.tool()
async def get_alerts(state: str) -> str:
    """获取天气警报"""
```
**思路**: 
- `@mcp.tool()` 装饰器自动注册工具到 MCP 服务器
- 函数签名中的参数会成为工具的输入参数
- 文档字符串会作为工具的描述（供 LLM 理解）
- 返回字符串作为工具执行结果

### 4. 服务器启动
```python
def main():
    mcp.run(transport='stdio')
```
**思路**: `stdio` 传输模式适合本地进程通信，Claude Desktop 通过标准输入输出与服务器交互。

## 常见问题

### Q: 为什么运行 `uv run weather.py` 没有任何输出？
**A**: 这是正常的！MCP 服务器使用 stdio 模式，它会等待客户端（如 Claude Desktop）通过标准输入发送 JSON-RPC 消息。服务器启动后会阻塞等待输入，不会主动输出内容。要测试服务器，使用 `uv run test_server.py` 或通过 Claude Desktop 连接。

### Q: 为什么使用 uv 而不是 pip？
**A**: `uv` 是 Rust 编写的现代 Python 包管理工具，比 pip 快 10-100 倍，且能更好地管理项目依赖。

### Q: 为什么需要 pyproject.toml？
**A**: 这是 Python 项目的标准配置文件（PEP 518），uv 用它来管理依赖、版本和项目元数据。

### Q: stdio 传输模式是什么？
**A**: MCP 支持多种传输方式，stdio 通过标准输入输出通信，适合本地工具集成；HTTP 传输适合远程服务。

### Q: 为什么不用 print() 调试？
**A**: 在 stdio 模式下，print() 会写入标准输出，破坏 JSON-RPC 消息格式。应该使用 Python logging 模块写入 stderr。

## 项目文件说明
- `weather.py`: MCP 服务器主程序
- `test_server.py`: 服务器测试脚本（模拟客户端连接）
- `pyproject.toml`: 项目配置和依赖管理
- `uv.lock`: 锁定依赖版本，确保可重现构建
- `.venv/`: 虚拟环境目录
- `.python-version`: Python 版本标识

## 下一步
- [ ] 添加日志记录（使用 logging 模块）
- [ ] 实现更多工具（如历史天气数据）
- [ ] 添加单元测试
- [ ] 支持更多国家的天气 API
