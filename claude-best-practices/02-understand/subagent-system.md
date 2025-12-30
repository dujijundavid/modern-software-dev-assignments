# Claude Code 子代理系统：专业化协作架构

> 理解主代理与子代理的关系，高效利用专业化 AI 助手

---

## 一、子代理与主代理的关系

### 1.1 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                     主代理 (Main Agent)                      │
│                   编排者 + 路由器 + 协调者                    │
│                                                              │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐  │
│  │  任务路由   │  上下文管理 │  质量门控   │  最终决策   │  │
│  └─────────────┴─────────────┴─────────────┴─────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   ┌─────────┐      ┌──────────┐     ┌─────────────┐
   │FastAPI  │      │Testing   │     │Code Review  │
   │Expert   │      │Expert    │     │Gateway      │
   └─────────┘      └──────────┘     └─────────────┘
        │                 │                 │
        ▼                 ▼                 ▼
   ┌─────────┐      ┌──────────┐     ┌─────────────┐
   │Python   │      │Security  │     │Performance  │
   │Expert   │      │Expert    │     │Optimizer    │
   └─────────┘      └──────────┘     └─────────────┘
```

### 1.2 角色对比

| 维度 | 主代理 | 子代理 |
|------|--------|--------|
| **定位** | 编排者和路由器 | 领域专家 |
| **权限** | 最终决策权 | 域内自主执行 |
| **职责** | 任务分解、协调、质量控制 | 专项任务执行 |
| **上下文** | 维护全局上下文 | 继承主代理目标 |
| **激活方式** | 始终运行 | 按需激活 |

### 1.3 交互模式

```yaml
# 标准委托流程
User Request → Main Agent
    ↓
    ├─ 分析任务类型
    ├─ 选择合适的子代理
    ├─ 委托任务 + 上下文
    │
    ├─► Subagent (专业执行)
    │       │
    │       └─► Result + Status
    │
    ├─ 评估结果
    ├─ 质量检查
    └─ 返回用户
```

---

## 二、何时使用子代理

### 2.1 强制使用场景 (MUST USE)

| 场景 | 子代理 | 触发条件 |
|------|--------|----------|
| **代码审查** | `code-reviewer` | 每次提交前必须运行 |
| **性能问题** | `performance-optimizer` | 系统缓慢、高成本、扩展问题 |
| **代码库探索** | `code-archaeologist` | 分析不熟悉或遗留代码 |
| **文档更新** | `documentation-specialist` | README、API 文档、指南 |

### 2.2 框架特定场景

| 任务类型 | 子代理 | 示例 |
|----------|--------|------|
| **FastAPI 开发** | `fastapi-expert` | API 端点、路由器、中间件 |
| **Python 后端** | `python-expert` | Python 特定任务（非 FastAPI） |
| **测试改进** | `python-testing-expert` | 测试结构、fixtures、覆盖率 |
| **安全分析** | `python-security-expert` | SQL 注入、XSS、认证漏洞 |

### 2.3 主动使用场景 (PROACTIVE)

```yaml
# 复杂任务自动分解
User: "实现一个用户认证系统"
    ↓
PM Agent → tech-lead-orchestrator (规划)
    → api-architect (API 设计)
    → fastapi-expert (后端实现)
    → python-security-expert (安全审查)
    → python-testing-expert (测试)
    → code-reviewer (最终审查)
```

### 2.4 决策树

```
用户请求
    │
    ├─ 是否需要代码变更？
    │   ├─ 是 → 是否涉及安全？
    │   │   ├─ 是 → python-security-expert
    │   │   └─ 否 → 框架特定专家
    │   │       ├─ FastAPI → fastapi-expert
    │   │       ├─ Django → django-expert
    │   │       └─ 通用 Python → python-expert
    │   │
    │   └─ 否 → 继续判断
    │
    ├─ 是否需要测试？
    │   └─ 是 → python-testing-expert
    │
    ├─ 是否需要文档？
    │   └─ 是 → documentation-specialist
    │
    ├─ 是否需要性能优化？
    │   └─ 是 → performance-optimizer
    │
    ├─ 是否需要探索代码？
    │   └─ 是 → code-archaeologist
    │
    └─ 通用任务 → 主代理直接处理
