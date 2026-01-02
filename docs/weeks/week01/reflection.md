---
week: 1
title: "Week 1: Reflection"
type: reflection
status: completed
created: 2025-12-07
updated: 2026-01-02
related:
  - week1:overview.md
  - week1:implementation.md
tags: [week-1, prompting, reflection, lessons-learned]
---

# Week 1: Reflection

> **Navigation**: [CS146S Docs](../INDEX.md) > [Weeks](../weeks/) > [Week 1](../weeks/week01/) > Reflection

> Week 1 focused on building theoretical foundations and hands-on experience with prompt engineering techniques, particularly K-shot prompting and systematic problem diagnosis.

---

## What I Learned

### Technical Skills

- **K-Shot Prompting**: Mastered example selection, positioning, and format consistency
  - How I applied it: Designed 5-iteration progression for "httpstatus reversal" challenge
  - Resources that helped: [Prompt Engineering Methodology](../../learning_notes/week1/01_prompt_engineering_methodology.md), [Case Study](../../learning_notes/week1/03_case_study_httpstatus_reversal.md)
  - Confidence level: 5/5

- **Systematic Problem Diagnosis**: Applied 5W1H framework (Why, What, How, Which, Verify)
  - How I applied it: Used in every iteration to diagnose why prompts failed before changing them
  - Resources that helped: [AI Agent Interaction Guide](../../learning_notes/week1/02_ai_agent_interaction_guide.md)
  - Confidence level: 4/5

- **LLM Behavior Understanding**: Learned about temperature, randomness, and semantic interference
  - How I applied it: Adjusted expectations based on temperature=0.5; understood why "more detailed" prompts made things worse
  - Resources that helped: [Pre-Learning Concepts](../../learning_notes/week1/01_pre_learning_concepts.md)
  - Confidence level: 4/5

- **Prompt Iteration Strategy**: Learned to diagnose → design → test → reflect (not just trial-and-error)
  - How I applied it: Documented all 5 iterations with analysis, not just final result
  - Resources that helped: [Code Review Feedback](../../learning_notes/week1/03_code_review_feedback.md)
  - Confidence level: 5/5

### AI Engineering Concepts

- **Recency Bias in LLMs**: LLMs weight later information more heavily in prompts
  - Real-world application: Always put most important/critical example last in K-shot prompts
  - Connection to course themes: Understanding LLM architecture (attention mechanism) informs prompt design

- **Semantic Pollution**: LLMs can be "distracted" by word meanings, interfering with mechanical tasks
  - Real-world application: Use "semantic firewalls" for non-semantic tasks (data transformation, formatting)
  - Connection to course themes: LLMs are probabilistic, not rule-based; need to design for this reality

- **Information vs. Noise**: More information doesn't always help; can create interference
  - Real-world application: Evaluate each prompt addition for signal-to-noise ratio
  - Connection to course themes: Good engineering is about removing complexity, not adding it

- **Direct Matching > Abstract Rules**: LLMs excel at mimicking examples, not inferring rules
  - Real-world application: Show examples liberally; don't rely on abstract instructions
  - Connection to course themes: Work with the model's strengths (pattern matching), not weaknesses (rule inference)

### Automation & Systems Thinking

**Automations I built/used**:
1. **test_your_prompt() function**: Automated testing framework that runs prompt 5 times and checks for success
   - Time saved: ~10 minutes per iteration (vs. manual testing)
2. **Iteration documentation template**: Structured format for recording prompts, outputs, and analysis
   - Time saved: Enabled rapid pattern recognition across iterations; ~30 minutes saved in overall learning

**Systems thinking insights**:
- **Diagnosis > Speed**: Taking 5 minutes to diagnose why something failed saves 30 minutes of random trial-and-error
- **Failures are data**: Each failed iteration provided information (e.g., Chain-of-Thought caused semantic pollution)
- **Principles over patterns**: Understanding WHY something works (Recency Bias) is more valuable than the specific prompt that works
- **Documentation is leverage**: Writing down iterations transformed individual experiments into a reusable case study

---

## What I'd Do Differently

### Mistake 1: Over-Engineering with Chain-of-Thought

- **What happened**: Added detailed step-by-step reasoning to K-shot prompt, expecting improvement
- **Root cause**: Assumed "more guidance = better performance" without considering semantic interference
- **Impact**: Performance degraded dramatically (HTTP status codes appeared); wasted ~15 minutes
- **How I'd fix it**: Start simpler; add complexity only if simpler approaches fail
- **Prevention strategy**: Always test baseline → simple → complex, not reverse
- **Automation opportunity**: Could build a "complexity checker" that warns if prompt length exceeds threshold

