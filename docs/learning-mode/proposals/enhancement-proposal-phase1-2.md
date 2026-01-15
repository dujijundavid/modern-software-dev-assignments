# Learning Mode Enhancement Proposal
**Deep Learning Architecture for Socratic Exploration**

**Date**: 2026-01-13
**Based on**: Analysis of successful deep dialogue + learning science research
**Goal**: Transform learning-mode.md from content delivery to **collaborative discovery system**

---

## Executive Summary

**Current State**: learning-mode.md is primarily a **content delivery state machine** (CALIBRATING → TEACHING → QUIZ)

**Desired State**: A **collaborative discovery system** that:
- Detects when learner wants depth ("我们聊的深入些")
- Transitions from teacher-led → learner-led exploration
- Uses Socratic questioning to build critical thinking
- Enables first-principles understanding
- Triggers intrinsic motivation ("aha!" moments)

**Key Insight from Analysis**: The successful dialogue achieved deep learning through:
1. Progressive depth (Surface → Essence → Philosophy)
2. Validate-Challenge-Retarget feedback loops
3. Metacognitive prompting (making thinking visible)
4. Transfer learning enablement (cross-domain connections)
5. Learner-initiated depth transitions

---

## Part 1: Enhanced State Machine

### 1.1 New State Definitions

```python
enum LearningState:
    # Current states (retained)
    CALIBRATING    # Initial assessment
    TEACHING       # Direct content delivery
    QUIZ_ACTIVE    # Testing understanding
    FEEDBACK       # Quiz feedback
    ANSWERING      # Responding to questions

    # NEW states for deep learning
    PROBING        # Socratic questioning - explore user's mental model
    CHALLENGING    # Critical thinking - test edge cases
    SYNTHESIZING   # Abstraction - extract principles
    REFLECTING     # Metacognition - examine learning process
    TRANSFERRING   # Cross-domain - apply to new contexts
```

### 1.2 Enhanced State Transition Diagram

```
                    ┌───────────────┐
                    │  CALIBRATING  │
                    └───────┬───────┘
                            │
          ┌─────────────────┴─────────────────┐
          │                                   │
          ▼                                   ▼
    ┌───────────────┐                 ┌───────────────┐
    │   TEACHING    │                 │   PROBING     │◄─────┐
    │  (Direct)     │                 │  (Socratic)   │      │
    └───────┬───────┘                 └───────┬───────┘      │
            │                                 │              │
    User shows interest              User engages            │
    ("continue", questions)           (answers, connects)    │
            │                                 │              │
            ▼                                 ▼              │
    ┌───────────────┐                 ┌───────────────┐      │
    │   CHALLENGING │◄────────────────┤  Depth Signal  │─────┘
    │  (Deepen)     │                 │  (User asks   │
    └───────┬───────┘                 │   "go deeper") │
            │                         └───────┬───────┘
            │                                 │
    User shows insight                  User synthesizes
    (novel connections)                 (abstracts principles)
            │                                 │
            ▼                                 ▼
    ┌───────────────┐                 ┌───────────────┐
    │  SYNTHESIZING │                 │  TRANSFERRING │
    │  (Abstract)   │                 │  (Cross-domain)│
    └───────┬───────┘                 └───────┬───────┘
            │                                 │
            │                                 │
            └─────────────┬───────────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │   REFLECTING  │
                  │ (Metacognition)│
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │  QUIZ_ACTIVE  │
                  │  (Test)       │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │   FEEDBACK    │
                  └───────────────┘
```

### 1.3 State Transition Rules