```

---

## 三、你的项目 AI 团队配置

### 3.1 完整团队清单

| 子代理 | 领域 | 优先级 | 关键文件 |
|--------|------|--------|----------|
| **fastapi-expert** | FastAPI 框架 | 最高 | `week2/app/routers/`, `week2/app/services/` |
| **python-expert** | Python 通用 | 高 | 所有 `.py` 文件 |
| **python-testing-expert** | pytest 测试 | 高 | `tests/`, `**/test_*.py` |
| **python-security-expert** | 安全漏洞 | 高 | 认证、数据库、输入验证 |
| **code-reviewer** | 代码审查 | **必须** | 所有提交 |
| **performance-optimizer** | 性能优化 | 按需 | 缓慢的 API、查询 |
| **code-archaeologist** | 代码分析 | 探索时 | 遗留代码、新模块 |
| **api-architect** | API 设计 | 设计时 | 新端点、版本控制 |
| **frontend-developer** | 前端开发 | 按需 | `week2/app/static/`, HTML/CSS/JS |
| **ml-data-expert** | LLM 集成 | 按需 | `week2/app/services/extract.py` |

### 3.2 技术栈映射

```yaml
Backend Framework:
  FastAPI → fastapi-expert (首选) > python-expert

Database:
  SQLite + SQLAlchemy → python-expert > django-orm-expert

Testing:
  pytest + httpx → python-testing-expert

LLM Integration:
  Ollama + OpenAI → ml-data-expert > python-expert

Code Quality:
  Black + Ruff → code-reviewer (强制)

Frontend:
  Vanilla JS + HTML/CSS → frontend-developer
```

### 3.3 每周作业工作流

```
周作业开发流程
    │
    ├─► 1. code-archaeologist (了解当前状态)
    │       └─ "分析本周代码结构和现有模式"
    │
    ├─► 2. fastapi-expert 或 python-expert (设计方案)
    │       └─ "根据项目架构设计实现"
    │
    ├─► 3. 对应专家 (实现)
    │       ├─ fastapi-expert (API 端点)
    │       ├─ python-expert (业务逻辑)
    │       ├─ frontend-developer (UI 更新)
    │       └─ ml-data-expert (LLM 集成)
    │
    ├─► 4. python-testing-expert (测试)
    │       └─ "编写和改进测试"
    │
    └─► 5. code-reviewer (审查) ← 提交前必做
            └─ "安全、性能、质量检查"
```

---

## 四、子代理协作模式

### 4.1 顺序协作

```yaml
# 典型的功能开发流程
用户: "添加一个 notes API 端点"

Phase 1 - Exploration:
  agent: code-archaeologist
  output: 现有代码结构分析
    ↓
Phase 2 - Design:
  agent: api-architect
  input: 探索结果
  output: API 契约设计
    ↓
Phase 3 - Implementation:
  agent: fastapi-expert
  input: API 设计
  output: 实现代码
    ↓
Phase 4 - Testing:
  agent: python-testing-expert
  input: 实现代码
  output: 测试套件
    ↓
Phase 5 - Review:
  agent: code-reviewer
  input: 代码 + 测试
  output: 审查报告
    ↓
Done: 提交代码
```

### 4.2 并行协作

```yaml
# 多模块同时开发
用户: "实现一个完整的 CRUD 功能"

PM Agent → Spawn:
    ├─► api-architect (API 契约设计)
    │
    ├─► fastapi-expert (后端实现)
    │
    ├─► frontend-developer (UI 组件)
    │
    └─► python-testing-expert (测试框架)

