# Serena Advanced Patterns

Advanced usage patterns for Serena MCP memory system.

---

## Metadata

| 字段 | 值 |
|------|-----|
| **创建时间** | 2025-01-19 |
| **最后更新** | 2025-01-19 |
| **维护者** | AI Team |
| **状态** | Active |
| **相关记忆** | [MCP Server Best Practices](mcp_server_best_practices.md), [Code Patterns](code_patterns.md) |

---

## Advanced Pattern 1: Memory Hierarchy System

### Knowledge Graph Structure

```
Level 1 (Meta): Project Vision & Goals
    ↓ influences
Level 2 (Decisions): Architecture & Tech Stack
    ↓ guides
Level 3 (Implementation): Code Patterns & Workflows
    ↓ solves
Level 4 (Experience): Common Issues & Solutions
    ↓ tracks
Level 5 (Real-time): Session History & Progress
```

### Implementation

```markdown
# In architecture_decisions.md (Level 2)

## Decision: FastAPI Framework (2025-01-15)

**Rationale**: Async support, auto docs, type safety

**Impacts**:
- → Code patterns: Use async/await consistently
- → Testing: Use TestClient for async endpoints
- → LLM integration: Structured output with Pydantic

**Related Memories**:
- See: [code_patterns.md#async-patterns](../code_patterns.md#async)
- See: [llm_integration_patterns.md#pydantic](../llm_integration_patterns.md#pydantic)
```

---

## Advanced Pattern 2: Autonomous Memory Maintenance

### Self-Healing Memory System

```yaml
AI 自动维护任务:

每日任务:
  - 检查记忆过期状态
  - 更新 session_history.md
  - 同步最新代码模式

每周任务:
  - 分析记忆使用频率
  - 合并重复内容
  - 优化记忆链接

每月任务:
  - 评估记忆组织结构
  - 归档不活跃记忆
  - 重建记忆索引
```

### Implementation Pattern

```python
# AI 可以自动执行的维护逻辑

class MemoryMaintainer:
    async def check_freshness(self):
        """检查记忆新鲜度"""
        stale_memories = []
        for memory in await self.list_memories():
            last_update = memory.metadata.get("last_updated")
            if (datetime.now() - last_update).days > 30:
                stale_memories.append(memory.name)
        
        if stale_memories:
            return {
                "status": "needs_update",
                "memories": stale_memories,
                "action": "update_with_latest_context"
            }
        return {"status": "fresh"}
    
    async def detect_orphans(self):
        """检测孤立记忆（没有被引用）"""
        all_memories = set(await self.list_memories())
        referenced = set()
        
        for memory in await self.list_memories():
            content = await self.read_memory(memory)
            links = extract_memory_links(content)
            referenced.update(links)
        
        orphans = all_memories - referenced
        return orphans
```

---

## Advanced Pattern 3: Memory Versioning Strategy

### Semantic Versioning for Memories

```markdown
# 在记忆文件中使用版本标记

## Version: 2.1

**Changelog**:
- v2.1 (2025-01-19): 添加 MCP 服务器模式
- v2.0 (2025-01-10): 重组章节结构
- v1.0 (2025-01-01): 初始版本

## Content
...
```

### Git Workflow for Memories

```bash
# 策略: 主题分支 + 频繁提交

# 创建记忆主题分支
git checkout -b docs/update-mcp-patterns

# 小步提交，清晰历史
git add .serena/memories/mcp_server_best_practices.md
git commit -m "docs(mcp): 添加速率限制模式"

git add .serena/memories/mcp_server_best_practices.md
git commit -m "docs(mcp): 添加测试策略"

# 完成后合并
git checkout master
git merge docs/update-mcp-patterns
```

---

## Advanced Pattern 4: Multi-Project Memory Sharing

### Git Submodule Approach

```bash
# 创建共享记忆库
mkdir shared-serena-memories
cd shared-serena-memories
git init
echo "# Shared Best Practices" > .serena/memories/shared_patterns.md
git add .
git commit -m "Initial shared memory"
git remote add origin https://github.com/yourname/shared-serena-memories.git
git push -u origin master

# 在各个项目中使用
cd project-a
git submodule add https://github.com/yourname/shared-serena-memories.git .serena-shared
echo ".serena-shared/" >> .serena/.gitignore
git add .serena-shared .gitmodules .serena/.gitignore
git commit -m "feat: add shared Serena memories"
```

### Symbolic Link Approach (Alternative)

```bash
# 本地开发时使用符号链接
ln -s ~/shared-serena-memories/.serena/memories/shared_patterns.md \
      .serena/memories/shared_patterns.md

# 注意: .gitignore 应该忽略符号链接
echo ".serena/memories/shared_patterns.md" >> .gitignore
```

