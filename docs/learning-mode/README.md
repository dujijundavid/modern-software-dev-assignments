# Learning Mode Documentation

**Overview**: Evidence-based learning design for Claude Code's interactive learning system.

---

## Quick Start

### What is Learning Mode?

Learning Mode is an interactive learning system built into Claude Code that adapts to each learner's level and goals. It uses a state machine with multiple teaching strategies (direct instruction, Socratic questioning, critical thinking challenges) to guide users from surface-level understanding to first-principles mastery.

### The 10 Design Principles (Quick Reference)

| # | Principle | Summary |
|---|-----------|----------|
| 1 | **Progressive Depth** | Surface → Essence → Philosophy → Application |
| 2 | **Adaptive Strategy** | Start direct, shift to Socratic when learner ready |
| 3 | **Metacognitive Prompting** | Articulation before explanation |
| 4 | **Critical Thinking Loops** | 2-3 refinements per concept |
| 5 | **Wait Time** | 5-15 seconds depending on complexity |
| 6 | **Validate-Challenge-Retarget** | Confidence first, then stretch |
| 7 | **Transfer Enablement** | Examples → Patterns → Principles → Transfer |
| 8 | **Motivation Design** | Competence + Value + Curiosity + Autonomy |
| 9 | **Chunking** | 3-4 ideas per chunk, ≤400 words |
| 10 | **Scaffolding Fading** | Heavy → Medium → Light as competence builds |

**Full details**: See [design-principles.md](design-principles.md)

---

## Document Structure

### Active References

| Document | Purpose |
|----------|---------|
| [design-principles.md](design-principles.md) | **Primary reference** - 10 evidence-based design principles with implementation guidelines |
| [implementation-summary.md](implementation-summary.md) | What was actually built in Phase 1+2 (PROBING, CHALLENGING, SYNTHESIZING states) |

### Historical Archives

| Document | Purpose |
|----------|---------|
| [research/learning-science-analysis.md](research/learning-science-analysis.md) | Academic research foundation - analysis of successful dialogue patterns |
| [proposals/enhancement-proposal-phase1-2.md](proposals/enhancement-proposal-phase1-2.md) | Original technical proposal for Phase 1+2 improvements |

---

## The State Machine

Learning Mode uses a 10-state machine:

| State | Purpose | Phase |
|-------|---------|-------|
| **CALIBRATING** | Initial assessment | Original |
| **TEACHING** | Direct content delivery | Original |
| **PROBING** ⭐ | Socratic questioning | Phase 1 |
| **CHALLENGING** ⭐ | Critical thinking tests | Phase 2 |
| **SYNTHESIZING** ⭐ | First-principles abstraction | Phase 2 |
| **QUIZ_ACTIVE** | Knowledge testing | Original |
| **FEEDBACK** | Quiz feedback | Original |
| **ANSWERING** | Q&A responses | Original |
| **QUIZ_PREP** | Transition state | Original |
| **SESSION_END** | Session cleanup | Original |

⭐ = Added in Phase 1+2 enhancements

**Key Transition**: `"我们聊的深入些"` (Let's go deeper) → Triggers shift to CHALLENGING state

---

## The "Go Deeper" Moment

The signature achievement of Learning Mode is the **learner-initiated depth transition**. When a user says "我们聊的深入些" (or similar), it signals:

- ✅ **Success momentum** built (confidence)
- ✅ **Relevance** established (value)
- ✅ **Curiosity** triggered (interest)
- ✅ **Autonomy** exercised (control)

This is the transition from teacher-led → learner-led exploration.

---

## Implementation

**Actual implementation**: [`.claude/commands/learning-mode.md`](../../.claude/commands/learning-mode.md)

For the most up-to-date state machine logic, question banks, and protocols, see the actual command file.

---

## Project History

### Phase 1: Deep Learning Foundation (Completed)
- Added PROBING state for Socratic questioning
- Implemented L0-L3 depth detection system
- Enhanced feedback loops (Validate → Challenge → Extend)

### Phase 2: Critical Thinking (Completed)
- Added CHALLENGING state for edge case testing
- Added SYNTHESIZING state for first-principles abstraction
- Implemented complete state decision tree

### Future: Phase 3+ (Proposed)
- TRANSFERRING state for cross-domain application
- REFLECTING state for metacognitive training
- Multi-modal learning (code + theory)

---

## Research Foundation

This system is grounded in established learning science research:

- **Cognitive Load Theory** (Sweller) - Chunking, load management
- **ICAP Framework** (Chi) - Interactive > Constructive > Active > Passive
- **Self-Determination Theory** (Deci & Ryan) - Intrinsic motivation
- **Transfer of Learning** (Perkins & Salomon) - Cross-domain connections
- **Metacognition** (Flavell, Nelson & Narens) - Making thinking visible
- **Flow Theory** (Csikszentmihalyi) - Optimal challenge zone

**Full bibliography**: See [research/learning-science-analysis.md](research/learning-science-analysis.md)

---

## Quick Reference: Insight Levels

When learners respond, classify their insight level:

| Level | Behavior | Response |
|-------|----------|----------|
| **REPEAT** | Parrots content | "Good memory! Now explain in your own words" |
| **APPLY** | Uses in familiar context | "Exactly! What about [edge case]?" |
| **CONNECT** | Makes cross-domain links | "Brilliant! What's the principle here?" |
| **SYNTHESIZE** | Creates new understanding | "Wow! You've discovered [Principle Name]" |

---

## For Developers

To extend or modify Learning Mode:

1. **Read** [design-principles.md](design-principles.md) for the "why"
2. **Review** [implementation-summary.md](implementation-summary.md) for what exists
3. **Edit** [`.claude/commands/learning-mode.md`](../../.claude/commands/learning-mode.md) for the "how"
4. **Test** with real learning scenarios
5. **Document** changes in [implementation-summary.md](implementation-summary.md)

---

**Last Updated**: 2026-01-15
**Status**: Phase 1+2 Complete, Phase 3 Proposed