所有子代理并行工作 → 最终由 code-reviewer 整合
```

### 4.3 Handoff 模式

```python
# 配置中的 handoff 规则
delegation_rules = {
    "trigger": "API design needed",
    "target": "api-architect",
    "handoff_message": "Backend logic ready. Need API endpoints for: {functionality}",

    # api-architect 完成后
    "next_agent": "fastapi-expert",
    "next_message": "API contract designed. Implement endpoints.",
    "context": ["api_spec", "data_models"]
}
```

### 4.4 协调机制

| 机制 | 说明 | 实现 |
|------|------|------|
| **上下文共享** | 代理链中保持上下文 | 继承主代理状态 |
| **状态报告** | 定期向协调代理更新 | 输出进度日志 |
| **共识检查** | 关键决策与主代理确认 | `AskUserQuestion` |
| **代码审查门** | 提交前必须通过审查 | `code-reviewer` |

---

## 五、定义新的子代理

### 5.1 配置结构

```yaml
# CLAUDE.md 中的子代理定义
custom_agents:
  <agent-name>:
    # 1. 描述：明确领域专长
    description: "专家...领域的专业代理"

    # 2. 强制使用标志
    must_use: true/false

    # 3. 代理类型
    type: specialist | orchestrator | reviewer

    # 4. 工具权限
    tools: [Read, Write, Edit, Bash, Grep, Glob, ...]

    # 5. 委托触发器
    delegation_rules:
      - trigger: "任务类型描述"
        target: target-agent
        handoff: "上下文传递消息"

    # 6. 输出格式
    output_format: structured | freeform
```

### 5.2 实际示例：你的配置

```yaml
# 从 CLAUDE.md 提取的真实配置
fastapi-expert:
  description: "Expert FastAPI spécialisé dans les APIs modernes hautes performances"
  must_use: true
  tools: [Read, Write, Edit, MultiEdit, Bash, Grep, Glob, LS]
  delegation_rules:
    - trigger: "API endpoints needed"
      target: self
    - trigger: "Backend development"
      target: python-expert  # 链式委托

python-testing-expert:
  description: "Specialized agent for Python testing, test automation, quality assurance"
  must_use: true
  tools: [All tools]
  delegation_rules:
    - trigger: "Test coverage low"
      target: self
    - trigger: "pytest improvements"
      target: self
```

### 5.3 创建步骤

```yaml
Step 1: 定义需求
  - 需要什么专业知识？
  - 与现有代理的区别？
  - 使用频率？

Step 2: 编写描述
  - 清晰的领域定义
  - 工具权限范围
  - 输出格式要求

Step 3: 设置触发器
  - 什么情况下激活？
  - 从谁接收任务？
  - 完成后交给谁？

Step 4: 测试代理
  - 使用显式调用测试
  - 验证输出质量
  - 调整触发条件

Step 5: 集成到工作流
  - 更新 CLAUDE.md
  - 添加到决策树
  - 记录使用模式
```

---

## 六、最佳实践

### 6.1 使用原则

| 原则 | 说明 | 反例 |
|------|------|------|
| **专业化优先** | 使用领域专家而非通用代理 | 用 `python-expert` 处理 FastAPI 任务 |
| **强制审查** | 所有代码变更必须审查 | 跳过 `code-reviewer` 直接提交 |
| **按需激活** | 只在需要时激活子代理 | 简单任务也调用多个子代理 |
| **上下文保持** | 委托时传递完整上下文 | 让子代理从头分析代码 |

### 6.2 性能优化

```yaml
Token 优化:
  - 避免不必要的子代理切换
  - 批量相关任务给同一子代理
  - 复用子代理的分析结果

质量优化:
  - 强制使用 code-reviewer
  - 关键任务使用专业子代理
  - 交叉验证（多个子代理审查）

效率优化:
  - 并行执行独立任务
  - 缓存子代理的输出
  - 建立常用工作流模式
```

### 6.3 常见陷阱

| 陷阱 | 问题 | 解决方案 |
|------|------|----------|
| **过度委托** | 简单任务也调用子代理 | 设置任务复杂度阈值 |
| **上下文丢失** | 子代理缺少必要信息 | 委托时传递完整上下文 |
| **代理冲突** | 多个子代理处理同一任务 | 明确代理边界和职责 |
| **循环依赖** | 子代理相互委托形成循环 | 设计单向依赖关系 |

### 6.4 调试技巧

```yaml
# 检查子代理调用
1. 查看日志中的 agent 切换
2. 验证上下文传递是否完整
3. 确认输出是否符合预期

# 优化子代理性能
1. 分析子代理的 Token 使用
2. 识别重复的分析工作
3. 建立结果缓存机制