---

## Advanced Pattern 5: Intelligent Memory Retrieval

### Relevance Scoring Algorithm

```python
async def retrieve_relevant_memories(query: str, top_k: int = 3):
    """智能检索最相关的记忆"""
    
    memories = await list_memories()
    scores = {}
    
    for memory_name in memories:
        memory = await read_memory(memory_name)
        
        # 多维度评分
        score = 0
        
        # 1. 关键词匹配 (30%)
        keywords = extract_keywords(query)
        memory_keywords = extract_keywords(memory.content)
        score += jaccard_similarity(keywords, memory_keywords) * 0.3
        
        # 2. 语义相似度 (40%)
        score += semantic_similarity(query, memory.content) * 0.4
        
        # 3. 时间衰减 (20%)
        days_old = (now - memory.updated_at).days
        score += decay_factor(days_old) * 0.2
        
        # 4. 记忆类型权重 (10%)
        if "best_practices" in memory_name:
            score += 0.1
        
        scores[memory_name] = score
    
    # 返回 top-K
    sorted_memories = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_memories[:top_k]
```

---

## Advanced Pattern 6: Memory-Driven AI Behavior

### Dynamic Workflow Adaptation

```yaml
示例: 记忆驱动的测试策略

读取: development_workflow.md

if workflow.test_strategy == "tdd":
    AI 行为:
      - 优先编写测试
      - 使用 test-driven development
      - 保持高测试覆盖率
      
elif workflow.test_strategy == "integration_first":
    AI 行为:
      - 先编写集成测试
      - 填充实现细节
      - 关注端到端功能
      
elif workflow.test_strategy == "manual_testing":
    AI 行为:
      - 生成测试清单
      - 提供手动测试步骤
      - 不生成自动化测试
```

### Configuration in Memory

```markdown
# development_workflow.md

## Testing Strategy

**Current Strategy**: TDD (Test-Driven Development)

**Rules**:
1. Always write tests before implementation
2. Maintain >80% code coverage
3. Use pytest with async support
4. Mock external dependencies (Ollama, APIs)

**When to Change**:
- Switch to "prototype" mode for rapid experimentation
- Switch to "integration_first" for API validation
```

---

## Advanced Pattern 7: Memory Analytics Dashboard

### Health Metrics

```python
class MemoryHealthAnalyzer:
    async def generate_report(self):
        """生成记忆系统健康度报告"""
        
        metrics = {
            "coverage": await self.check_coverage(),
            "freshness": await self.check_freshness(),
            "connectivity": await self.check_connectivity(),
            "balance": await self.check_balance(),
        }
        
        # 计算综合健康度
        health_score = (
            metrics["coverage"] * 0.3 +
            metrics["freshness"] * 0.3 +
            metrics["connectivity"] * 0.2 +
            metrics["balance"] * 0.2
        )
        
        return {
            "score": health_score,
            "metrics": metrics,
            "recommendations": await self.generate_recommendations(metrics)
        }
    
    async def check_coverage(self):
        """检查记忆覆盖率"""
        required_memories = [
            "project_context_and_goals",
            "architecture_decisions",
            "code_patterns",
            "testing_strategies",
            "common_issues_solutions",
        ]
        
        coverage = sum(1 for m in required_memories 
                     if await self.memory_exists(m))
        
        return coverage / len(required_memories)
    
    async def check_freshness(self):
        """检查记忆新鲜度"""
        memories = await self.list_memories()
        total_age = 0
        
        for memory_name in memories:
            memory = await self.read_memory(memory_name)
            age = (datetime.now() - memory.last_updated).days
            total_age += age
        
        avg_age = total_age / len(memories)
        freshness = max(0, 1 - (avg_age / 90))  # 90天为过期
        
        return freshness
```

---

## Best Practices Summary

### DO ✅

- 建立清晰的记忆层次结构
- 使用语义化版本控制
- 定期维护和更新记忆
- 在记忆间建立链接关系
- 使用多项目共享通用知识
- 实施自动化健康检查

### DON'T ❌

- 不要创建平铺的记忆结构（无层次）
- 不要忽略记忆的版本控制
- 不要让记忆过期不更新
- 不要创建孤立记忆（无链接）
- 不要在每个项目中重复相同内容
- 不要忽视记忆系统的健康度

---

## Related Resources

- [MCP Server Best Practices](mcp_server_best_practices.md)
- [Code Patterns](code_patterns.md)
- [LLM Integration Patterns](llm_integration_patterns.md)
- [Development Workflow](development_workflow.md)

---

## Changelog

| 日期 | 变更 | 作者 |
|------|------|------|
| 2025-01-19 | 初始版本，记录高级使用模式 | AI Team |
