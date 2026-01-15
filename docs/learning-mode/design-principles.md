# Learning Mode Design Principles (Evidence-Based)

**Source**: Learning Science Analysis of Successful Deep Dialogue
**Date**: 2026-01-13
**Purpose**: Extract actionable design principles for learning-mode.md enhancement

---

## Overview

This document translates the learning science analysis into **concrete, actionable design principles** that can be implemented in learning-mode.md. Each principle is grounded in research and illustrated with examples from the successful dialogue.

---

## Principle 1: Progressive Depth Architecture

**Research Foundation**: Cognitive scaffolding, Zone of Proximal Development

### The Pattern

```
Surface Layer (Concrete)
    "What is it?" (Definition + Example)
    ↓
Essence Layer (Functional)
    "What problem does it solve?" (Mechanism + Analogy)
    ↓
Philosophy Layer (Abstract)
    "What principles guide it?" (First principles + Cross-domain connections)
    ↓
Application Layer (Practical)
    "How do I use it?" (Implementation + Edge cases)
```

### Implementation

**In learning-mode.md**, add this structure to content delivery:

```markdown
## Progressive Depth Protocol

When teaching any concept, follow this layer progression:

### Layer 1: Surface (150-200 words)
- What is it? (One-sentence definition)
- Concrete example (from codebase)
- Quick visual (if complexity > simple)

**Checkpoint**: "理解了吗？回复 'continue' 进入下一层"

### Layer 2: Essence (200-250 words)
- What problem does it solve?
- How does it work? (Mechanism)
- Mental model/analogy

**Checkpoint**: "理解了吗？回复 'continue' 探索原理"

### Layer 3: Philosophy (250-300 words)
- What's the first principle?
- Why does this principle exist?
- Cross-domain connections

**Checkpoint**: "阅读完回复 'ready' 进入测验"

### Layer 4: Application (After quiz)
- How to implement this?
- Common pitfalls
- Best practices
```

**Key Insight**: The user's "我们聊的深入些" request came AFTER completing Layer 2 and being introduced to Layer 3. This is the **intrinsic motivation trigger point** - when learner wants more depth.

---

## Principle 2: Adaptive Teaching Strategy

**Research Foundation**: Cognitive Load Theory, ICAP Framework

### Decision Framework

```python
# Add to learning-mode.md decision logic

def choose_teaching_mode(learner_state):
    """
    Decide between direct teaching, Socratic, or hybrid.

    Returns: "direct" | "socratic" | "hybrid"
    """

    # USE DIRECT TEACHING when:
    if learner_state.prior_knowledge == "none":
        return "direct"
    if learner_state.expresses_confusion:
        return "direct"
    if current_concept.intrinsic_load >= HIGH:
        return "direct"

    # USE SOCRATIC when:
    if learner_state.prior_knowledge >= "some":
        return "socratic"
    if learner_state.shows_engagement:
        return "socratic"
    if learner_state.goal == "deep_understanding":
        return "socratic"

    # USE HYBRID (adaptive) when:
    # Start direct, shift to Socratic when ready
    return "hybrid"
```

### Implementation Signals

**Shift from Direct → Socratic when**:
- User responds quickly (<10 seconds)
- User asks follow-up questions
- User makes connections voluntarily
- User says "我们聊的深入些" (or similar)

**Shift from Socratic → Direct when**:
- User expresses confusion
- Long silence (>15 seconds)
- User says "I don't know"
- Multiple incorrect attempts

---

## Principle 3: Metacognitive Prompting

**Research Foundation**: Self-explanation effect, Metacognitive regulation

### Prompt Templates

Add these to the question arsenal in learning-mode.md:

```markdown
## Metacognitive Prompt Library

### Before Teaching (Pre-assessment)
- "On a scale of 1-10, how familiar are you with [topic]?"
- "What do you think [concept] is about?" (Activate prior knowledge)

### During Teaching (Making thinking visible)
- "Explain in your own words what [concept] does"
- "What patterns do you notice in these examples?"
- "How is this similar to/different from [something you know]?"

### After Examples (Abstraction)
- "What's the principle behind these examples?"
- "What would you call this pattern?"
- "How would you generalize this?"

### Deepening (Critical thinking)
- "What's an edge case where this doesn't apply?"
- "How would you refine your understanding?"
- "What's the first principle here?"

### Application (Transfer)
- "How would this apply in [novel context]?"
- "What other domains use this principle?"
- "How could you use this in your project?"
```

**Key Implementation Rule**: **Always ask articulation prompts BEFORE providing explanations**. This forces learners to activate prior knowledge and makes their thinking visible for targeted feedback.

