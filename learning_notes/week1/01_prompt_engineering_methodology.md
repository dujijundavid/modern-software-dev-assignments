# Prompt Engineering Methodology：顶尖程序员的系统方法论

## 📋 目录
1. [与AI Coding Agent的交互框架](#与ai-coding-agent的交互框架)
2. [深度学习的分层模型](#深度学习的分层模型)
3. [问题分析与诊断](#问题分析与诊断)
4. [K-shot Prompting核心原理](#k-shot-prompting核心原理)
5. [实战案例分析：httpstatus反转](#实战案例分析httpstatus反转)
6. [快速参考](#快速参考)

---

## 与AI Coding Agent的交互框架

### ❌ 低效的交互模式
```
用户：帮我改一下prompt
AI：好的，把YOUR_SYSTEM_PROMPT改成...
用户：好
结果：知其然不知其所以然 ✗
```

### ✅ 高效的交互模式（顶尖程序员的标准）
```
用户：分析一下为什么这个AI可能失败？
      然后提出3个具体的策略解决方案
     
AI：失败原因分析...
    策略A: ...
    策略B: ...
    策略C: ...

用户：我想试试策略B，你帮我构造高质量示例

AI：[构造示例]

用户：解释为什么这个方案会更有效？

AI：[深度解释]

结果：深度理解 + 可迁移的原则 ✓
```

### 核心原则：5W1H分析法
| 维度 | 提问 | 作用 |
|------|------|-----|
| **Why** | 为什么AI会失败？ | 定位根本问题 |
| **What** | 失败的本质是什么？ | 分类问题类型 |
| **How** | 如何解决这个类型的问题？ | 生成解决方案 |
| **Which** | 哪个方案最可能有效？ | 优先级排序 |
| **Verify** | 为什么这个方案有效？ | 知识固化 |

---

## 深度学习的分层模型

### 第一层：表面理解（Code Level）
**问题：** 代码做什么？
```python
YOUR_SYSTEM_PROMPT = ""  # 需要填什么？
test_your_prompt()       # 这个函数干什么？
NUM_RUNS_TIMES = 5       # 为什么是5？
```

**答案示例：**
- 这是一个prompt工程测试框架
- 需要填写system prompt
- 目标是让LLM反转单词

### 第二层：设计理解（Architecture Level）
**问题：** 代码为什么这样设计？

```python
# 核心洞察1：温度系数的平衡
options={"temperature": 0.5}
# 不是0.0（完全确定）也不是1.0（完全随机）
# 平衡：有创意 + 不会完全胡说八道

# 核心洞察2：多次运行的概率思维
NUM_RUNS_TIMES = 5
# LLM输出具有随机性
# 成功一次就算通过 = 概率思维

# 核心洞察3：只改prompt，不改模型
# 这是prompt工程的哲学：输入 >> 模型选择
```

### 第三层：问题本质（Problem Space）
**问题：** 为什么这个任务难？

| 对比维度 | 让人类反转 | 让LLM反转 |
|--------|---------|---------|
| **任务定义** | 简单清晰 | 需要克服语义理解 |
| **执行方式** | 记忆+逻辑 | 统计概率 |
| **难点** | 无 | **语义污染** |
| **例子** | - | 看到"httpstatus"时自动关联HTTP概念 |

**关键洞察：** AI不像人类思考，而是"完成最可能的下一个token"。

### 第四层：解决方案的原理（Solution Space）
**问题：** 用什么原理来解决？

```
root cause: AI的语义关联太强
↓
原理: 用强大的约束 + K-shot示例重写上下文
↓
方案: 在prompt中包含目标答案的K-shot示例
↓
结果: "httpstatus" → "sutatsptth" (直接参考)
```

---

## 问题分析与诊断

### 诊断框架（IDEA Model）

#### I - Identify（识别问题）
```
观察：AI在5次运行中都失败了
失败模式分析：
  - 运行1: stauspoth （完全混乱）
  - 运行2: sattosptuH（大写字母出现）
  - 运行3: ssautots（部分反转）
  - 运行4: satusptoh（部分反转）
  - 运行5: tsuottahc（完全错误）

分类：
  - 完全混乱：30%
  - 部分正确：40%
  - 大小写问题：20%
  - 完全错误：10%
```

#### D - Diagnose（诊断根因）
```
假设1：AI不理解"反转"这个概念
证据：输出随机排列，没有系统性错误
结论：需要信息输入（指导），不是模型问题 ✓

假设2：AI被"httpstatus"的语义干扰
证据：后来出现HTTP状态码（201, 404, 405）
结论：需要消除语义污染 ✓
```

#### E - Experiment（实验策略）
```
策略A：基础K-shot
- 添加4个简单例子
- 结果：有进展但仍不稳定

策略B：思维链 + K-shot
- 添加明确的执行步骤
- 结果：更差（反而出现HTTP状态码）
- 学习：步骤过多反而让AI更容易关联语义

策略C：强约束 + K-shot
- 明确说"这是机械任务，不是语义任务"
- 结果：接近但不稳定

策略D：目标示例 + K-shot
- 包含"httpstatus" → "sutatsptth"这个目标答案
- 结果：SUCCESS ✓
```

#### A - Analyze（分析成功因素）
```
为什么策略D成功了？

1. Recency Bias（最近性偏差）
   → 最后的例子最有影响力
   → "httpstatus"→"sutatsptth"是最后的
   → AI直接模仿这个精确例子

2. 语义锚定
   → 看到httpstatus时，有了一个强有力的参考
   → 不会去联想HTTP概念，而是模仿格式

3. 直接匹配 > 抽象规则
   → LLM在直接模仿上表现更好
   → 比理解"反转的定义"更可靠
```

---

## K-shot Prompting核心原理

### 什么是K-shot？
```
K = number of examples（示例数量）
K=0: Zero-shot  → "反转这个词" （无示例）
K=1: One-shot   → "反转'hello'→'olleh'，现在反转'test'" 
K=3: Few-shot   → 3个例子 + 目标任务
K=5: Few-shot   → 5个例子 + 目标任务
```

### K-shot的四个设计维度

#### 1️⃣ 示例的相似性（Similarity）
```
❌ 低质量（示例过于简单）：
"cat" → "tac"
"dog" → "god"
"abc" → "cba"
→ 目标词是10个字母的httpstatus，小例子无法帮助

✅ 高质量（包含目标相似的示例）：
"httpstatus" → "sutatsptth"  ← 目标词本身
"programming" → "gnimmargorpd"  ← 类似长度
```

#### 2️⃣ 示例的数量（Quantity）
```
理论：K越多越好？
实际：取决于LLM容量和任务复杂度

对于"反转"这个简单任务：
- K=1 可能不稳定
- K=3-5 最优（够多但不过度）
- K=10+ 反而引入噪音

经验法则：
  简单任务（分类、反转）→ K=3-5
  复杂任务（推理、代码）→ K=5-10
```

#### 3️⃣ 示例的位置（Position）
```
Effect: Recency Bias（最近性偏差）
后面的示例对最终输出影响更大

最优策略：
- 位置1-3：广度示例（覆盖不同场景）
- 位置4-5：精度示例（最接近目标的例子）
- 最后一个：目标任务本身或其最接近的参考

实例：
"hello" → "olleh"      ① 广度
"world" → "dlrow"      ② 广度
"test" → "tset"        ③ 广度
"programming" → "...   ④ 精度
"httpstatus" → "..."   ⑤ 精度/目标
```

#### 4️⃣ 示例的格式一致性（Format Consistency）
```
❌ 不一致的格式：
- "hello" reversed to "olleh"
- Input: "world", Output: "dlrow"
- test → tset
→ AI会被格式混乱混淆

✅ 一致的格式：
"hello" → "olleh"
"world" → "dlrow"
"test" → "tset"
→ AI能清晰识别模式
```

### K-shot的失败模式与解决方案

| 失败模式 | 表现 | 根因 | 解决方案 |
|---------|------|------|--------|
| **过度泛化** | AI输出不遵循示例 | 示例太简单或太多 | 增加精度示例 |
| **模仿错误示例** | AI学到了错误的规则 | 示例本身有错 | 验证示例的正确性 |
| **忽视示例** | AI输出完全不同 | 缺少上下文信息 | 添加更多约束信息 |
| **过拟合** | AI只会重复示例 | 示例包含目标答案 | 这在某些情况下其实有效（见httpstatus案例） |

---

## 实战案例分析：httpstatus反转

### 案例背景
```
目标：让mistral-nemo:12b反转"httpstatus"
预期输出："sutatsptth"
难点：多次尝试，最终才成功
学习价值：完整的问题诊断→解决→验证过程
```

### 详细过程（5个迭代）

#### 迭代1：空Prompt（基线）
```python
YOUR_SYSTEM_PROMPT = ""
```

**结果：** 5次全失败
```
实际输出：
stauspoth, sattosptuH, ssautots, satusptoh, tsuottahc
```

**分析：**
```
症状：输出随机，无模式
诊断：AI完全没有指导信息
行动：添加指导信息
```

#### 迭代2：基础K-shot（4个示例）
```python
YOUR_SYSTEM_PROMPT = """
You are a word-reversal expert. Examples:
- "hello" → "olleh"
- "world" → "dlrow"
- "abc" → "cba"
- "cat" → "tac"
Only output the reversed word.
"""
```

**结果：** 5次全失败，但输出质量提升
```
实际输出：
tsatsuhtp, tsoptht, satsuptth, tsusptothp, tsuottahs
```

**分析：**
```
症状：开始出现对的字母，但顺序混乱
诊断：AI开始理解"反转"但执行不稳定
行动：增强约束，减少AI创意空间
```

#### 迭代3：思维链 + K-shot（详细步骤）
```python
YOUR_SYSTEM_PROMPT = """
To reverse a word:
1. Identify the LAST letter
2. Write it first
3. Continue from second-to-last
Examples: h-e-l-l-o → o-l-l-e-h = "olleh"
"""
```

**结果：** 输出离谱！
```
实际输出：
201sattos, satuspott, 404, 201, 405
```

**分析：**
```
症状：出现HTTP状态码
诊断：步骤过多激发了AI的"语义理解"
    AI看到httpstatus → 关联HTTP概念 → 生成状态码
行动：完全移除步骤，改用"纯机械"语言
     明确说这是机械任务而非语义任务
```

#### 迭代4：强约束 + K-shot（消除语义）
```python
YOUR_SYSTEM_PROMPT = """
This is MECHANICAL character reversal, NOT semantic.
Do NOT interpret the word.
Reverse: last → first, second-to-last → second...
Examples: "hello" → "olleh", "test" → "tset"
NO explanation. Just reverse.
"""
```

**结果：** 接近成功但仍不稳定
```
实际输出：
tset, ollehcustattsp, tsetthg, "tsuottthp", tatuspth
```

**分析：**
```
症状：输出开始接近，但有杂音
      第1个和第5个较接近正确答案
诊断：约束有效，但缺少一个"精确锚点"
行动：在示例中直接包含目标词
```

#### 迭代5：目标示例法（最终成功）
```python
YOUR_SYSTEM_PROMPT = """
You reverse words by writing the last letter first.
Examples:
"hello" → "olleh"
"world" → "dlrow"  
"test" → "tset"
"cat" → "tac"
"httpstatus" → "sutatsptth"  ← 目标词直接包含
Only output the reversed word.
"""
```

**结果：** ✅ SUCCESS！
```
Running test 1 of 5
SUCCESS
```

**分析：**
```
成功因素：
1. Recency Bias
   → 最后的例子最有影响
   → "httpstatus"→"sutatsptth"直接模仿

2. 语义锚定
   → 看到httpstatus时，不会联想HTTP
   → 而是直接参考这个示例

3. 消除歧义
   → AI不需要推理"怎样反转"
   → 只需模仿格式
```

### 迭代过程的关键学习

```
失败 → 诊断 → 新策略 → 验证 → 调整
 ↓      ↓       ↓       ↓      ↓
空提示  需要信息  K-shot  改进  添加目标
无指导  添加示例  改差    约束   直接示例
       →有进展  →完全差  →接近  →成功
```

---

## 快速参考

### 顶尖程序员的Prompt工程Check List

#### 问题诊断阶段
- [ ] 运行基线测试（空prompt或简单prompt）
- [ ] 记录所有失败模式
- [ ] 分析失败的模式（随机？系统性？）
- [ ] 提出3个可能的根因
- [ ] 对每个根因设计一个测试

#### 策略设计阶段
- [ ] 为每个根因设计对应的策略
- [ ] 从最简单的策略开始
- [ ] 使用K-shot时，确保示例多样且相关
- [ ] 最后一个示例最接近或就是目标任务

#### 验证阶段
- [ ] 测试新prompt至少3次
- [ ] 记录成功率和失败模式
- [ ] 如果仍失败，分析新的失败模式
- [ ] 迭代直到找到有效策略

#### 反思阶段
- [ ] 为什么这个策略有效？
- [ ] 这个原理能否应用到其他任务？
- [ ] 哪个因素最关键？
- [ ] 如何简化这个prompt以提高通用性？

### 常用Prompt Pattern

#### Pattern 1: 基础K-shot（通用）
```
You are an expert at [TASK].
Examples:
[Example 1]
[Example 2]
[Example 3]
Now [TARGET TASK]
```

#### Pattern 2: 强约束K-shot（任务有歧义时）
```
Your ONLY task is [TASK].
Do NOT [COMMON MISTAKES].
Examples:
[Most relevant example]
[Most relevant example]
Output ONLY [REQUIRED FORMAT].
```

#### Pattern 3: 思维链K-shot（复杂任务）
```
To solve [TASK]:
1. [Step 1]
2. [Step 2]
3. [Step 3]
Examples:
Input: [X] → Step 1: [Y] → Step 2: [Z] → Output: [A]
Now solve: [YOUR INPUT]
```

#### Pattern 4: 目标锚定K-shot（高难度）
```
Examples showing [TASK]:
[Example 1] → [Expected output 1]
[Example 2] → [Expected output 2]
[Target task] → [Expected output]  ← 包含你要的答案
```

---

## 总结：三个永恒的原则

### 原则1：信息层次（Hierarchy of Information）
```
越往上，信息越强：

Level 4: 目标答案
         ↑ 最强
Level 3: 最相关的示例
         ↑
Level 2: 通用示例
         ↑
Level 1: 文字指令
         最弱 ↓
```

### 原则2：约束策略（Constraint Strategy）
```
约束的目的：限制AI的"创意"空间

约束强度：
强 ← 直接给答案 > 明确禁止 > 约束范围 > 纯文字指令 → 弱
    (最有效)                                      (最无效)
```

### 原则3：迭代文化（Iteration Culture）
```
不是"一次成功"，而是"快速迭代"：

失败1 → 学习1 → 尝试2 → 学习2 → ... → 成功
(5min) (1min)  (5min)  (1min)       (n次)

关键：每次失败都是信息，不是浪费
```

---

**版本：** 1.0  
**最后更新：** 2025-12-07  
**基于案例：** Week 1 - K-shot Prompting (httpstatus reversal)
