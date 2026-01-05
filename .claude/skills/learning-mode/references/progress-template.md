# Progress Tracking Template for Learning Mode

This file contains templates for tracking learning sessions and progress. Use these when saving session logs to `learning_progress/`.

## Session Log Template

Save to: `learning_progress/[TOPIC]_[YYYY-MM-DD].md`

```markdown
# Learning Session: [Topic]

**Date**: 2025-01-01
**Duration**: ~20 minutes
**Starting Level**: [Beginner|Intermediate|Advanced]
**Ending Level**: [Beginner|Intermediate|Advanced]
**Session Type**: [Codebase Exploration|Concept Learning|Review]

## Concepts Covered

### [Concept 1: Name]
- Status: [✅ Understood | ⚠️ Needs Review | 📝 To Explore]
- Confidence: [X]/10
- Quiz Score: [X]/[X] correct

### [Concept 2: Name]
- Status: [✅ Understood | ⚠️ Needs Review | 📝 To Explore]
- Confidence: [X]/10
- Quiz Score: [X]/[X] correct
- Knowledge Gap: [Specific gap identified, if any]

### [Concept 3: Name]
- Status: [📝 To Explore]
- Not covered in this session

## Questions & Answers

**Q1:** [Question from quiz]
**A1:** [User's answer]
**Feedback:** [AI feedback]

**Q2:** [Question from quiz]
**A2:** [User's answer]
**Feedback:** [AI feedback]

## Spaced Repetition Schedule

| Review Date | Concept | Reason | Confidence Goal |
|-------------|---------|--------|-----------------|
| [Day 3] | [Concept name] | Initial review | 7/10 |
| [Day 7] | [Concept names] | Weekly review | 8/10 |
| [Day 14] | [All concepts] | Full consolidation | 9/10 |

## Next Learning Steps

1. [ ] Practice: [Actionable next step]
2. [ ] Explore: [What to explore next]
3. [ ] Connect: [How this relates to other topics]

## Notes

[User's own notes or AI-suggested insights]
```

## Cumulative Progress Index Template

Auto-generate: `learning_progress/index.md`

```markdown
# Learning Progress Index

## Last Updated: [YYYY-MM-DD]

## Topics Mastered (Confidence ≥ 8/10)
- [x] [Topic 1] ([Date])
- [x] [Topic 2] ([Date])
- [x] [Topic 3] ([Date])

## Topics in Progress (Confidence 5-7/10)
- [ ] [Topic 1] ([X]/10, next review: [Date])
- [ ] [Topic 2] ([X]/10, next review: [Date])

## Topics to Explore
- [ ] [Topic 1]
- [ ] [Topic 2]
- [ ] [Topic 3]

## Quick Stats
- Total Sessions: [X]
- Concepts Mastered: [X]
- Avg Confidence: [X.X]/10
- Active Review Schedule: [X] items pending
```

## Spaced Repetition Interval Reference

Use these intervals based on quiz performance:

| Performance | Next Review | Interval |
|-------------|-------------|----------|
| Perfect score (2/2) | Day 7 | Long retention |
| 1/2 correct | Day 3 | Short reinforcement |
| 0/2 correct | Day 1 | Immediate review needed |
| Self-rated confidence < 5/10 | Day 1-2 | Re-explain concept |

## Confidence Level Guide

| Score | Description | Action |
|-------|-------------|--------|
| 9-10 | Can teach someone else | Move to advanced topics |
| 7-8 | Confident with minor gaps | Review in 1 week |
| 5-6 | Understand basics | Review in 3 days |
| 3-4 | Shaky understanding | Re-explain and retry |
| 1-2 | Confused | Start over with simpler approach |

## Status Icons Guide

| Icon | Meaning | Action |
|------|---------|--------|
| ✅ | Understood | Move forward, scheduled review |
| ⚠️ | Needs Review | Focus area for next session |
| 📝 | To Explore | Future topic, not yet covered |
| ❌ | Not Started | Not attempted yet |
