# Business Panel Analysis System

**Command**: `/sc:business-panel`
**Category**: Analysis & Strategic Planning
**Purpose**: Multi-expert business analysis through simulated panel discussions

---

## 📖 Table of Contents

- [Quick Start](#quick-start)
- [Expert Frameworks Reference](#expert-frameworks-reference)
- [Mode Selection Guide](#mode-selection-guide)
- [Common Use Cases](#common-use-cases)
- [Integration with Other Tools](#integration-with-other-tools)
- [Best Practices](#best-practices)
- [Examples & Templates](#examples--templates)

---

## 🚀 Quick Start

### 5-Minute Getting Started

**Step 1: Basic Analysis**
```bash
# Analyze a document with default settings (discussion mode, auto-selected experts)
/sc:business-panel ./docs/strategy.md
```

**Step 2: Select Specific Experts**
```bash
# Focus on competitive strategy and innovation
/sc:business-panel ./docs/strategy.md --experts "porter,christensen"
```

**Step 3: Choose Analysis Mode**
```bash
# Stress-test your strategy with adversarial analysis
/sc:business-panel ./docs/strategy.md --mode debate
```

**Step 4: Get Quick Synthesis**
```bash
# Skip detailed discussion, get just the key insights
/sc:business-panel ./docs/strategy.md --synthesis-only
```

### Command Syntax

```bash
/sc:business-panel [document_path_or_content] [options]

Options:
  --experts <names>          Comma-separated expert names
  --mode <discussion|debate|socratic|adaptive>
  --focus <domain>           Auto-select experts for domain
  --synthesis-only           Show only synthesis, skip detailed analysis
  --structured               Use symbol system for efficiency
  --verbose                  Full detailed analysis
  --questions                Focus on strategic questions
```

---

## 🧠 Expert Frameworks Reference

### 1. Clayton Christensen
**Framework**: Disruption Theory, Jobs-to-be-Done

**Core Concepts**:
- Disruptive vs. Sustaining Innovation
- Jobs-to-be-Done (JTBD) Framework
- Theory of Innovator's Dilemma

**When to Use**:
- Analyzing innovation strategies
- Understanding why products succeed/fail
- Evaluating market disruption potential
- Product development decisions

**Key Questions**:
- What "job" is the customer hiring this product to do?
- Is this innovation sustaining or disruptive?
- Who are the underserved or non-consumers?

---

### 2. Michael Porter
**Framework**: Competitive Strategy, Five Forces

**Core Concepts**:
- Five Forces Analysis (Supplier power, Buyer power, Competition, Substitution, Entry)
- Generic Strategies (Cost leadership, Differentiation, Focus)
- Value Chain Analysis

**When to Use**:
- Industry analysis and market positioning
- Competitive strategy development
- Assessing industry attractiveness
- M&A and partnership decisions

**Key Questions**:
- What are the five forces in this industry?
- What's our sustainable competitive advantage?
- How can we build defensible barriers to entry?

---

### 3. Peter Drucker
**Framework**: Management Philosophy, MBO (Management by Objectives)

**Core Concepts**:
- Management by Objectives
- Knowledge Worker Productivity
- Innovation and Entrepreneurship
- Purpose of business = creating customer

**When to Use**:
- Organizational design and management
- Goal setting and performance measurement
- Knowledge work optimization
- Strategic planning cycles

**Key Questions**:
- What business are we really in?
- What should we abandon to make room for innovation?
- How do we measure knowledge worker productivity?

---

### 4. Seth Godin
**Framework**: Marketing Innovation, Tribe Building

**Core Concepts**:
- Purple Cow (remarkable products)
- Tribe Building (leading movements)
- Permission Marketing
- The Dip (when to quit vs. stick)

**When to Use**:
- Marketing strategy and positioning
- Community building and engagement
- Product launch strategies
- Brand differentiation

**Key Questions**:
- Is this remarkable? Would people talk about it?
- Who is our tribe and what do they believe?
- What permission do we have from our audience?

---

### 5. W. Chan Kim & Renée Mauborgne
**Framework**: Blue Ocean Strategy

**Core Concepts**:
- Red Ocean (competition) vs. Blue Ocean (uncontested space)
- Strategy Canvas
- Four Actions Framework (Eliminate, Reduce, Raise, Create)
- Value Innovation

**When to Use**:
- Market entry and positioning
- Product differentiation strategies
- Escaping competitive markets
- Creating new demand

**Key Questions**:
- What factors should we eliminate that industry takes for granted?
- What factors should we reduce below industry standard?
- What factors should we raise above industry standard?
- What factors should we create that never existed?

---

### 6. Jim Collins
**Framework**: Organizational Excellence, Good to Great

**Core Concepts**:
- Level 5 Leadership
- First Who, Then What
- Confront the Brutal Facts
- Hedgehog Concept (passion, best at, economic engine)
- Flywheel Effect

**When to Use**:
- Organizational transformation
- Leadership development
- Building enduring companies
- Strategic focus and prioritization

**Key Questions**:
- What can we be the best in the world at?
- What are we deeply passionate about?
- What drives our economic engine?
- Is this a "doom loop" or a "flywheel" decision?

---

### 7. Nassim Nicholas Taleb
**Framework**: Risk Management, Antifragility

**Core Concepts**:
- Fragile, Robust, Antifragile
- Black Swan Events
- Skin in the Game
- Via Negativa (subtraction improves)

**When to Use**:
- Risk assessment and management
- System design and resilience
- Decision-making under uncertainty
- Stress-testing strategies

**Key Questions**:
- What's fragile here? What can break?
- What black swans could destroy us?
- Do we have skin in the game?
- How can we benefit from volatility?

---

### 8. Donella Meadows
**Framework**: Systems Thinking, Leverage Points

**Core Concepts**:
- Systems Archetypes
- Leverage Points (places to intervene in system)
- Feedback loops (reinforcing, balancing)
- Delays and oscillations

**When to Use**:
- Complex system analysis
- Finding high-leverage interventions
- Understanding unintended consequences
- Organizational/system design

**Key Questions**:
- Where are the feedback loops in this system?
- What are the leverage points for change?
- What delays exist that cause problems?
- What archetypes are at play?

---

### 9. Jean-luc Doumont
**Framework**: Communication Systems, Structured Clarity

**Core Concepts**:
- Bottom-up communication structure
- Assertion-Evidence approach
- Cognitive load management
- Visual clarity principles

**When to Use**:
- Presentation and communication design
- Document structure and clarity
- Teaching and explaining complex ideas
- Technical communication

**Key Questions**:
- What's the core message?
- What's the evidence for each assertion?
- Are we managing cognitive load?
- Is this structured for clarity?

---

## 🎯 Mode Selection Guide

### Decision Tree

```
Start
 │
 ├─→ What's your primary goal?
 │    │
 │    ├─ Explore and understand → DISCUSSION MODE
 │    ├─ Stress-test and challenge → DEBATE MODE
 │    └─ Learn and question → SOCRATIC MODE
 │
 └─→ Not sure? Use --mode adaptive
```

### Mode Comparison

| Aspect | Discussion | Debate | Socratic |
|--------|-----------|--------|----------|
| **Tone** | Collaborative | Adversarial | Inquisitive |
| **Goal** | Comprehensive analysis | Stress-test ideas | Deep learning |
| **Expert Interaction** | Build on each other | Challenge each other | Ask questions |
| **Output** | Balanced synthesis | Critical analysis | Strategic questions |
| **Best For** | Initial analysis | High-stakes decisions | Learning & prep |

### When to Use Each Mode

#### Discussion Mode (Default)
```yaml
Use Cases:
  - Initial strategic analysis
  - Exploring new business models
  - Synthesizing diverse perspectives
  - Team alignment and understanding

Not For:
  - Controversial topics (use debate)
  - Learning concepts (use socratic)
  - Quick decisions (use synthesis-only)
```

#### Debate Mode
```yaml
Use Cases:
  - Stress-testing controversial strategies
  - Evaluating high-risk decisions
  - Challenging assumptions
  - Preparing for investor/board questions

Not For:
  - Initial exploration (use discussion)
  - Consensus building (creates conflict)
  - Sensitive team dynamics
```

#### Socratic Mode
```yaml
Use Cases:
  - Learning business strategy concepts
  - Developing strategic thinking
  - Preparing for board meetings
  - Interview preparation

Not For:
  - Quick answers (slower process)
  - Actionable plans (generates questions)
  - Time-sensitive analysis
```

#### Adaptive Mode
```yaml
Uses:
  - When you're unsure which mode to pick
  - Let the system analyze content and select
  - Good for first-time users

Logic:
  - Detects controversy → Debate
  - Detects learning context → Socratic
  - Default → Discussion
```

---

## 💼 Common Use Cases

### 1. Strategic Document Review

**Scenario**: Reviewing a product strategy document

```bash
# Comprehensive analysis with multiple frameworks
/sc:business-panel ./docs/product-strategy.md \
  --experts "porter,christensen,collins" \
  --mode discussion
```

**What You Get**:
- Porter: Competitive positioning and five forces
- Christensen: Jobs-to-be-done and disruption potential
- Collins: Hedgehog concept and flywheel analysis
- Cross-framework synthesis showing connections

**Expert Selection Rationale**:
- Porter → Market position
- Christensen → Innovation angle
- Collins → Organizational capacity

---

### 2. Risk Analysis

**Scenario**: Evaluating a risky market expansion

```bash
# Stress-test with risk and systems experts
/sc:business-panel ./docs/expansion-plan.md \
  --experts "taleb,meadows" \
  --mode debate
```

**What You Get**:
- Taleb: Fragility analysis, black swan scenarios, antifragility opportunities
- Meadows: System leverage points, feedback loops, unintended consequences
- Debate between them on risk assessment
- Synthesis of robust risk mitigation strategies

**Why Debate Mode**: Risk analysis requires stress-testing and adversarial thinking

---

### 3. Innovation Strategy

**Scenario**: Analyzing a new product concept

```bash
# Innovation and marketing focus
/sc:business-panel ./docs/product-concept.md \
  --experts "christensen,kim,godin" \
  --mode discussion
```

**What You Get**:
- Christensen: JTBD, disruption potential, target customers
- Kim: Blue ocean opportunity, value innovation
- Godin: Remarkability, tribe identification, permission
- Synthesis: Integrated go-to-market strategy

**Expert Synergy**: These frameworks complement each other perfectly for innovation

---

### 4. Organizational Transformation

**Scenario**: Planning a major company change

```bash
# Organizational excellence focus
/sc:business-panel ./docs/transformation-plan.md \
  --experts "collins,drucker,meadows" \
  --mode discussion
```

**What You Get**:
- Collins: Flywheel building, first-who-then-what, brutal facts
- Drucker: MBO setup, abandonment decisions, knowledge work
- Meadows: System leverage points, feedback design, change delays
- Synthesis: Transformation roadmap with clear leverage points

---

### 5. Quick Synthesis for Executive Summary

**Scenario**: Need quick insights for leadership

```bash
# Get just the synthesis, skip detailed discussion
/sc:business-panel ./docs/strategy.md \
  --experts "porter,christensen" \
  --synthesis-only \
  --structured
```

**What You Get**:
- No detailed back-and-forth
- Just the key insights and synthesis
- Symbol-based structure for quick scanning
- Perfect for executive summaries

---

### 6. Learning Business Strategy

**Scenario**: Preparing for an exam or interview

```bash
# Use socratic mode to generate questions
/sc:business-panel ./docs/case-study.md \
  --experts "porter,christensen" \
  --mode socratic \
  --questions
```

**What You Get**:
- Strategic questions instead of answers
- Helps develop strategic thinking
- Prepares you for case interviews
- Questions that probe deeper understanding

---

### 7. Pre-Board Meeting Preparation

**Scenario**: Getting ready for a board presentation

```bash
# Multi-mode analysis: first explore, then stress-test
/sc:business-panel ./docs/board-deck.md \
  --experts "collins,taleb,porter" \
  --mode discussion

# Then stress-test with debate
/sc:business-panel ./docs/board-deck.md \
  --experts "taleb,porter" \
  --mode debate
```

**Two-Pass Strategy**:
1. Discussion mode: Explore all angles, get comprehensive view
2. Debate mode: Stress-test assumptions, prepare for tough questions

---

### 8. Competitive Intelligence

**Scenario**: Analyzing a competitor's move

```bash
# Competitive analysis focus
/sc:business-panel ./docs/competitor-analysis.md \
  --experts "porter,christensen" \
  --mode discussion
```

**What You Get**:
- Porter: Five forces impact, competitive dynamics
- Christensen: Disruptive threat assessment
- Synthesis: Strategic response options

---

## 🔗 Integration with Other Tools

### With `/sc:index-repo`

**Workflow**: Index repository first, then analyze specific docs

```bash
# Step 1: Index the repo for context
/sc:index-repo

# Step 2: Analyze specific strategy docs with rich context
/sc:business-panel ./strategy/go-to-market.md --experts "porter,kim"
```

**Benefit**: Business panel understands your full codebase context

---

### With `/sc:pm` (Project Manager)

**Workflow**: Use PM to plan, business panel to analyze strategic decisions

```bash
# Step 1: Plan the feature
/sc:pm "Plan a new subscription feature"

# Step 2: Analyze the business model
/sc:business-panel ./docs/subscription-model.md \
  --experts "christensen,collins,porter"
```

**Benefit**: Combines execution planning with strategic analysis

---

### With `/sc:document`

**Workflow**: Document → Analyze → Refine

```bash
# Step 1: Draft initial document
/sc:document "Create a product strategy doc"

# Step 2: Analyze with business panel
/sc:business-panel ./docs/strategy.md --mode discussion

# Step 3: Refine based on insights
/sc:document "Update strategy with panel insights"
```

**Benefit**: Iterative refinement with expert feedback

---

### With `/sc:analyze`

**Workflow**: Technical analysis → Business analysis

```bash
# Step 1: Code/technical analysis
/sc:analyze ./src --security --performance

# Step 2: Business implications
/sc:business-panel ./docs/architecture.md \
  --experts "collins,taleb" \
  --mode debate
```

**Benefit**: Full stack analysis from code to business strategy

---

### Multi-Agent Orchestration

**Advanced Pattern**: Run multiple analyses in parallel

```bash
# Terminal 1: Technical analysis
/sc:analyze ./backend --security &

# Terminal 2: Repository indexing
/sc:index-repo &

# Terminal 3: Business analysis
/sc:business-panel ./docs/strategy.md --experts "porter,christensen"

# All run in parallel, then synthesize results
```

**Benefit**: Comprehensive analysis in parallel time

---

## ✅ Best Practices

### Expert Selection

| Tip | Explanation |
|-----|-------------|
| **Start with 2-3 experts** | More = analysis paralysis, conflicting frameworks |
| **Choose complementary experts** | Porter + Christensen = great combo for strategy |
| **Match experts to goal** | Risk analysis → Taleb + Meadows |
| **Use domain experts for your industry** | Tech → Christensen, Manufacturing → Porter |
| **Avoid over-selection** | 5+ experts = hard to synthesize |

### Mode Selection

| Tip | Explanation |
|-----|-------------|
| **Discussion first** | Always start with collaborative mode |
| **Debate for controversy** | Use debate when you need stress-testing |
| **Socratic for learning** | When you want to develop thinking, not get answers |
| **Adaptive when unsure** | Let the system pick based on content |
| **Combine modes** | Discussion → Debate is powerful pattern |

### Getting the Most Value

| Tip | Explanation |
|-----|-------------|
| **Use --synthesis-only for summaries** | Skip details, get insights |
| **Use --structured for quick scanning** | Symbol-based, easier to parse |
| **Use --questions for learning** | Generates questions, not answers |
| **Document the synthesis** | Cross-expert insights are most valuable |
| **Iterate based on insights** | Don't just read, act on the analysis |

### Common Mistakes to Avoid

| Mistake | Solution |
|---------|----------|
| **Using all 9 experts** | Start with 2-3, add if needed |
| **Skipping the synthesis** | The synthesis is where gold is |
| **Wrong mode for goal** | Use decision tree to pick mode |
| **One-shot analysis** | Run discussion, then debate for depth |
| **Not acting on insights** | Analysis without action = waste |

### Workflow Patterns

#### Pattern 1: Exploration → Stress-Testing
```bash
# Step 1: Explore comprehensively
/sc:business-panel doc.md --mode discussion

# Step 2: Stress-test the conclusions
/sc:business-panel doc.md --mode debate

# Step 3: Extract synthesis
/sc:business-panel doc.md --synthesis-only
```

#### Pattern 2: Multi-Expert Deep Dive
```bash
# Run same doc through different expert combinations
/sc:business-panel doc.md --experts "porter,christensen"
/sc:business-panel doc.md --experts "collins,drucker"
/sc:business-panel doc.md --experts "taleb,meadows"

# Compare syntheses for comprehensive view
```

#### Pattern 3: Learning Loop
```bash
# Step 1: Generate questions
/sc:business-panel case.md --mode socratic --questions

# Step 2: Research answers
# (Use web search, read docs, etc.)

# Step 3: Test understanding
/sc:business-panel case.md --mode socratic
```

---

## 📋 Examples & Templates

### Template 1: Product Launch Analysis

```markdown
# Product Launch Business Panel Analysis

## Document to Analyze
Path: ./product-launch-plan.md

## Expert Selection
- **Christensen**: JTBD, disruption potential
- **Kim**: Blue ocean positioning
- **Godin**: Marketing and tribe building

## Command
```bash
/sc:business-panel ./product-launch-plan.md \
  --experts "christensen,kim,godin" \
  --mode discussion
```

## Expected Insights
- Target customer jobs-to-be-done
- Blue ocean opportunity map
- Tribe identification and remarkability
- Integrated go-to-market synthesis
```

---

### Template 2: Risk Assessment

```markdown
# Risk Assessment Business Panel Analysis

## Document to Analyze
Path: ./risky-proposal.md

## Expert Selection
- **Taleb**: Fragility, black swans, antifragility
- **Meadows**: System risks, leverage points
- **Collins**: Organizational capacity assessment

## Command
```bash
/sc:business-panel ./risky-proposal.md \
  --experts "taleb,meadows,collins" \
  --mode debate
```

## Expected Insights
- Fragility points and breaking scenarios
- Black swan risks and mitigation
- System leverage points for resilience
- Debate on risk tolerance
- Antifragile opportunities
```

---

### Template 3: Strategic Planning

```markdown
# Strategic Planning Business Panel Analysis

## Document to Analyze
Path: ./annual-strategy.md

## Expert Selection
- **Drucker**: What business are we in?
- **Porter**: Competitive positioning
- **Collins**: Hedgehog and flywheel

## Command
```bash
/sc:business-panel ./annual-strategy.md \
  --experts "drucker,porter,collins" \
  --mode discussion \
  --structured
```

## Expected Insights
- Core business definition (Drucker)
- Competitive advantage (Porter)
- Strategic focus areas (Collins)
- Integrated strategic roadmap
```

---

### Template 4: Innovation Workshop

```markdown
# Innovation Workshop Business Panel Analysis

## Document to Analyze
Path: ./innovation-ideas.md

## Expert Selection
- **Christensen**: Disruption analysis
- **Kim**: Blue ocean canvas
- **Godin**: Remarkability filter

## Command
```bash
/sc:business-panel ./innovation-ideas.md \
  --experts "christensen,kim,godin" \
  --mode discussion \
  --questions
```

## Expected Insights
- Disruption potential for each idea
- Blue ocean opportunity mapping
- Remarkability assessment
- Strategic questions for ideation
```

---

## 🎓 Quick Reference Card

### Expert Cheat Sheet

| Expert | Framework | Best For |
|--------|-----------|----------|
| **Christensen** | Disruption, JTBD | Innovation, product strategy |
| **Porter** | Five Forces, Strategy | Competition, positioning |
| **Drucker** | Management, MBO | Organization, goals |
| **Godin** | Marketing, Tribes | Marketing, community |
| **Kim** | Blue Ocean | New markets, differentiation |
| **Collins** | Good to Great | Org excellence, focus |
| **Taleb** | Antifragility | Risk, uncertainty |
| **Meadows** | Systems Thinking | Complex systems, change |
| **Doumont** | Communication | Presentations, docs |

### Mode Cheat Sheet

| Mode | Use When... | Output |
|------|-------------|--------|
| **Discussion** | Exploring, understanding | Balanced synthesis |
| **Debate** | Stress-testing, controversy | Critical analysis |
| **Socratic** | Learning, questioning | Strategic questions |
| **Adaptive** | Unsure | Auto-selected |

### Option Cheat Sheet

| Option | Purpose |
|--------|---------|
| `--experts` | Select specific experts |
| `--mode` | Choose analysis mode |
| `--focus` | Auto-select by domain |
| `--synthesis-only` | Skip details, show synthesis |
| `--structured` | Symbol-based output |
| `--verbose` | Full detailed analysis |
| `--questions` | Generate questions |

---

## 📚 Additional Resources

### Related Commands
- [`/sc:index-repo`](../04-deep-dive/index-repo-analysis.md) - Repository context indexing
- [`/sc:pm`](../04-deep-dive/sc-pm-explained.md) - Project manager agent
- [`/sc:analyze`](../) - Code analysis tools

### Further Reading
- [SuperClaude Commands Guide](../01-setup/skills-system-guide.md)
- [AI Engineering Principles](../02-understand/ai-engineering-principles.md)
- [Multi-Agent Design Patterns](../05-learning_mode_design/commands-vs-skills.md)

---

**Document Version**: 1.0
**Last Updated**: 2025-01-04
**Maintained By**: Claude Code Best Practices Team