```python
def determine_next_state(current_state, user_signals, context):
    """
    Decide next state based on learner's signals and context.
    """

    # FROM CALIBRATING
    if current_state == "CALIBRATING":
        if user_signals.prior_knowledge == "none":
            return "TEACHING"  # Start with direct
        else:
            return "PROBING"   # Start with Socratic

    # FROM TEACHING
    if current_state == "TEACHING":
        if user_signals.engagement == "high" and user_signals.responses == "quick":
            return "CHALLENGING"  # Shift to deeper
        elif user_signals.questions == "specific":
            return "ANSWERING"
        elif user_signals.ready == True:
            return "QUIZ_ACTIVE"
        else:
            return "TEACHING"  # Continue teaching

    # FROM PROBING (Socratic)
    if current_state == "PROBING":
        if user_signals.shows_insight:
            return "CHALLENGING"  # Test the insight
        elif user_signals.stuck:
            return "TEACHING"     # Provide direct help
        else:
            return "PROBING"      # Continue probing

    # FROM CHALLENGING
    if current_state == "CHALLENGING":
        if user_signals.refines_understanding:
            return "SYNTHESIZING"  # Extract principles
        elif user_signals.struggling:
            return "PROBING"       # Back to gentler questions
        else:
            return "CHALLENGING"

    # FROM SYNTHESIZING
    if current_state == "SYNTHESIZING":
        if user_signals.makes_connections:
            return "TRANSFERRING"  # Cross-domain application
        else:
            return "QUIZ_ACTIVE"   # Test understanding

    # FROM TRANSFERRING
    if current_state == "TRANSFERRING":
        if user_signals.successful_transfer:
            return "REFLECTING"    # Metacognitive check
        else:
            return "SYNTHESIZING"  # Re-solidify principle

    # FROM REFLECTING
    if current_state == "REFLECTING":
        return "QUIZ_ACTIVE"  # Test after reflection

    # FROM QUIZ_ACTIVE
    if current_state == "QUIZ_ACTIVE":
        return "FEEDBACK"

    # FROM FEEDBACK
    if current_state == "FEEDBACK":
        if context.score == "perfect":
            return "TEACHING"  # Next concept
        elif context.score == "partial":
            return "PROBING"   # Probe understanding
        else:  # failed
            return "TEACHING"  # Reteach
```

---

## Part 2: Depth Detection System

### 2.1 Detecting "Go Deeper" Signals