### Mistake 2: Not Testing Multiple Runs Initially

- **What happened**: Tested some iterations only once, missing the randomness effect
- **Root cause**: Forgot that temperature=0.5 means 50% randomness; single runs aren't representative
- **Impact**: Misjudged some prompts as "good" when they were actually unstable
- **How I'd fix it**: Always run 5x from the start; never trust single-run results
- **Prevention strategy**: Make test function enforce 5 runs by default
- **Automation opportunity**: Auto-run 5x and report success rate + variance

### Mistake 3: Focusing on Output Format Over Strategy

- **What happened**: Initially spent time on perfecting prompt formatting (bullet points, bolding, etc.)
- **Root cause**: Confused "polished appearance" with "effective prompting"
- **Impact**: Wasted ~10 minutes on formatting that didn't affect performance
- **How I'd fix it**: Focus on content (examples, constraints) first; format last
- **Prevention strategy**: Set a timer: 5 min max on formatting before testing
- **Automation opportunity**: Prompt formatter/linter that standardizes format automatically

### Mistake 4: Not Anticipating Semantic Pollution

- **What happened**: Surprised when "httpstatus" triggered HTTP status code generation
- **Root cause**: Didn't consider that LLMs interpret words semantically, not just mechanically
- **Impact**: Lost time debugging why Chain-of-Thought failed
- **How I'd fix it**: Proactively ask: "Could the word meanings interfere with the task?"
- **Prevention strategy**: Add "semantic interference check" to diagnosis framework
- **Automation opportunity**: Tool that detects "risky words" in prompts and suggests semantic firewalls

---

## Time Allocation

| Activity | Estimated | Actual | Variance | Notes |
|----------|-----------|--------|----------|-------|
| Reading theory & concepts | 3 hrs | 2.5 hrs | -0.5 hrs | Concepts were clearer than expected |
| Setting up environment (Ollama) | 1 hr | 0.5 hrs | -0.5 hrs | Already had conda set up |
| Implementing K-shot baseline | 1 hr | 1.5 hrs | +0.5 hrs | Debugging environment issues |
| Iterating on prompts (5 iterations) | 2 hrs | 3 hrs | +1 hr | Chain-of-Thought detour took time |
| Documenting iterations | 1 hr | 2 hrs | +1 hr | More detailed than planned |
| Writing reflection | 1 hr | 1 hr | 0 hrs | As expected |
| **Total** | **9 hrs** | **10.5 hrs** | **+1.5 hrs** | Reasonable for first week |

**Time allocation insights**:
- Iteration + documentation took longer than expected, but was high-value (created reusable case study)
- Environment setup was faster due to prior conda/Poetry experience
- Chain-of-Thought detour was "expensive" but taught critical lesson about semantic pollution
- Next time: Allocate more time for systematic documentation (it pays off)

---

## Quality Metrics

### Code Quality

- **Test coverage**: N/A (Week 1 is exploratory, not production code)
- **Linting/Type checking**: Not applicable (experimentation scripts)
- **Code review feedback**: Received detailed feedback on prompt structure and methodology (see [Code Review Feedback](../../learning_notes/week1/03_code_review_feedback.md))
- **Self-assessment**: 4/5 - Prompts are effective, but could be more generalized

### Documentation Quality

- **Completeness**: All required docs created (7 learning notes + 3 new structured docs) ✓
- **Clarity**: 5/5 - Clear structure, examples, and explanations
- **Reusability**: High - Case study format makes concepts transferable

### Learning Depth

- **Concept understanding**: 5/5 - Can explain Recency Bias, semantic pollution, and K-shot design principles
- **Ability to explain to others**: 5/5 - Confident I could teach these concepts to a peer
- **Connection to previous weeks**: N/A - This is Week 1, but sets foundation for Weeks 2-8

---

## Next Steps

### Immediate (This Week)

- [x] Complete all 6 prompting technique implementations
- [x] Document each technique with examples
- [x] Create technique selection matrix
- [ ] Practice applying K-shot to 2-3 new words (generalization test)
- [ ] Build simple "prompt tester" automation for future weeks

### Short-term (Next Week - Week 2)

- [ ] Apply Week 1 prompting skills to Action Item Extraction (LLM-based)
- [ ] Use systematic diagnosis (5W1H) for any failures
- [ ] Document Week 2 using same structured format
- [ ] Build prompt versioning system to track iterations across weeks

### Long-term (Course Goals)

- [ ] Develop "prompt engineering playbook" by end of course
- [ ] Create reusable prompt templates for common LLM tasks
- [ ] Build automated prompt evaluation framework
- [ ] Contribute prompt patterns back to open-source community

---

## Questions for Future

### Unresolved Questions

