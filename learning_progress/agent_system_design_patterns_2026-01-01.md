# Learning Session: Agent System Design Patterns (Week 5)

**Date**: 2026-01-01
**Duration**: ~20 minutes
**Starting Level**: Beginner
**Ending Level**: Beginner → Early Intermediate
**Session Type**: Concept Understanding

## Concepts Covered

### Sequential vs Parallel vs Orchestrator (overview)
- Status: ✅ Understood (high-level)
- Confidence: 6/10

### Parallel pattern safety (Gate → Map → Reduce → Verify → Rollback)
- Status: ✅ Understood (basic template)
- Confidence: 6/10
- Key decision: Gate = small set of key unit tests (A2)

### Critic vs Verifier (role separation + loop control)
- Status: ✅ Understood (rules)
- Confidence: 6/10
- Key decision: Critic max 2 rounds, block P0/P1 only (B2)

## Questions & Answers

**Q1:** Parallel 模式里 Gate 最适合做哪类检查？  
**A1:** 选择 “跑 2-3 个关键单测”（A2）  
**Feedback:** ✓ Gate 目标是便宜且能挡大坑；全量测试太贵，不适合放在并行前。

**Q2:** Critic 停止条件怎么设避免无限返工？  
**A2:** 最多 2 轮 + 只拦截 P0/P1（B2）  
**Feedback:** ✓ 有轮次上限 + 严重级别门禁 + 可验证标准，可避免“无限完美主义循环”。

## Spaced Repetition Schedule

| Review Date | Concept | Reason | Confidence Goal |
|-------------|---------|--------|-----------------|
| 2026-01-04 | Critic vs Verifier | 巩固角色边界 | 7/10 |
| 2026-01-08 | Parallel safety template | 能复述并应用到 Week5 | 8/10 |
| 2026-01-15 | 3 patterns compare | 建立选型直觉 | 8/10 |

## Next Learning Steps

1. [ ] 把 “Gate/Verify” 映射到 Week5：分别对应哪些 `make` 命令？
2. [ ] 选一个 Week5 automation（Sequential 或 Parallel）写出手工流程图（输入/输出/停止条件）。
3. [ ] 准备一个 Critic 规则清单（P0/P1 定义 + 两轮上限），用于后续实现时落地。