# 改进子代理协作
1. 绘制代理协作图
2. 识别瓶颈和冗余
3. 优化委托顺序
```

---

## 七、进阶主题

### 7.1 子代理链模式

```yaml
# 多个子代理形成处理链
Request → Parser Agent → Validator Agent
    → Processor Agent → Formatter Agent → Response

每个子代理专注于单一职责
```

### 7.2 子代理池模式

```yaml
# 同类任务使用子代理池
Testing Pool:
  - python-testing-expert (单元测试)
  - integration-test-expert (集成测试)
  - e2e-test-expert (端到端测试)

PM Agent 根据任务类型选择合适的子代理
```

### 7.3 自适应代理选择

```yaml
# 基于历史表现选择子代理
1. 记录每个子代理的成功率
2. 分析任务类型与代理匹配度
3. 动态调整代理选择策略

示例：
  fastapi-expert 成功率: 95%
  python-expert 成功率: 80%
  → FastAPI 任务优先使用 fastapi-expert
```

---

## 八、实战案例

### 案例 1：实现新 API 端点

```yaml
User: "添加一个 /notes 端点"

执行流程:
1. PM Agent 识别为 FastAPI 任务
2. 委托给 fastapi-expert
3. fastapi-expert 创建:
   - app/routers/notes.py
   - app/services/notes_service.py
4. 委托给 python-testing-expert
5. 创建 tests/test_notes.py
6. 委托给 code-reviewer
7. 审查通过 → 提交

Token 成本: ~5,000
时间: ~5 分钟
质量: 高（专业子代理）
```

### 案例 2：性能问题排查

```yaml
User: "API 响应很慢"

执行流程:
1. PM Agent 识别为性能问题
2. 委托给 performance-optimizer
3. 分析数据库查询、缓存策略
4. 提供优化方案
5. 委托给 fastapi-expert 实现
6. 委托给 python-testing-expert 验证
7. 委托给 code-reviewer 审查

输出: 性能提升 3x
```

### 案例 3：安全审查

```yaml
User: "检查代码安全性"

执行流程:
1. PM Agent 识别为安全任务
2. 委托给 python-security-expert
3. 扫描常见漏洞:
   - SQL 注入
   - XSS
   - CSRF
   - 认证缺陷
4. 生成安全报告
5. 委托给 code-reviewer 最终确认

输出: 安全审查报告 + 修复建议
```

---

## 九、快速参考

### 9.1 子代理选择速查表

| 任务 | 首选子代理 | 备选子代理 |
|------|-----------|-----------|
| FastAPI 端点 | `fastapi-expert` | `python-expert` |
| Python 脚本 | `python-expert` | - |
| 测试编写 | `python-testing-expert` | - |
| 安全检查 | `python-security-expert` | `code-reviewer` |
| 性能优化 | `performance-optimizer` | - |
| 代码审查 | `code-reviewer` | - |
| 文档编写 | `documentation-specialist` | - |
| API 设计 | `api-architect` | `fastapi-expert` |
| 前端开发 | `frontend-developer` | - |
| LLM 集成 | `ml-data-expert` | `python-expert` |

### 9.2 工作流模板

```yaml
# 标准开发工作流
development_workflow:
  steps:
    - agent: code-archaeologist
      action: "探索现有代码"
    - agent: <framework>-expert
      action: "设计方案"
    - agent: <framework>-expert
      action: "实现功能"
    - agent: python-testing-expert
      action: "编写测试"
    - agent: code-reviewer
      action: "审查代码"

# 安全审查工作流
security_workflow:
  steps:
    - agent: python-security-expert
      action: "扫描漏洞"
    - agent: code-reviewer
      action: "确认修复"

# 性能优化工作流
performance_workflow:
  steps:
    - agent: performance-optimizer
      action: "分析瓶颈"
    - agent: <framework>-expert
      action: "实现优化"
    - agent: python-testing-expert
      action: "验证改进"
```

---

## 相关资源

- [PROJECT_INDEX 使用指南](01-project-index-usage.md)
- [SuperClaude 架构分析](../learning-prompts/superclaude-architecture-analysis.md)
- [CLAUDE.md 配置](../../CLAUDE.md)
- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
