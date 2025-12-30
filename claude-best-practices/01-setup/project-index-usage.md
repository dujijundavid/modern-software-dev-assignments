# PROJECT_INDEX 使用指南：Claude Code 如何理解你的项目

> 理解索引机制，让你的项目对 AI 更友好

## 核心概念

### 什么是 PROJECT_INDEX？

**传统方式**：
```
每次会话开始 → AI 读取整个代码库 → 58,000 tokens
```

**索引方式**：
```
预先生成索引 → AI 先读 PROJECT_INDEX (3,000 tokens) → 按需深入特定文件
```

**效果**：**94% token 节省**

---

## 索引的数据结构设计

你的 [PROJECT_INDEX.json](../../PROJECT_INDEX.json) 采用**分层信息架构**：

```yaml
metadata:              # 元数据层 - 项目身份
  project_name         # CS146S: Modern Software Developer
  token_efficiency     # ROI 量化展示
  index_version        # 版本控制

project_structure:     # 结构层 - 项目组织
  weeks: []           # 按周组织的课程递进
  learning_notes: {}  # 知识沉淀
  claude_config: {}   # AI 配置入口点

tech_stack:           # 技术栈层 - 技术决策
  languages           # Python 3.10+
  frameworks          # FastAPI, SQLAlchemy
  llm                 # Ollama, OpenAI
  testing             # pytest, httpx

skills_pyramid:       # 能力金字塔 - 学习目标
  level_1: 基础技能
  level_2: 协作技能
  level_3: 系统设计

quick_commands:       # 快速命令 - 常用操作
navigation:           # 导航指南 - AI 使用提示
key_resources:        # 资源链接 - 内外部资源
```

### 设计原则

| 原则 | 说明 | 示例 |
|------|------|------|
| **渐进式揭示** | 从概览到细节 | metadata → structure → files |
| **多维度索引** | 按周、技能、技术栈 | 同一内容多种访问路径 |
| **机器+人类** | JSON + MD 双格式 | AI 读 JSON，人类读 MD |
| **可扩展性** | 易于添加新字段 | 不破坏现有结构 |

---

## AI 读取索引的认知流程

```
┌─────────────────────────────────────────────────────────────┐
│ 1. 元数据识别 (metadata)                                      │
│    ├─ project_name → 理解项目类型：教育课程                   │
│    ├─ institution → 了解背景：斯坦福大学                      │
│    └─ token_efficiency → 理解索引策略的价值                   │
├─────────────────────────────────────────────────────────────┤
│ 2. 技术栈匹配 (tech_stack)                                   │
│    ├─ Backend: FastAPI → 激活 fastapi-expert                 │
│    ├─ LLM: Ollama → 激活 ml-data-expert                     │
│    ├─ Testing: pytest → 激活 python-testing-expert           │
│    └─ Code Quality: black, ruff → 了解代码风格               │
├─────────────────────────────────────────────────────────────┤
│ 3. 结构映射 (project_structure.weeks)                        │
│    ├─ Week 1: Prompt Engineering → 理解课程起点              │
│    ├─ Week 2: LLM-Powered Apps → 找到主要实现                │
│    └─ week2/app/services/ → 定位核心代码                     │
├─────────────────────────────────────────────────────────────┤
│ 4. 关键文件定位 (key_files)                                  │
│    ├─ app/main.py → API 入口点                              │
│    ├─ app/services/extract.py → 核心服务                    │
│    └─ tests/test_extract.py → 测试覆盖                      │
├─────────────────────────────────────────────────────────────┤
│ 5. 上下文触发 (navigation.for_ai_agents)                     │
│    ├─ Read PROJECT_INDEX.md → 获取结构概览                   │
│    ├─ Use /week → 获取周特定上下文                          │
│    ├─ Use code-reviewer → 提交前审查                         │
│    └─ Use /test-week → 运行测试                             │
└─────────────────────────────────────────────────────────────┘
```

### 认知负载对比

```
无索引：
  认知负载 = O(n²) 需要理解所有文件间的关系
  Token 使用 = 58,000 tokens/会话

有索引：
  认知负载 = O(n) 先理解结构，按需深入
  Token 使用 = 3,000 tokens/会话
```

---

## 索引在 AI 工作流中的实际应用

### 场景 1：用户说 "帮我测试 week2"

```
AI 的思考过程：
├─ 1. 读取 PROJECT_INDEX.json
│      └─ 发现: week2 技术栈是 FastAPI + pytest
├─ 2. 查找 week2 测试配置
│      └─ tests: week2/tests/
│      └─ coverage: 85%
├─ 3. 激活 python-testing-expert
│      └─ 专门处理 pytest 测试
├─ 4. 运行测试命令
│      └─ pytest week2/tests/
└─ 5. 分析结果并提供建议
```

### 场景 2：用户说 "实现一个新端点"

```
AI 的思考过程：
├─ 1. 读取 PROJECT_INDEX.json
│      └─ 发现: FastAPI 项目，routers 在 app/routers/
├─ 2. 查找项目模式
│      └─ API Structure: routers/ + services/
├─ 3. 激活 fastapi-expert
│      └─ 专门处理 FastAPI 开发
├─ 4. 按照项目模式创建文件
│      ├─ app/routers/new_endpoint.py
│      └─ app/services/new_service.py
└─ 5. 更新索引（如果需要）
```

### 场景 3：用户说 "为什么我的测试失败了"

