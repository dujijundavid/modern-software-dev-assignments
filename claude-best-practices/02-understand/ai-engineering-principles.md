# AI Engineering 核心原则

> 成为更好的 AI Engineer 的关键洞察

---

## 一、认知负载理论

### 信息密度与理解成本

```
信息密度层级：
纯代码文件      = 100% 密度，需要逐行解析
摘要文档        = 20% 密度，可快速扫描
分层索引        = 5% 密度 + 指针，按需深入
```

### 设计原则

| 原则 | 说明 | 应用 |
|------|------|------|
| **渐进式揭示** | 从概览到细节 | Metadata → Structure → Details |
| **按需深入** | 只读需要的部分 | 先读索引，再读具体文件 |
| **多级缓存** | 避免重复计算 | PROJECT_INDEX 作为 L1 缓存 |

### 实践示例

```yaml
# 差的做法：一次性加载所有信息
"读取所有代码文件并分析..."

# 好的做法：渐进式加载
"1. 读取 PROJECT_INDEX 了解结构
 2. 定位相关文件
 3. 只读取需要的文件
 4. 按需深入更多文件"
```

---

## 二、Token 效率优化的数学原理

### 基本公式

```
Token Budget = Context Window - System Prompt - Input - Output
```

### 索引策略的数学模型

```
Cost_no_index = Sessions × Token_full_codebase
Cost_with_index = Token_creation + Sessions × Token_index

盈亏平衡点：
Token_creation = Sessions × (Token_full - Token_index)
Sessions = Token_creation / (Token_full - Token_index)
```

### 实际计算

```
你的项目：
- Token_full = 58,000
- Token_index = 3,000
- Token_creation = 2,000

Sessions = 2000 / (58000 - 3000)
         = 2000 / 55000
         ≈ 0.036

结论：1 次会话即可收回成本！
```

### 优化策略

| 策略 | 效果 | 适用场景 |
|------|------|----------|
| 创建索引 | 94% 节省 | 大型项目 |
| 分模块索引 | 按需加载 | 模块化项目 |
| 增量更新 | 减少重建 | 频繁变更 |
| 压缩冗余 | 减少噪音 | 文档多的项目 |

---

## 三、Prompt Engineering 分层思维

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: 元指令 (Persona)                                   │
│         "你是一个..." "你的任务是..."                            │
│         目的: 建立 AI 的角色认知                               │
│         验证: AI 是否表现出预期行为                           │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: 结构化指令 (Process)                                │
│         Phase 1 → Phase 2 → Phase 3                        │
│         目的: 定义执行流程                                     │
│         验证: AI 是否按步骤执行                               │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: 模板指令 (Output)                                   │
│         {field} 填充具体内容                                  │
│         目的: 确保输出格式一致性                               │
│         验证: 输出是否符合模板                                │
├─────────────────────────────────────────────────────────────┤
│ Layer 4: 验证指令 (Quality)                                  │
│         检查清单 [ ] [ ] [ ]                                  │
│         目的: 激发自我审查                                    │
│         验证: AI 是否检查自己的输出                           │
└─────────────────────────────────────────────────────────────┘
```

### 设计流程（从下往上）

```
1. 定义输出模板 (Layer 3)
   ↓
   问题："我想要什么样的输出？"
   - 设计 markdown/JSON 结构
   - 定义占位符
   - 添加视觉层级

2. 定义执行步骤 (Layer 2)
   ↓
   问题："如何生成这个输出？"
   - 分解任务
   - 定义阶段
   - 添加验证门控

3. 定义角色认知 (Layer 1)
   ↓
   问题："谁最适合执行这个任务？"
   - 选择合适的 persona
   - 定义行为模式
   - 设置约束条件

4. 添加验证机制 (Layer 4)
   ↓
   问题："如何确保质量？"
   - 添加检查清单
   - 定义质量标准
   - 设置验证触发器
```

---

## 四、验证驱动的 Prompt 设计

### 自我验证触发器

```markdown
## Quality Validation

**Completeness Checks**:
- [ ] All entry points identified?
- [ ] Core modules documented?

**Quality Checks**:
- [ ] Index size < 5KB?
- [ ] All paths are valid?

**Usability Checks**:
- [ ] Human-readable format?
- [ ] Machine-parseable format?
```

### 验证模式

| 模式 | 触发词 | 效果 |
|------|--------|------|
| **检查清单** | `[ ]` | 二元确认 |
| **阈值验证** | `< 5KB` | 可量化标准 |
| **存在性检查** | `All ...?` | 完整性验证 |
| **用户视角** | `Human-readable` | 可用性检查 |

### 实践示例

```yaml
# 差的做法：没有验证
"创建一个索引文件"

# 好的做法：带验证
"创建一个索引文件，然后检查：
 - [ ] 文件大小 < 5KB
 - [ ] 所有关键路径已包含
 - [ ] 格式符合 JSON 规范
 - [ ] 人类可读"
```

---

## 五、并行执行模式

### 激活并发思维

```markdown
**Parallel analysis** (5 concurrent Glob searches):

1. Code Structure: src/**/*.py
2. Documentation: docs/**/*.md
3. Configuration: *.{toml,yaml,json}
4. Tests: tests/**/*.py
5. Scripts: scripts/**/*
```

### 并行模式设计

| 要素 | 作用 | 示例 |
|------|------|------|
| **数量明确** | 告知并行度 | `5 concurrent` |
| **任务独立** | 确保可并行 | 5 个独立的 Glob |
| **结果合并** | 指定合并方式 | `Extract metadata` |
| **同步点** | 定义等待点 | `Phase 2` 合并结果 |

### 实践示例

```yaml
# 差的做法：顺序执行
"1. 读取 src/
 2. 读取 tests/
 3. 读取 docs/"

