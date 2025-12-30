# /sc:index-repo 提示词工程深度解析

> 分析 SuperClaude 的索引生成命令背后的 Prompt Engineering 原理

## 核心设计哲学

### 1. 问题-解决方案框架 (Problem-Solution Framework)

```markdown
## Problem Statement
**Before**: Reading all files → 58,000 tokens every session
**After**: Read PROJECT_INDEX.md → 3,000 tokens (94% reduction)
```

**Prompt Engineering 原理**：
- **量化价值主张**：用数字说话，建立可信度
- **Before/After 对比**：激活 AI 的"改进思维"
- **明确目标**：让 AI 知道"成功是什么样"

**应用模式**：
```markdown
## Problem Statement
**Current**: [描述当前低效状态，量化成本]
**Target**: [描述目标状态，量化改进]
**Impact**: [对用户的影响]
```

---

### 2. 分阶段执行流 (Phased Execution Flow)

```yaml
Phase 1: Analyze Repository Structure
  ↓ (5 parallel Glob searches)
Phase 2: Extract Metadata
  ↓ (entry points, modules, dependencies)
Phase 3: Generate Index
  ↓ (structured template)
Phase 4: Validation
  ↓ (quality checks)
```

**Prompt Engineering 原理**：

| 技术 | 作用 | 示例 |
|------|------|------|
| 任务分解 | 复杂任务 → 可管理步骤 | 4 个明确的阶段 |
| 并行执行提示 | 激活并发思维 | `5 concurrent Glob searches` |
| 验证门控 | 每阶段结束都有质量检查 | Phase 4: Validation |
| 流向清晰 | 用箭头表示数据流向 | `↓` 符号连接阶段 |

**应用模式**：
```yaml
## Execution Flow

### Phase {N}: {Phase Name}
**Objective**: [本阶段目标]
**Actions**:
  - [具体行动 1]
  - [具体行动 2]
**Output**: [期望产出]
**Validation**: [如何验证完成]

  ↓ (连接到下一阶段)

### Phase {N+1}: ...
```

---

### 3. 模板化输出 (Template-Based Output)

```markdown
## 📁 Project Structure
{tree view of main directories}

## 🚀 Entry Points
- CLI: {path} - {description}
- API: {path} - {description}

## 📦 Core Modules
### Module: {name}
- Path: {path}
- Exports: {list}
- Purpose: {1-line description}
```

**Prompt Engineering 原理**：

| 要素 | 作用 | 技巧 |
|------|------|------|
| 结构化模板 | 确保输出一致性 | 固定的 markdown 结构 |
| 占位符 | 明确告知需要填充什么 | `{path}`, `{name}` |
| 视觉层级 | 提高可读性 | emoji + 标题 + 缩进 |
| 约束条件 | 限制输出长度 | `{1-line description}` |

**应用模式**：
```markdown
## 📋 {Section Title}

### {Subsection}
- **Field**: `{placeholder}` - {constraint/hint}
- **Field**: `{placeholder}` - {constraint/hint}

### {Subsection}
For each {item}:
  - Attribute: `{value}`
  - Attribute: `{value}`
```

---

### 4. Token 效率的 ROI 计算

```markdown
**ROI Calculation**:
- Index creation: 2,000 tokens (one-time)
- Index reading: 3,000 tokens (every session)
- Full codebase read: 58,000 tokens (every session)

**Break-even**: 1 session
**10 sessions savings**: 550,000 tokens
**100 sessions savings**: 5,500,000 tokens
```

**Prompt Engineering 原理**：

| 组件 | 心理效应 | 技术目的 |
|------|----------|----------|
| ROI 计算 | 投资回报率可视化 | 让 AI 理解"为什么值得" |
| 复利效应 | 展示长期价值 | 强调一次性成本的合理性 |
| 盈亏平衡点 | 决策依据 | 给出明确的"何时值得"阈值 |
| 数字精确性 | 建立信任 | 具体数字比模糊描述更有说服力 |

**应用模式**：
```markdown
## Cost-Benefit Analysis

**Investment**:
- One-time cost: {tokens} tokens
- Per-session cost: {tokens} tokens

**Baseline (without solution)**:
- Per-session cost: {tokens} tokens

**Break-even Point**: {N} sessions

**Projected Savings**:
- {N} sessions: {tokens} tokens
- {N} sessions: {tokens} tokens
```

---

### 5. 模式匹配与 Glob 搜索策略

```yaml
1. Code Structure
   src/**/*.{ts,py,js,tsx,jsx}
   lib/**/*.{ts,py,js}

2. Documentation
   docs/**/*.md
   *.md (root level)
   README*.md

3. Configuration
   *.toml
   *.yaml, *.yml
   *.json (exclude package-lock, node_modules)
```

**Prompt Engineering 原理**：

| 技术 | 目的 | 示例 |
|------|------|------|
| 文件类型分类 | 按用途而非位置分组 | Code / Docs / Config |
| Glob 模式精确性 | 匹配特定文件类型 | `**/*.test.{ts,py,js}` |
| 排除模式 | 避免噪音 | `exclude package-lock` |
| 并行搜索提示 | 激活并发思维 | `5 concurrent` |