```
AI 的思考过程：
├─ 1. 读取 PROJECT_INDEX.json
│      └─ 发现: 使用 httpx TestClient
├─ 2. 查找测试指南
│      └─ learning_notes/week2/testing_llm_functions_guide.md
├─ 3. 激活 python-testing-expert
│      └─ 专门处理测试问题
├─ 4. 读取失败测试
│      └─ 分析错误模式
└─ 5. 提供针对性解决方案
```

---

## 创建有效索引的准则

### 1. 元数据层：建立项目身份

```json
"metadata": {
  "project_name": "项目名称",
  "purpose": "项目目的（一句话）",
  "tech_stack_primary": "主要技术栈",
  "generated_at": "生成时间",
  "index_version": "索引版本"
}
```

**关键点**：
- 项目名称要具体
- 目的要简洁
- 包含生成时间（便于判断是否过期）

### 2. 结构层：描述项目组织

```json
"project_structure": {
  "directories": {
    "src/": "源代码",
    "tests/": "测试文件",
    "docs/": "文档"
  },
  "entry_points": {
    "cli": "bin/main.py",
    "api": "src/api/main.py",
    "web": "src/web/index.html"
  }
}
```

**关键点**：
- 按功能组织目录
- 明确入口点
- 包含关键文件路径

### 3. 技术栈层：列出技术决策

```json
"tech_stack": {
  "languages": {
    "python": ">=3.10"
  },
  "frameworks": {
    "backend": "FastAPI >=0.111.0"
  },
  "testing": {
    "framework": "pytest >=7.0.0",
    "http_client": "httpx >=0.24.0"
  }
}
```

**关键点**：
- 包含版本信息
- 按类别分组
- 列出主要和次要技术

### 4. 导航层：指导 AI 使用

```json
"navigation": {
  "for_ai_agents": [
    "Read PROJECT_INDEX.md first",
    "Use /week for week-specific context",
    "Use code-reviewer before commits"
  ],
  "quick_commands": {
    "test": "pytest tests/",
    "run": "python main.py",
    "format": "black ."
  }
}
```

**关键点**：
- 给出明确的执行顺序
- 提供常用命令
- 指定何时使用哪些子代理

---

## Token 效率的数学模型

### ROI 计算公式

```
Token_no_index = Sessions × Tokens_full_codebase
Token_with_index = Tokens_creation + Sessions × Tokens_index

盈亏平衡点：
Tokens_creation = Sessions × (Tokens_full - Tokens_index)
Sessions = Tokens_creation / (Tokens_full - Tokens_index)
```

### 你的项目数据

```
创建索引：2,000 tokens (一次性)
读取索引：3,000 tokens (每次会话)
完整代码：58,000 tokens (每次会话)

盈亏平衡：
Sessions = 2000 / (58000 - 3000)
         = 2000 / 55000
         = 0.036

结论：1 次会话即可收回成本！
```

### 长期收益

```
10 次会话：节省 550,000 tokens
100 次会话：节省 5,500,000 tokens
1000 次会话：节省 55,000,000 tokens
```

---

## 索引与 CLAUDE.md 的配合

### CLAUDE.md：行为指南

```markdown
## AI Team Assignments
| Task | Agent | Notes |
|------|-------|-------|
| FastAPI development | fastapi-expert | Primary for API work |
| Testing | python-testing-expert | Test structure |
```

**作用**：告诉 AI "使用哪个子代理"

### PROJECT_INDEX：结构指南

```json
"structure": {
  "backend": "week2/app/",
  "routers": "week2/app/routers/",
  "services": "week2/app/services/"
}
```

**作用**：告诉 AI "东西在哪里"

### 配合效果

```
用户："实现一个用户认证端点"

AI 的决策过程：
1. 读取 PROJECT_INDEX → 找到 week2/app/routers/
2. 读取 CLAUDE.md → 激活 fastapi-expert
3. 创建文件 → week2/app/routers/auth.py
4. 遵循模式 → routers + services 分层
```

---

## 维护和更新索引

### 何时更新索引

```yaml
触发条件：
  - 添加新模块/功能
  - 技术栈变更
  - 项目结构重组
  - 每周作业完成后

更新流程：
  1. 运行 /sc:index-repo
  2. 检查生成的索引
  3. 手动调整（如需要）
  4. 验证 JSON 格式
```

### 索引质量检查

```yaml
质量指标：
  - 文件大小：< 15KB (JSON), < 10KB (MD)
  - 完整性：所有关键路径已包含
  - 准确性：路径和版本号正确
  - 可读性：人类能够理解结构

验证命令：
  - cat PROJECT_INDEX.json | jq .  # JSON 格式检查
  - wc -l PROJECT_INDEX.md         # 大小检查
```

---

## 进阶技巧

### 1. 添加依赖关系图

```json
"dependency_graph": {
  "app/main.py": ["app/routers/", "app/services/"],
  "app/routers/extract.py": ["app/services/extract.py"],
  "app/services/extract.py": ["ollama", "pydantic"]
}
```

### 2. 添加 AI 代理映射

```json
"ai_persona_map": {
  "fastapi": ["fastapi-expert", "python-expert"],
  "testing": ["python-testing-expert"],
  "security": ["python-security-expert", "code-reviewer"]
}
```

### 3. 添加会话上下文（Serena MCP）

```json
"session_context": {
  "last_session": "2025-12-28",
  "current_week": 2,
  "in_progress": ["action items extraction"],
  "next_actions": ["improve test coverage"]
}
```

---

## 相关资源

- [Prompt Engineering 分析](../prompt-engineering/01-index-repo-analysis.md)
- [AI 工程原则](../prompt-engineering/02-ai-engineering-principles.md)
- [学习 Prompts 集合](../learning-prompts/README.md)