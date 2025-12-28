# Learning Progress

Track skills acquired, concepts mastered, and proficiency growth throughout the 8-week course.

## Course Overview: CS146S Modern Software Developer

Philosophy: Hands-on building progressing from basic prompting to multi-agent AI systems.

```
Week 1: Prompt Engineering → Learn LLM communication
         ↓
Week 2: LLM-Powered Apps → Integrate LLMs into applications
         ↓
Week 3: MCP Servers → Extend AI tool capabilities
         ↓
Week 4-7: AI-Human Collaboration → Automated workflows
         ↓
Week 8: Multi-Stack → Full-stack AI applications
```

---

## Week 1: Prompt Engineering ✅

**Skills Mastered:**
- K-shot prompting (5-shot examples)
- Chain-of-thought reasoning
- Tool calling with function definitions
- RAG (Retrieval-Augmented Generation) basics

**Proficiency Level:** Intermediate

**Learning Resources:** learning_notes/week1/ (8 files)

**Knowledge Gaps:**
- Reflexion pattern needs more practice

**Key Insights:**
- System prompts matter more than few-shot examples for consistency
- Temperature=0.1 provides reliable outputs for structured data

---

## Week 2: LLM Integration 🟡 IN PROGRESS

**Current Focus:** Building reliable LLM-powered action item extraction

**Skills In Progress:**
- FastAPI + Ollama integration
- Structured JSON output handling
- Testing LLM-powered functions
- Service layer architecture patterns

**Proficiency Level:** Beginner → Intermediate

**Recent Accomplishments:**
- Implemented `extract_action_items_llm()` with JSON schema validation
- Database layer refactoring with custom exceptions
- Test coverage improvements

**Current Challenges:**
- LLM response reliability (hallucinations, formatting issues)
- Test isolation for LLM-dependent code

**Next Steps:**
- Master mocking strategies for LLM unit tests
- Improve prompt engineering for consistent outputs

---

## Week 3: MCP Servers ⏳ NOT STARTED

**Planned Skills:**
- Model Context Protocol fundamentals
- Tool definition and implementation
- Rate limiting and error handling
- Async MCP server patterns

---

## Week 4-8: Advanced Topics ⏳ NOT STARTED

**Projected Skills:**
- Multi-agent orchestration
- Human-AI collaboration workflows
- Full-stack AI application development

---

## Cross-Week Connections

| Week | Builds On | Enables |
|------|-----------|---------|
| Week 1 | - | Week 2 (prompts) |
| Week 2 | Week 1 | Week 3 (tool patterns) |
| Week 3 | Week 2 | Weeks 4-7 (MCP clients) |
| Weeks 4-7 | Week 3 | Week 8 (full integration) |

---

## Personal Goals

1. **Master prompt engineering** for reliable LLM outputs ✅ Week 1
2. **Build production-ready FastAPI apps** 🟡 Week 2
3. **Understand multi-agent AI orchestration** ⏳ Weeks 4-7
4. **Contribute to open-source AI tools** 🎯 Stretch goal

---

## Success Criteria

| Criterion | Target | Status |
|-----------|--------|--------|
| All weeks completed | 8/8 | 2/8 |
| Test coverage >80% | Per week | 🟡 On track |
| Learning notes created | Per week | ✅ Week 1 |
| GitHub portfolio | ≥1 project | ⏳ Pending |