- **Question 1**: How do K-shot principles scale to much longer texts (paragraphs, documents)?
  - Current understanding: Works for words/sentences; unclear for longer contexts
  - Need to test: Does Recency Bias still apply with 1000+ token contexts?

- **Question 2**: How do different models (GPT-4, Claude, Llama) compare on semantic pollution?
  - Current understanding: Tested only on mistral-nemo:12b
  - Need to test: Are larger models more/less susceptible to semantic interference?

- **Question 3**: Can we quantify "signal-to-noise ratio" in prompts?
  - Current understanding: Qualitative concept
  - Need to test: Can we build an automated tool that measures prompt "clarity"?

### Topics to Revisit

- **Topic 1**: Chain-of-Thought variations (didn't work for httpstatus, but critical for reasoning tasks)
  - Need to understand: When does CoT help vs. hurt?
  - Plan: Test CoT on math/logic problems (where it should shine)

- **Topic 2**: Self-Consistency and voting mechanisms
  - Need to understand: Cost-benefit of running LLM 5x vs. single better prompt
  - Plan: Implement Self-Consistency for Week 1 tasks

- **Topic 3**: Tool Calling and function integration
  - Need to understand: How to structure tool definitions for maximum clarity
  - Plan: Build Week 1 tool calling examples (e.g., calculator for verification)

---

## Connection to Course Themes

### Stanford AI Engineering Mindset

**Build Systems, Not Just Code**:
- Week 1 could have been "just write prompts until one works"
- Instead, built a **systematic framework**: 5W1H diagnosis → iteration design → documentation
- Created reusable artifacts (case study, methodology guide) that benefit all future weeks
- Example: The "httpstatus reversal" case study is now a teaching tool, not just a solved problem

**System-level thinking examples**:
- Designed iteration tracker to work for ANY prompting task, not just httpstatus
- Created 5W1H framework applicable to ALL AI debugging, not just Week 1
- Documented principles (Recency Bias, semantic pollution) that generalize across tasks

### The Automation Hierarchy

**Current level achieved**: Level 2 (Reusable Functions)

**Evidence**:
- Built `test_your_prompt()` function that works for any prompt
- Created iteration documentation template reusable across weeks
- Developed prompting methodology applicable to all 6 techniques

**Next level goal**: Level 3 (Composable Systems)

**What would advance to next level**:
- Build prompt pipeline that chains techniques: K-shot → CoT → Self-Consistency
- Create automated prompt evaluator that suggests improvements
- Develop prompt version control with A/B testing framework

### The Three Questions

1. **What's the bottleneck?**
   - **Answer for Week 1**: Manual prompt trial-and-error without systematic diagnosis
   - **Evidence**: Spent 3+ hours iterating; could have been faster with better diagnosis
   - **Solution built**: 5W1H framework, iteration templates

2. **What's the leverage point?**
   - **Answer for Week 1**: Understanding WHY prompts work (principles) > specific prompts that work
   - **Evidence**: Recency Bias principle now applicable to ALL future tasks
   - **Solution built**: Documented principles (semantic pollution, information vs. noise) in case study

3. **How to compound value?**
   - **Answer for Week 1**: Use Week 1 learnings to accelerate Weeks 2-8
   - **Evidence**: Same 5W1H framework, iteration templates, and diagnostic approach apply to all weeks
   - **Solution built**: Structured documentation in `/docs/weeks/week01/` enables reuse

---

## Key Takeaways Summary

### Technical Mastery

✅ **K-Shot Prompting**: Deep understanding of example selection, positioning (Recency Bias), and format consistency

✅ **Systematic Diagnosis**: 5W1H framework prevents random trial-and-error

✅ **LLM Behavior**: Understanding of temperature, semantic pollution, and probability-based reasoning

### Mental Models

✅ **LLMs are pattern matchers, not rule engines**: Design for this reality

✅ **Information vs. Noise**: More prompt ≠ better prompt; maximize signal-to-noise

✅ **Diagnosis > Speed**: 5 minutes of analysis saves 30 minutes of blind iteration

### Process Improvements

✅ **Document everything**: Failures are data; iterations are lessons

✅ **Build systems, not just solutions**: Frameworks (5W1H, iteration tracker) outlive specific problems

✅ **Principles over patterns**: Understanding WHY is more valuable than knowing WHAT

---

## Quick Links

- [Overview](./overview.md) - Concepts and objectives
- [Implementation](./implementation.md) - Technical approach and decisions
- [Weekly Deliverable](../../weeks/week1/writeup.md) - Submission writeup

---

*[Template: weekly_reflection.md - Migrated from learning_notes/week1/]*
*[Last updated: 2026-01-02]*