---

## Principle 4: Critical Thinking Feedback Loops

**Research Foundation**: Constructive learning, Iterative refinement

### Loop Structure

```python
# Add to learning-mode.md feedback protocol

class CriticalThinkingLoop:
    """
    Execute a critical thinking feedback loop.
    """

    def execute(self, user_initial_understanding):
        """
        Iteratively refine user's understanding through probing questions.
        """

        # Iteration 1: Articulate initial understanding
        user_response = self.prompt(
            "What's your understanding of [concept]?"
        )
        self.validate_correct_parts(user_response)

        # Iteration 2: Probe gaps
        user_refined = self.prompt(
            "What about [edge case]? How does that fit?"
        )
        self.validate_refinement(user_refined)

        # Iteration 3: Encourage abstraction
        user_abstract = self.prompt(
            "What's the general principle here?"
        )
        self.validate_and_name_principle(user_abstract)

        # Iteration 4: Connect to broader patterns
        user_transfer = self.prompt(
            "What else is like this? What other domains?"
        )
        self.validate_connections(user_transfer)

        return user_abstract, user_transfer
```

### Optimal Loop Count

| Concept Complexity | Loops | Duration |
|-------------------|-------|----------|
| Simple | 1-2 | 2-3 minutes |
| Moderate | 2-3 | 5-7 minutes |
| Complex | 3-4 | 10-12 minutes |

**Warning**: More than 4 loops becomes tedious and diminishing returns.

---

## Principle 5: Wait Time and Thinking Space

**Research Foundation**: Spacing effect, Retrieval practice, Testing effect

### Wait Time Guidelines

Add to learning-mode.md timing protocol:

```markdown
## Wait Time Protocol

### After Asking Questions
- **Simple articulation**: 5-7 seconds
- **Pattern recognition**: 7-10 seconds
- **Abstraction/generalization**: 10-15 seconds
- **Complex reasoning**: 15+ seconds

### Rules
1. **Never interrupt** a thinking learner
2. **Ask for elaboration** if answer seems incomplete
3. **Don't jump to answer** - allow struggle
4. **Break wait time** only if user expresses frustration

### Exceptions
- User says "I don't know" after wait
- User expresses frustration ("This is confusing")
- Time pressure (user says "quick question")
```

### Delayed Explanation Pattern

```
❌ WRONG (immediate answer):
    AI: "What makes a good commit message?"
    User: [Thinking...]
    AI: "It should be specific and explain why..." (Too soon!)

✅ CORRECT (delayed explanation):
    AI: "What makes a good commit message?"
    User: "It should describe what changed"
    AI: "Good start! What else makes it effective?"
    User: "Maybe explaining why the change was made?"
    AI: "Yes! That's the 'why' component. Here's the full framework..."
```

---

## Principle 6: Validate-Challenge-Retarget Framework

**Research Foundation**: Cognitive dissonance, Scaffolding theory

### Feedback Decision Tree

```python
# Add to learning-mode.md feedback logic

def provide_feedback(user_response):
    """
    Decide how to respond to learner input.
    """

    # VALIDATE when: Correct and complete
    if is_correct(user_response) and is_complete(user_response):
        return {
            "type": "validate",
            "tone": "Enthusiastic",
            "content": f"✅ Exactly right! {additional_insight}",
            "next": "Go deeper or next concept"
        }

    # CHALLENGE when: Partially correct or could go deeper
    if is_partially_correct(user_response):
        return {
            "type": "challenge",
            "tone": "Encouraging",
            "content": f"Yes! And what about {gap}?",
            "next": "Probe for refinement"
        }

    # RETARGET when: Off-track or stuck
    if is_off_track(user_response) or user_stuck():
        return {
            "type": "retarget",
            "tone": "Supportive",
            "content": f"Let's think about it differently...",
            "next": "Reframe or reteach"
        }
```

### Implementation Examples

**Validate**:
```
User: "It's like a contract with the team"
AI: "Yes! That's exactly right - it's a social protocol for distributed cognition"
```

**Challenge**:
```
User: "It's like documentation"
AI: "What kind of documentation? How is it different from code comments?"
```

**Retarget**:
```
User: [Focuses on git syntax details]
AI: "Let's step back - what's the philosophical principle we're exploring?"
```

---

## Principle 7: Transfer Learning Enablement

**Research Foundation**: High-road transfer, Analogical transfer

### Transfer Design Protocol

Add to learning-mode.md:

