# Week 2 服务器运行指南

## 快速启动

```bash
# 在项目根目录执行
poetry run uvicorn week2.app.main:app --reload
```

服务器将在 http://127.0.0.1:8000 启动

---

## 命令解释

| 命令部分 | 说明 |
|----------|------|
| `poetry run` | 使用 Poetry 管理的虚拟环境运行命令 |
| `uvicorn` | ASGI 服务器（FastAPI 应用需要） |
| `week2.app.main:app` | 应用入口：`week2/app/main.py` 文件中的 `app` 对象 |
| `--reload` | 代码变更时自动重载（开发模式） |

---

## API 端点

| 方法 | 路径 | 功能 | 是否需要 Ollama |
|------|------|------|-----------------|
| GET | `/` | 前端页面 | ❌ |
| POST | `/action-items/extract` | 启发式提取（正则匹配） | ❌ |
| POST | `/action-items/extract-llm` | LLM 智能提取 | ✅ |
| GET | `/notes` | 列出所有笔记 | ❌ |

---

## Ollama 配置

### Ollama 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│  Ollama 架构                                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ~/.ollama/models/          ← 模型存储目录                  │
│    ├── llama3.1:8b          ← 已下载的模型                  │
│    └── ...                                               │
│             ↓                                               │
│  ollama serve                ← 启动 API 服务器               │
│             ↓                                               │
│  http://127.0.0.1:11434      ← API 端点                     │
│             ↓                                               │
│  Python ollama.chat()       ← 按名称调用模型                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**关键点**:
- `ollama pull` 下载模型到 `~/.ollama/models`（只需一次）
- `ollama serve` 启动服务器，**自动发现**所有已下载模型
- Python 代码通过模型名称（`llama3.1:8b`）调用，无需指定路径

### 安装 Ollama
```bash
# macOS
brew install ollama

# 或访问 https://ollama.com/download
```

### 首次使用：下载模型
```bash
# 只需执行一次，模型会被保存到 ~/.ollama/models
ollama pull llama3.1:8b
```

### 启动 Ollama 服务
```bash
# 每次使用 LLM 功能前需要启动
ollama serve

# 看到 "Listening on 127.0.0.1:11434" 表示成功
```

### 验证状态
```bash
# 查看已下载的模型
ollama list

# 输出示例：
# NAME                ID              SIZE      MODIFIED
# llama3.1:8b         ...             4.7 GB    2 days ago
```

---

## 故障排查

### 问题：LLM 调用失败
```
Error calling LLM: ConnectionError: Failed to connect to Ollama
```

**解决方法**:
1. 确保 Ollama 正在运行：`ollama serve`
2. 检查模型是否已下载：`ollama list`

**注意**: 即使 Ollama 未运行，服务器仍会正常响应其他请求，LLM 端点会返回空结果

### 问题：模块未找到
```bash
# 确保 Poetry 依赖已安装
poetry install
```

---

## 测试 API

```bash
# 启动服务器后，使用 curl 测试
# 启发式提取（无需 Ollama）
curl -X POST http://127.0.0.1:8000/action-items/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "- Fix bug\n- Write tests", "save_note": false}'

# LLM 提取（需要 Ollama 运行）
curl -X POST http://127.0.0.1:8000/action-items/extract-llm \
  -H "Content-Type: application/json" \
  -d '{"text": "Meeting notes: Need to fix bug #123 and write tests by Friday", "save_note": false}'
```