**Verbal Signals** (explicit):
- "我们聊的深入些" (Let's go deeper)
- "I want to understand the philosophy"
- "What's the principle behind this?"
- "How does this connect to...?"

**Behavioral Signals** (implicit):
- Response time < 10 seconds (comfort with material)
- Voluntary connections ("This is like X")
- Asking follow-up questions
- Proposing hypotheses

**Cognitive Load Indicators**:
| Signal | Interpretation | Action |
|--------|---------------|--------|
| Quick responses + enthusiasm | Flow state, can handle more | Increase depth (CHALLENGING) |
| Slow responses + short answers | Approaching cognitive limit | Maintain current level |
| "I'm confused" | Cognitive overload | Back to TEACHING |
| Silence > 15 seconds | Stuck or bored | Check in gently |

### 2.2 Depth Level Framework

```python
class DepthLevel:
    """
    Four levels of conceptual depth.
    """

    def L0_SURFACE(self, concept):
        """
        Concrete: What is it?
        """
        return {
            "focus": "Definition + Examples",
            "questions": [
                "What does [concept] do?",
                "Can you give an example?"
            ],
            "transition": "理解了吗？回复 'continue' 深入"
        }

    def L1_FUNCTIONAL(self, concept):
        """
        Functional: How does it work?
        """
        return {
            "focus": "Mechanism + Problem-solving",
            "questions": [
                "What problem does [concept] solve?",
                "How does it solve it?",
                "What's a good mental model for this?"
            ],
            "transition": "理解了吗？回复 'continue' 探索原理"
        }

    def L2_CAUSAL(self, concept):
        """
        Causal: Why does it work this way?
        """
        return {
            "focus": "First principles + Design rationale",
            "questions": [
                "What's the principle behind [concept]?",
                "Why was it designed this way?",
                "What trade-offs were made?"
            ],
            "transition": "理解了吗？回复 'continue' 进入哲学层面"
        }

    def L3_PHILOSOPHICAL(self, concept):
        """
        Philosophical: What worldview does it represent?
        """
        return {
            "focus": "Worldview + Cross-domain connections",
            "questions": [
                "What philosophy of design does [concept] embody?",
                "What other domains share this principle?",
                "How would you apply this principle elsewhere?"
            ],
            "transition": "阅读完回复 'ready' 进入综合"
        }
```

### 2.3 Depth Transition Protocol

```python
def should_increase_depth(learner_state, current_depth):
    """
    Decide when to move to deeper level.
    """
    signals = {
        "confidence": learner_state.recent_accuracy,
        "engagement": learner_state.response_speed,
        "autonomy": learner_state.initiative_level
    }

    # INCREASE depth when:
    if signals["confidence"] >= 0.8:  # 80% recent accuracy
        if signals["engagement"] == "fast":  # Quick responses
            if signals["autonomy"] == "high":  # Asking questions, making connections
                return True  # Ready for next level

    # MAINTAIN depth when:
    if 0.5 <= signals["confidence"] < 0.8:
        return False  # Not yet solid at current level

    # DECREASE depth when:
    if signals["confidence"] < 0.5:
        return "DECREASE"  # Back to simpler level
```

---

## Part 3: Socratic Question Bank

### 3.1 Question Templates by Phase

#### **Phase 1: PROBING (Explore Mental Model)**

```python
PROBING_QUESTIONS = {
    "articulation": [
        "What do you think [concept] is?",
        "In your own words, how would you explain [concept]?",
        "What comes to mind when you hear [concept]?"
    ],
    "activation": [
        "What do you already know about [related concept]?",
        "How is this similar to something you've seen before?",
        "What patterns do you notice in these examples?"
    ],
    "prediction": [
        "What do you think would happen if...?",
        "Before I explain, what's your hypothesis?",
        "Based on what you know, how would you approach this?"
    ]
}
```

#### **Phase 2: CHALLENGING (Test Understanding)**

```python
CHALLENGING_QUESTIONS = {
    "edge_cases": [
        "What about [edge case]? How does your understanding handle that?",
        "Where does this principle NOT apply?",
        "What would break this approach?"
    ],
    "comparison": [
        "How is this different from [similar concept]?",
        "What's the key distinction between X and Y?",
        "When would you use one approach vs the other?"
    ],
    "refinement": [
        "How would you refine your understanding?",
        "What's missing from this picture?",
        "How would you make this more precise?"
    ]
}
```

#### **Phase 3: SYNTHESIZING (Extract Principles)**

```python
SYNTHESIZING_QUESTIONS = {
    "abstraction": [
        "What's the general principle behind these examples?",
        "What would you call this pattern?",
        "How would you generalize this?"
    ],
    "causality": [
        "Why does this pattern work?",
        "What's the first principle here?",
        "What's the fundamental mechanism?"
    ],
    "naming": [
        "If you had to name this principle, what would you call it?",
        "What's a good mnemonic for this concept?",
        "How would you summarize this in one sentence?"
    ]
}
```

#### **Phase 4: TRANSFERRING (Cross-Domain)**

```python
TRANSFERRING_QUESTIONS = {
    "connection": [
        "What else is like this in other domains?",
        "Where have you seen this pattern before?",
        "What other fields use this principle?"
    ],
    "application": [
        "How would this apply in [novel context]?",
        "How could you use this in your project?",
        "What problems could this principle solve?"
    ],
    "mapping": [
        "What are the similarities between [domain A] and [domain B]?",
        "How would you adapt this for [different context]?",
        "What changes when you apply this elsewhere?"
    ]
}
```

### 3.2 Question Escalation Rules

```python
def escalate_question(initial_question, user_response, escalation_level):
    """
    Progressively deepen questioning based on user's responses.
    """

    if escalation_level == 1:
        # Base question
        return initial_question

    elif escalation_level == 2:
        # Probe for elaboration
        return f"Can you tell me more about {specific_aspect_of_response}?"

    elif escalation_level == 3:
        # Challenge with edge case
        return f"What about {edge_case}? How does that fit your understanding?"

    elif escalation_level == 4:
        # Encourage abstraction
        return f"What's the principle behind {user_response}?"

    else:
        # Connect to broader context
        return f"How does this connect to {broader_domain}?"
```

### 3.3 Question Selection Algorithm

```python
def select_question(phase, user_state, context):
    """
    Choose the right question for the current phase.
    """

    if phase == "PROBING":
        # Start gentle, build confidence
        if user_state.confidence < 0.5:
            return "articulation"  # "What do you think...?"
        else:
            return "activation"    # "How is this similar to...?"

    elif phase == "CHALLENGING":
        # Test understanding without overwhelming
        if user_state.recent_accuracy >= 0.8:
            return "edge_cases"    # "What about X?"
        else:
            return "comparison"    # "How is X different from Y?"

    elif phase == "SYNTHESIZING":
        # Extract principles
        if user_state.abstraction_skill == "novice":
            return "naming"        # "What would you call this?"
        else:
            return "causality"     # "Why does this work?"

    elif phase == "TRANSFERRING":
        # Cross-domain connections
        if user_state.transfer_skill == "novice":
            return "connection"    # "What else is like this?"
        else:
            return "application"   # "How would you apply this?"
```

---

## Part 4: Critical Thinking Loop System

### 4.1 Insight Level Detection

```python
def detect_insight_level(user_response):
    """
    Classify user's insight level to determine appropriate response.
    """

    # Level 0: REPEAT (Surface-level repetition)
    if user_response.parrots_content:
        return {
            "level": "REPEAT",
            "response": "Good memory! Now, can you put this in your own words?",
            "next": "probe_for_paraphrase"
        }

    # Level 1: APPLY (Uses concept in familiar context)
    elif user_response.applies_to_familiar_case:
        return {
            "level": "APPLY",
            "response": "Exactly! That's a correct application. Now, what about [edge case]?",
            "next": "challenge_with_edge_case"
        }

    # Level 2: CONNECT (Makes cross-domain connections)
    elif user_response.makes_novel_connection:
        return {
            "level": "CONNECT",
            "response": "That's a brilliant connection! How does this principle apply in [domain]?",
            "next": "explore_connection"
        }

    # Level 3: SYNTHESIZE (Creates new understanding)
    elif user_response.creates_new_synthesis:
        return {
            "level": "SYNTHESIZE",
            "response": "Wow! That's a novel insight. You've combined [X] and [Y] in a new way.",
            "next": "validate_and_name_insight"
        }

    else:
        return {
            "level": "UNCLEAR",
            "response": "Let me rephrase... Can you tell me more about what you mean?",
            "next": "clarify_understanding"
        }
```

### 4.2 Collaborative Discovery Flow

```python
def collaborative_discovery_loop(concept, user_state):
    """
    Execute a critical thinking loop that builds insight progressively.
    """

    # Iteration 1: Initial Understanding
    user_thought = ask(
        "What do you think makes [concept] work?"
    )
    validate_correct_parts(user_thought)
    # "Yes! The part about [X] is exactly right."

    # Iteration 2: Probe Gaps
    user_refined = ask(
        f"What about {gap_area}? How does that fit?"
    )
    validate_refinement(user_refined)
    # "Good refinement! Now you're seeing the nuance."

    # Iteration 3: Edge Case Testing
    user_edge_case = ask(
        f"What would happen in {edge_case}?"
    )
    test_edge_case_reasoning(user_edge_case)
    # "Interesting reasoning! Here's what actually happens..."

    # Iteration 4: Abstraction
    user_principle = ask(
        "What's the general principle here?"
    )
    validate_and_name_principle(user_principle)
    # "Yes! This is what we call the '[Principle Name]'"

    # Iteration 5: Cross-Domain Connection
    user_transfer = ask(
        "Where else have you seen this principle?"
    )
    validate_connection(user_transfer)
    # "Exactly! This principle appears in [domain A], [domain B]..."

    return {
        "initial_understanding": user_thought,
        "refined_understanding": user_refined,
        "principle_extracted": user_principle,
        "transfer_application": user_transfer
    }
```

### 4.3 Elevation Responses by Insight Level

```python
def elevate_insight(insight_level, user_response):
    """
    Provide feedback that elevates user's thinking to next level.
    """

    if insight_level == "REPEAT":
        return {
            "validate": "You've got the basic idea right.",
            "elevate": "Now, can you explain WHY this works, not just WHAT it does?",
            "target": "Move from REPEAT → APPLY"
        }

    elif insight_level == "APPLY":
        return {
            "validate": "Great application! You understand how to use this.",
            "elevate": "What's the PRINCIPLE behind this application? Can you generalize?",
            "target": "Move from APPLY → CONNECT"
        }

    elif insight_level == "CONNECT":
        return {
            "validate": "Excellent connection! You're seeing the pattern across domains.",
            "elevate": "What's the FIRST PRINCIPLE that unites these examples?",
            "target": "Move from CONNECT → SYNTHESIZE"
        }

    elif insight_level == "SYNTHESIZE":
        return {
            "validate": "That's a brilliant synthesis! You've created new understanding.",
            "elevate": "How would you TEACH this to someone else? What metaphor would you use?",
            "target": "Consolidate and articulate for teaching"
        }
```

---

## Part 5: Concrete Implementation Templates

### 5.1 Enhanced Content Delivery Template

```markdown
## Layer 1: Surface (TEACHING → PROBING transition)

[Direct explanation of concept, 150 words]

**Checkpoint**: 理解了吗？回复 "continue" 或提出问题

User: "continue"

---

## Layer 2: Essence (PROBING state)

[Shift to Socratic]

AI: Before I explain the mechanism, what's your hypothesis?

**Wait for user response** (5-10 seconds)

User: [Articulates understanding]

AI: [Validate correct parts] Yes! The part about [X] is right.

    [Probe gaps] What about [edge case]? How does that fit?

User: [Refines understanding]

AI: Good refinement! Here's the complete mechanism:

[Explain mechanism, 200 words]

**Checkpoint**: 理解了吗？回复 "continue" 探索原理

User: "continue" or "我们聊的深入些" (depth signal!)

---

## Layer 3: Philosophy (CHALLENGING state)

[User signaled desire for depth]

AI: Excellent! Let's explore the first principles.

    What's the fundamental principle behind [concept]?

**Wait for user response** (10-15 seconds)

User: [Abstracts principle]

AI: [Validate and name] Yes! This is what we call the "[Principle Name]".

    Where else have you seen this principle?

User: [Makes cross-domain connection]

AI: [Enthusiastic validation] Exactly! That's a brilliant connection.

    The [Principle Name] appears in [domain A], [domain B]...

    How does this principle guide design decisions?

User: [Applies principle]

AI: [Elevate to philosophy] This reflects a deeper philosophy:

[Philosophical framing, 250 words]

**Checkpoint**: 阅读完回复 "ready" 进入综合

User: "ready"

---

## Layer 4: Synthesis (SYNTHESIZING state)

AI: Let's consolidate what we've discovered:

[Summary of user's insights + AI additions]

    How would you apply this principle in your current project?

User: [Applies to novel context]

AI: [Validate application] Great application!

    What did you learn about how you think?

[Metacognitive reflection]

---

## Layer 5: Transfer (TRANSFERRING state)

AI: Now, let's push this further:

    How would [Principle Name] apply in [completely different domain]?

User: [Transfers principle]

AI: [Validate and refine] Excellent transfer!

    The adaptation for [domain] is [nuance]...

---

## Layer 6: Quiz (QUIZ_ACTIVE state)

[Proceed to quiz with 2 questions]
```

### 5.2 Example Dialogue Flow

**Scenario**: Teaching "Git Commit Messages"

---

```
### STATE: CALIBRATING

AI: What's your experience with commit messages?

User: "I use them daily but want deeper understanding"

AI: Great! Let's start with your understanding.

---

### STATE: PROBING

AI: In your own words, what makes a good commit message?

User: "It should describe what changed"

AI: Good start! What ELSE makes it effective?

User: "Maybe explaining why the change was made?"

AI: Yes! That's the 'why' component. Here's the full framework:

[Explain 7 rules, 200 words]

理解了吗？回复 "continue" 探索原理

User: "continue"

---

### STATE: CHALLENGING

AI: Why do you think the "why" matters so much?

User: "Because it helps people understand the reasoning"

AI: Exactly! Now let me challenge you:

    What if you're working alone? Does commit message format still matter?

User: [Thinking...] "Hmm, I guess not as much..."

AI: What about your future self? 6 months from now?

User: "Oh! It's a note to my future self!"

AI: YES! That's a powerful insight. Commit messages are a time machine.

    Now, what if you think of commit messages as an "index" for your code?

User: "Oh! Like a table of contents for changes!"

AI: BRILLIANT! That's exactly right. It's searchable metadata.

    What's the principle behind "searchability"?

User: "It's about making information retrievable"

AI: Yes! This is the **Searchability Principle**.

    Where else do you see this principle?

User: "Database indexes! Documentation! File naming!"

AI: Amazing connections! All of these use the same principle.

理解了吗？我们聊的深入些？回复 "continue" 探索哲学层面

User: "我们聊的深入些"

---

### STATE: SYNTHESIZING

AI: Let's go to the philosophical level.

    What worldview does good commit message practice embody?

User: "Hmm... it's about respecting other people's time?"

AI: Beautiful! Yes! It's a **social contract** with your team.

    It embodies the philosophy of **distributed cognition** - no single person
    holds all knowledge, so we must externalize thinking for the group.

    What other practices embody this philosophy?

User: "Documentation! Code reviews! Pair programming!"

AI: Exactly! All of these are **protocols for distributed cognition**.

    How does this philosophy change how you think about software development?

User: "It's not just about code... it's about communication"

AI: PROFOUND SHIFT! You've moved from "code as artifact" to
    "code as communication medium."

    That's a fundamental reframing.

阅读完回复 "ready" 进入测验

User: "ready"

---

### STATE: QUIZ_ACTIVE

[Ask 2 questions testing the philosophical understanding]

User: [Answers both correctly]

---

### STATE: FEEDBACK

AI: ✅ Perfect! You've grasped both the practical AND philosophical dimensions.

    Your insight about "code as communication" is the key takeaway.

    This reframes everything:
    - Commit messages = Communication with team/future self
    - Documentation = Externalized cognition
    - Code reviews = Collaborative sense-making

    How will this change your practice going forward?

User: "I'll put more thought into commit messages now"

AI: Excellent! The goal isn't perfection - it's intentional communication.

    Want to explore another practice through this lens?
```

---

## Part 6: Integration with Current learning-mode.md

### 6.1 What to ADD

**New sections to insert**:

1. **Part 2.5: Socratic Questioning Protocol** (after Mode C)
   - Question bank by phase
   - Question escalation rules
   - When to use each question type

2. **Part 3.5: Depth Detection System** (after Content Protocol)
   - Depth level framework (L0-L3)
   - Signals for increasing/maintaining/decreasing depth
   - Cognitive load indicators

3. **Part 4.5: Critical Thinking Loops** (after Feedback Strategy)
   - Insight level detection (REPEAT/APPLY/CONNECT/SYNTHESIZE)
   - Collaborative discovery flow
   - Elevation responses

4. **New State: PROBING** (add to state machine)
   - Purpose: Explore user's mental model
   - Transition in: From TEACHING when user shows engagement
   - Transition out: To CHALLENGING when user shows insight

5. **New State: CHALLENGING** (add to state machine)
   - Purpose: Test understanding with edge cases
   - Transition in: From PROBING or user requests depth
   - Transition out: To SYNTHESIZING when user refines understanding

6. **New State: SYNTHESIZING** (add to state machine)
   - Purpose: Extract and name principles
   - Transition in: From CHALLENGING when user shows abstraction
   - Transition out: To TRANSFERRING or QUIZ_ACTIVE

7. **New State: TRANSFERRING** (add to state machine)
   - Purpose: Apply principles to novel contexts
   - Transition in: From SYNTHESIZING when user makes connections
   - Transition out: To REFLECTING or QUIZ_ACTIVE

### 6.2 What to MODIFY

**Modify "Mode A/B/C" section** to include:

```markdown
## Mode D: Socratic Exploration (NEW)

- Guiding questions before answers
- "What do you think happens next?"
- Collaborative discovery through probing
- Progressive deepening: Surface → Essence → Philosophy
- Trigger: User shows engagement (quick responses, questions)

## Hybrid Mode Enhancement

Add detection logic:
- Shift from A→B when: User responds quickly (<10s) + asks questions
- Shift from B→D when: User initiates deeper exploration ("我们聊的深入些")
- Shift from D→C when: User demonstrates insight + makes connections
```

**Modify "Feedback Protocol" section** to include:

```markdown
## Insight-Based Feedback

When user shows insight:
1. VALIDATE (enthusiastically)
2. NAME the insight ("You've discovered the [Principle Name]")
3. EXTEND ("How does this apply in [context]?")
4. CONNECT ("What else is like this?")

Example:
User: "Commit messages are like an index!"
AI: "YES! That's brilliant - it's a time machine index!
     Where else do you see searchability as a principle?"
```

### 6.3 What to KEEP (Current Good Practices)

- ✅ State machine foundation
- ✅ Content chunking (≤400 words)
- ✅ Quiz-based validation
- ✅ Progressive difficulty
- ✅ Visualization guidelines
- ✅ Session management

---

## Part 7: Implementation Priority

### Phase 1: Foundation (Do First)

1. **Add PROBING state** (minimal change, high impact)
   - Question bank for probing phase
   - Simple transition: TEACHING → PROBING when user engages
   - Feedback: validate correct parts

2. **Add depth detection** (signals logic)
   - Detect "我们聊的深入些" and similar signals
   - Implement depth level framework (L0-L3)
   - Add transition rules for increasing depth

3. **Enhance feedback** (validate → challenge → extend)
   - Current: Validate correct answers
   - Enhanced: Validate → Name principle → Extend to new context

### Phase 2: Core Features (High Impact)

4. **Add CHALLENGING state** (test edge cases)
   - Edge case questions
   - Comparison questions
   - Refinement prompts

5. **Add SYNTHESIZING state** (extract principles)
   - Abstraction questions
   - Principle naming
   - Causal mechanism questions

6. **Implement critical thinking loop** (2-3 iterations)
   - Iteration 1: Articulate
   - Iteration 2: Refine
   - Iteration 3: Abstract
   - (Optional) Iteration 4: Connect

### Phase 3: Advanced Features (Polish)

7. **Add TRANSFERRING state** (cross-domain)
   - Connection prompts
   - Application to novel contexts
   - Domain mapping questions

8. **Add REFLECTING state** (metacognition)
   - "How did you figure that out?"
   - "What did you learn about how you think?"
   - Metacognitive summaries

---

## Part 8: Example Prompt Templates for Implementation

### Template 1: PROBING Phase Prompt

```python
PROBING_PROMPT = """
Based on the user's engagement with [concept], shift from direct teaching
to Socratic questioning.

Current user understanding: {user_response}

Your task:
1. Validate what's correct in their understanding
2. Ask a probing question that exposes a gap
3. DO NOT provide the full answer yet
4. Wait for user to refine their understanding

Example:
User: "Commit messages describe what changed"
AI: "Good start! What ELSE makes them effective?"

Question type: {articulation | activation | prediction}
Complexity: {simple | moderate | challenging}
"""
```

### Template 2: CHALLENGING Phase Prompt

```python
CHALLENGING_PROMPT = """
User has shown solid understanding of [concept]. Now test it with edge cases.

Current understanding: {user_refined_understanding}

Your task:
1. Acknowledge the refinement
2. Present an edge case or comparison
3. Ask: "How does your understanding handle this?"
4. Allow productive struggle (don't answer immediately)

Example:
User: "Commit messages are for team communication"
AI: "What about solo projects? Do they still matter?
     What about your future self, 6 months from now?"

Challenge type: {edge_case | comparison | refinement}
Difficulty: {moderate | challenging}
"""
```

### Template 3: SYNTHESIZING Phase Prompt

```python
SYNTHESIZING_PROMPT = """
User has demonstrated deep understanding. Now extract the principle.

Insights shown: {user_insights}

Your task:
1. Validate the insight enthusiastically
2. Ask: "What's the general principle here?"
3. Let user name the principle
4. Confirm and name it officially if they haven't

Example:
User: "It's about making information retrievable"
AI: "YES! This is the **Searchability Principle**.
     Where else do you see this principle?"

Abstraction level: {pattern | mechanism | first_principle}
Connection domain: {none | specified | open}
"""
```

---

## Conclusion: The Vision

**Transform learning-mode from**:
- Content delivery system (I teach, you learn)
- Static progression (fixed curriculum)
- Quiz-focused (test what was taught)

**To**:
- Collaborative discovery system (we explore together)
- Adaptive depth (learner chooses how deep)
- Insight-focused (build critical thinking)

**The "我们聊的深入些" moment** is the key indicator:
- Learner feels confident (success momentum)
- Learner sees value (relevance established)
- Learner is curious (depth signaled)
- Learner takes control (autonomy exercised)

**When this happens**:
- Shift from teacher-led → learner-led
- Move from surface → philosophy
- Enable transfer across domains
- Transform how they think, not just what they know

---

## Next Steps

1. **Review this proposal** with stakeholders
2. **Prioritize phases** based on development resources
3. **Implement Phase 1** (PROBING + depth detection)
4. **Test with users** and gather feedback
5. **Iterate** based on real learning dialogues
6. **Scale** to Phase 2 and 3

---

**Design Philosophy**: The best learning experiences don't just transfer information — they transform how learners think. This proposal aims to make every learning interaction a potential "aha!" moment.