# 好的做法：并行执行
"并行读取（3个并发）：
 - src/**/*.py
 - tests/**/*.py
 - docs/**/*.md
然后合并结果"
```

---

## 六、ROI 量化的说服力

### 数字的力量

```markdown
**ROI Calculation**:
- Index creation: 2,000 tokens (one-time)
- Index reading: 3,000 tokens (every session)
- Full codebase read: 58,000 tokens (every session)

**Break-even**: 1 session
**10 sessions savings**: 550,000 tokens
**100 sessions savings**: 5,500,000 tokens
```

### ROI 模板

```markdown
## Cost-Benefit Analysis

**Investment**:
- One-time: {tokens} tokens
- Per-session: {tokens} tokens

**Baseline**:
- Without solution: {tokens} tokens/session

**Break-even**: {N} sessions

**Projected Savings**:
- {N} sessions: {tokens} tokens
- {N} sessions: {tokens} tokens
```

### 为什么有效

| 心理效应 | 技术目的 |
|----------|----------|
| 投资回报率可视化 | 让 AI 理解"为什么值得" |
| 复利效应 | 强调一次性成本的合理性 |
| 盈亏平衡点 | 给出明确的决策阈值 |
| 数字精确性 | 建立信任 |

---

## 七、问题-解决方案框架

### 结构模板

```markdown
## Problem Statement
**Current**: [描述当前低效状态，量化成本]
**Target**: [描述目标状态，量化改进]
**Impact**: [对用户的影响]

## Solution Approach
[详细说明解决方案]

## Expected Outcomes
- [定量指标 1]
- [定量指标 2]
```

### 实践示例

```markdown
## Problem Statement
**Current**: Reading all files → 58,000 tokens every session
**Target**: Read PROJECT_INDEX.md → 3,000 tokens (94% reduction)
**Impact**: Faster context loading, lower costs
```

---

## 八、模板化输出的约束设计

### 占位符设计

| 类型 | 格式 | 约束 |
|------|------|------|
| 自由文本 | `{field}` | 无约束 |
| 单行 | `{field} (1-line)` | 最多一行 |
| 列表 | `{list}` | 数组格式 |
| 路径 | `{path}` | 文件系统路径 |

### 约束技巧

```markdown
### Module: {name}
- Path: {path}                    # 自由文本
- Exports: {list}                 # 列表格式
- Purpose: {1-line description}   # 单行约束
- Dependencies: {optional}        # 可选字段
```

### 实践原则

1. **明确约束类型**：单行、列表、可选
2. **使用占位符**：`{field}` 清晰标记
3. **提供示例**：`{value} → 实际值`
4. **视觉区分**：用不同格式标记不同类型

---

## 九、上下文触发的导航设计

### AI 友好的导航指令

```json
"navigation": {
  "for_ai_agents": [
    "Read PROJECT_INDEX.md first for structure",
    "Use /week command for week-specific context",
    "Use code-reviewer agent before commits",
    "Use /test-week to run tests"
  ]
}
```

### 触发模式

| 触发条件 | 动作 | 目的 |
|----------|------|------|
| 会话开始 | Read PROJECT_INDEX | 建立结构认知 |
| 特定周任务 | Use /week | 获取周上下文 |
| 代码变更 | Use code-reviewer | 质量门控 |
| 测试需求 | Use /test-week | 执行测试 |

### 设计原则

1. **明确的触发条件**：何时做什么
2. **具体的动作**：调用哪个命令/代理
3. **预期效果**：为什么这样做

---

## 十、持续改进的反馈循环

### PDCA 循环在 Prompt Engineering 中

```yaml
Plan (计划):
  - 定义 Prompt 目标
  - 设计输出模板
  - 规划验证机制

Do (执行):
  - 运行 Prompt
  - 收集输出
  - 记录异常

Check (检查):
  - 对比预期与实际
  - 分析差异原因
  - 识别改进点

Act (改进):
  - 调整 Prompt
  - 更新模板
  - 优化验证
```

### 改进检查清单

```markdown
## Prompt Quality Checklist

**Clarity**:
- [ ] 目标明确？
- [ ] 约束清晰？
- [ ] 示例充分？

**Structure**:
- [ ] 逻辑分层？
- [ ] 步骤合理？
- [ ] 流程清晰？

**Validation**:
- [ ] 有验证机制？
- [ ] 质量标准明确？
- [ ] 错误处理完善？

**Efficiency**:
- [ ] Token 优化？
- [ ] 并行机会？
- [ ] 缓存策略？
```

---

## 实战检查清单

### 写 Prompt 前检查

```markdown
- [ ] 目标：AI 知道"成功是什么样"？
- [ ] 步骤：复杂任务是否分阶段？
- [ ] 输出：是否定义了期望格式？
- [ ] 验证：如何检查质量？
- [ ] ROI：是否量化了价值？
```

### 写 Prompt 后检查

```markdown
- [ ] 每层指令是否清晰？
- [ ] 占位符是否明确？
- [ ] 验证机制是否完善？
- [ ] 并行机会是否利用？
- [ ] Token 使用是否优化？
```

---

## 相关资源

- [索引生成分析](./01-index-repo-analysis.md)
- [PROJECT_INDEX 使用](../project-patterns/01-project-index-usage.md)
- [学习 Prompts](../learning-prompts/README.md)