**常用 Glob 模式参考**：
```yaml
代码文件:
  - "**/*.{ts,tsx,js,jsx}"       # 所有 JS/TS 文件
  - "**/*.test.{ts,py}"          # 测试文件
  - "src/**/*.py"                # 特定目录

文档文件:
  - "**/*.md"                    # 所有 Markdown
  - "docs/**/*.md"               # 特定目录
  - "{README,CONTRIBUTING}.md"   # 特定文件名

配置文件:
  - "*.{toml,yaml,yml,json}"     # 所有配置
  - ".env*"                      # 环境配置
  - "package.json"               # 特定文件

排除模式:
  - "node_modules/**"            # 排除依赖目录
  - "**/*.min.js"                # 排除压缩文件
  - "**/{package-lock, yarn.lock}"  # 排除锁文件
```

---

### 6. 质量检查清单 (Validation Checklist)

```markdown
### Phase 4: Validation

Quality checks:
- [ ] All entry points identified?
- [ ] Core modules documented?
- [ ] Index size < 5KB?
- [ ] Human-readable format?
```

**Prompt Engineering 原理**：

| 要素 | 作用 |
|------|------|
| 自我验证触发 | 让 AI 审查自己的输出 |
| 约束明确 | `< 5KB` 可量化指标 |
| 用户视角 | `Human-readable` 提醒最终受众 |
| 二元选择 | `[ ]` 清晰的是/否检查 |

**应用模式**：
```markdown
## Quality Validation

**Completeness Checks**:
- [ ] {检查项 1}
- [ ] {检查项 2}

**Quality Checks**:
- [ ] {质量标准 1} (阈值: {value})
- [ ] {质量标准 2} (阈值: {value})

**Usability Checks**:
- [ ] {用户视角检查}
- [ ] {用户视角检查}
```

---

## Prompt Engineering 的分层思维

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: 元指令 (Persona Instructions)                       │
│         "你是一个..." "你的任务是..."                            │
│         目的: 建立 AI 的角色认知                               │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: 结构化指令 (Structured Instructions)                 │
│         Phase 1 → Phase 2 → Phase 3                        │
│         目的: 定义执行流程                                     │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: 模板指令 (Template Instructions)                     │
│         {field} 填充具体内容                                  │
│         目的: 确保输出格式一致性                               │
├─────────────────────────────────────────────────────────────┤
│ Layer 4: 验证指令 (Validation Instructions)                   │
│         检查清单 [ ] [ ] [ ]                                  │
│         目的: 激发自我审查                                    │
└─────────────────────────────────────────────────────────────┘
```

### 设计流程（从下往上）

```
1. 定义输出模板 (Layer 3)
   ↓
   "我想要什么样的输出？"
   - 设计 markdown 结构
   - 定义占位符
   - 添加视觉层级

2. 定义执行步骤 (Layer 2)
   ↓
   "如何生成这个输出？"
   - 分解任务
   - 定义阶段
   - 添加验证

3. 定义角色认知 (Layer 1)
   ↓
   "谁最适合执行这个任务？"
   - 选择合适的 persona
   - 定义行为模式
   - 设置约束条件

4. 添加验证机制 (Layer 4)
   ↓
   "如何确保质量？"
   - 添加检查清单
   - 定义质量标准
   - 设置验证触发器
```

---

## 实战模板：创建自定义索引命令

### 模板：每周作业索引生成器

```markdown
---
name: index-week
description: Generate weekly assignment index with status tracking
---

# Week Index Generator

## Problem Statement
**Current**: Need to manually check assignment status across weeks
**Target**: Auto-generated week index with completion tracking
**Impact**: Save time, ensure consistent format

## Execution Flow

### Phase 1: Week Detection
**Objective**: Identify current week context
**Actions**:
  - Read current directory structure
  - Detect week number (week1/, week2/, ...)
  - Load week-specific requirements from docs/

**Output**: Week number, theme, key files

**Validation**:
- [ ] Week directory exists?
- [ ] Week README/requirements found?

### Phase 2: Status Analysis
**Objective**: Analyze completion status
**Actions**:
  - Check for main implementation files
  - Run test coverage analysis
  - Check for learning notes
  - Identify missing components

**Output**: Status metrics (coverage %, completion %)

**Validation**:
- [ ] All key files checked?
- [ ] Test coverage calculated?

### Phase 3: Generate Index
**Objective**: Create structured index file
**Actions**:
  - Create WEEK_INDEX.md with template below
  - Create WEEK_STATUS.json for machine reading

**Template**:
```markdown
# Week {N}: {Theme}

## Status Summary
- Completion: {percentage}%
- Test Coverage: {percentage}%
- Learning Notes: {yes/no}

## Key Files
- Implementation: {path}
- Tests: {path}
- Learning Notes: {path}

## Next Actions
1. {action 1}
2. {action 2}
```

**Validation**:
- [ ] Index file created?
- [ ] All placeholders filled?
- [ ] Format consistent?

### Phase 4: Quality Check
**Objective**: Ensure index is useful
**Actions**:
  - Verify index size < 3KB
  - Check all paths are valid
  - Confirm human-readable format

**Validation**:
- [ ] Index size OK?
- [ ] All paths valid?
- [ ] Ready for AI consumption?
```

---

## 关键要点总结

1. **量化价值**：始终用数字说明"为什么值得"
2. **分阶段执行**：复杂任务分解为可管理的步骤
3. **模板化输出**：确保输出一致性和可解析性
4. **验证门控**：每个阶段结束都进行质量检查
5. **并行执行**：提示 AI 可以并行处理独立任务
6. **用户视角**：最终输出必须对人类和机器都友好

---

## 相关资源

- [PROJECT_INDEX 使用指南](../project-patterns/01-project-index-usage.md)
- [AI 工程原则](../prompt-engineering/02-ai-engineering-principles.md)
- [学习 Prompts 集合](../learning-prompts/README.md)