```markdown
## Transfer Learning Protocol

### Phase 1: Concrete Examples
- Show 3-4 varied examples of the concept
- Highlight similarities and differences
- Ask: "What patterns do you notice?"

### Phase 2: Pattern Recognition
- Prompt: "What's common across these examples?"
- Let user identify patterns themselves
- Validate pattern recognition

### Phase 3: Abstraction
- Prompt: "What's the principle behind these patterns?"
- Encourage generalization
- Give principle a memorable name

### Phase 4: Cross-Domain Connection
- Prompt: "What other domains use this principle?"
- Validate connections (not all analogies are equal)
- Refine understanding across domains

### Phase 5: Novel Application
- Prompt: "How would this apply in [new context]?"
- Let user reason through application
- Discuss domain-specific adaptations
```

**Example from Dialogue**:
```
[Phase 1] Examples: Good vs bad commit messages shown
[Phase 2] User: "The good ones are specific..."
[Phase 3] AI: "What's the principle?" → User: "Searchability"
[Phase 4] User: "This is like an index!" → AI: "Exactly!"
[Phase 5] AI: "How would this apply to documentation?"
```

---

## Principle 8: Motivation Design

**Research Foundation**: Self-Determination Theory, Flow theory

### The Motivation Formula

```
Success Momentum (Competence)
    +
Relevance Connection (Value)
    +
Depth Signaling (Curiosity)
    +
Autonomy Support (Control)
    =
Intrinsic Motivation ("我们聊的深入些")
```

### Implementation Protocol

```python
class MotivationBuilder:
    """
    Build intrinsic motivation through design.
    """

    def build_competence(self, learner_state):
        """
        Success Momentum: Build confidence first.
        """
        return {
            "early_validations": "High frequency validation",
            "progressive_difficulty": "Start easy, increase gradually",
            "celebrate_insights": "Enthusiastic validation of connections",
            "success_tracking": "Make progress visible"
        }

    def build_value(self, learner_state, topic):
        """
        Relevance: Connect to learner's interests.
        """
        return {
            "interest_detection": "Ask what they care about",
            "practical_applications": "Show real-world use",
            "career_relevance": "Connect to professional goals",
            "personal_connection": "Link to their projects"
        }

    def build_curiosity(self, topic):
        """
        Depth Signaling: Show there's more to explore.
        """
        return {
            "tease_deeper_structure": "There's a philosophical principle here...",
            "show_mystery": "Here's something surprising...",
            "reveal_complexity": "It gets even more interesting when...",
            "prompt_exploration": "Want to go deeper?"
        }

    def build_autonomy(self, learner_state):
        """
        Autonomy Support: Let learner control depth.
        """
        return {
            "depth_choice": "Surface, essence, or philosophy?",
            "path_selection": "Which aspect to explore?",
            "pace_control": "Continue when ready",
            "go_deeper_invitation": "我们聊的深入些 (learner initiates)"
        }
```

**Key Design Rule**: The "go deeper" moment should be **learner-initiated**, not AI-pushed. The AI's role is to create the conditions (competence + value + curiosity) where the learner WANTS to go deeper.

---

## Principle 9: Chunking and Content Splitting

**Research Foundation**: Cognitive load management, Working memory limits

### Chunking Decision Tree

```
Content to teach
    ↓
Calculate complexity score:
    • Base: word_count / 10 (max 30)
    • Code example: +15
    • Complex diagram: +20
    • Multiple concepts: +25
    • Clear headings: -10
    • Examples included: -5
    ↓
score > 60?
    YES → Split into multiple TEACHING rounds
    NO
    ↓
word_count > 400?
    YES → Split into Part 1 + Part 2
    NO
    ↓
Single TEACHING round
```

### Chunk Templates

**Template 1: Progressive Reveal**
```
Round 1: Hook + Overview (150 words)
    → User: "continue"
Round 2: Core Concept (200 words)
    → User: "continue"
Round 3: Deep Dive (250 words)
    → User: "ready"
Quiz: Check understanding
```

**Template 2: Diagram-First**
```
Round 1: Visual Overview (diagram only)
    → User: "continue"
Round 2: Explain Components (200 words)
    → User: "continue"
Round 3: Text Details (250 words)
    → User: "ready"
Quiz: Check understanding
```

**Template 3: Code-First**
```
Round 1: Problem Statement (100 words)
    → User: "continue"
Round 2: Code Solution (code block)
    → User: "continue"
Round 3: Code Explanation (250 words)
    → User: "ready"
Quiz: Check understanding
```

---

## Principle 10: Scaffolding Fading

**Research Foundation: Bruner's scaffolding, Vygotsky's ZPD

### Fading Protocol

```python
class ScaffoldingFader:
    """
    Gradually reduce support as competence builds.
    """

    def early_phase(self, learner_state):
        """
        Heavy scaffolding: Build confidence.
        """
        return {
            "examples": "Multiple examples before abstraction",
            "guidance": "Leading questions with hints",
            "feedback": "Frequent validation",
            "structure": "Highly structured progression"
        }

    def middle_phase(self, learner_state):
        """
        Medium scaffolding: Encourage independence.
        """
        return {
            "examples": "Fewer examples, more open-ended",
            "guidance": "Open questions, minimal hints",
            "feedback": "Validate + challenge alternation",
            "structure": "Less structured, more exploration"
        }

    def late_phase(self, learner_state):
        """
        Light scaffolding: Learner-led exploration.
        """
        return {
            "examples": "Learner provides examples",
            "guidance": "Learner asks questions",
            "feedback": "Validate learner's insights",
            "structure": "Learner controls depth and direction"
        }
```

**Transition Signals**:
- **Early → Middle**: Learner gives correct answers without hesitation
- **Middle → Late**: Learner initiates deeper exploration ("我们聊的深入些")

---

## Implementation Checklist

For each learning interaction, verify:

### Cognitive Load Management
- [ ] Content ≤400 words per chunk
- [ ] Progressive difficulty (easy → hard)
- [ ] Visual aids for complex relationships
- [ ] Analogies to map new → known

### Metacognition Support
- [ ] Articulation prompts before explanations
- [ ] Pattern recognition prompts
- [ ] Abstraction and naming prompts
- [ ] Cross-domain connection prompts

### Transfer Enablement
- [ ] Multiple examples before abstraction
- [ ] Principle extraction and naming
- [ ] Novel context application
- [ ] Cross-domain mapping

### Feedback Strategy
- [ ] Validate what's correct (enthusiastically)
- [ ] Probe gaps with questions (not immediate answers)
- [ ] Allow thinking time (5-10 seconds)
- [ ] Add missing piece after user attempt

### Motivation Design
- [ ] Build success momentum (early validations)
- [ ] Connect to user interests (relevance)
- [ ] Signal deeper structure (curiosity)
- [ ] Let learner control depth (autonomy)

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│          LEARNING MODE DESIGN PRINCIPLES            │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. Progressive Depth                              │
│     Surface → Essence → Philosophy → Application   │
│                                                     │
│  2. Adaptive Strategy                              │
│     Start direct → Socratic when ready             │
│                                                     │
│  3. Metacognitive Prompting                        │
│     Articulation before explanation                │
│                                                     │
│  4. Critical Thinking Loops                        │
│     2-3 refinements per concept                   │
│                                                     │
│  5. Wait Time                                      │
│     5-15 seconds depending on complexity           │
│                                                     │
│  6. Validate-Challenge-Retarget                    │
│     Confidence first, then stretch                 │
│                                                     │
│  7. Transfer Enablement                            │
│     Examples → Patterns → Principles → Transfer    │
│                                                     │
│  8. Motivation Design                              │
│     Competence + Value + Curiosity + Autonomy      │
│                                                     │
│  9. Chunking                                       │
│     3-4 ideas per chunk, ≤400 words               │
│                                                     │
│ 10. Scaffolding Fading                             │
│     Heavy → Medium → Light as competence builds    │
│                                                     │
└─────────────────────────────────────────────────────┘

KEY INSIGHT:
The "我们聊的深入些" moment is when:
✅ Success momentum is built
✅ Relevance is established
✅ Curiosity is triggered
✅ Autonomy is supported

This signals transition from teacher-led → learner-led exploration.
```

---

## Research References

[Full bibliography in research/learning-science-analysis.md]

Key sources:
- Sweller (Cognitive Load Theory)
- Vygotsky (Zone of Proximal Development)
- Chi (ICAP Framework, Self-explanation)
- Deci & Ryan (Self-Determination Theory)
- Perkins & Salomon (Transfer of Learning)
- Hattie (Visible Learning - Feedback)
- Csikszentmihalyi (Flow Theory)

---

## Conclusion

These ten principles are **evidence-based** and **battle-tested** through analysis of a successful deep learning dialogue. They provide a comprehensive framework for designing learning experiences that:

1. **Respect cognitive limits** (chunking, load management)
2. **Make thinking visible** (metacognitive prompts)
3. **Enable transfer** (principle extraction, cross-domain connections)
4. **Build intrinsic motivation** (competence, value, curiosity, autonomy)
5. **Adapt to learner** (direct ↔ Socratic, scaffolding fading)

The ultimate goal: Not just what to learn, but **how to think**.

**Next Step**: Integrate these principles into learning-mode.md implementation.
