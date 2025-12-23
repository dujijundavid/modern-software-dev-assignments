from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv
import logging

# TODO 3: Replaced print statements with proper logging
logger = logging.getLogger(__name__)

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    """Check if a line looks like an action item based on format and content."""
    stripped = line.strip().lower()
    if not stripped:
        return False
    
    # Must have some format indicator
    has_format = (
        BULLET_PREFIX_PATTERN.match(stripped) or
        any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES) or
        "[ ]" in stripped or "[todo]" in stripped
    )
    
    if not has_format:
        return False
    
    # TODO 3: Additional filtering - must look like actionable content
    # Filter out non-actionable content
    if len(stripped) < 3:  # Too short
        return False
    
    # Remove format markers to check content
    content = BULLET_PREFIX_PATTERN.sub("", stripped)
    content = content.replace("[ ]", "").replace("[todo]", "").strip()
    
    # Filter out questions (likely not action items)
    if content.endswith("?"):
        return False
    
    # Filter out pure gibberish (too many repeated characters or symbols)
    if len(set(content)) < 3:  # Less than 3 unique chars
        return False
    
    # Filter out lines that are mostly symbols/punctuation
    alpha_chars = sum(c.isalpha() or c.isspace() for c in content)
    if len(content) > 0 and alpha_chars / len(content) < 0.5:
        return False
    
    return True


def extract_action_items(text: str) -> List[str]:
    """Extract action items using heuristic pattern matching.
    
    TODO 3: Replaced all print() statements with logger.debug() for cleaner production code.
    """
    logger.debug(f"Input text (first 100 chars): {text[:100]}...")
    
    lines = text.splitlines()
    logger.debug(f"Split into {len(lines)} line(s)")
    
    extracted: List[str] = []
    for idx, raw_line in enumerate(lines):
        line = raw_line.strip()
        logger.debug(f"Line {idx}: '{line}'")
        
        if not line:
            logger.debug(f"  Skipped: empty line")
            continue
        
        if _is_action_line(line):
            logger.debug(f"  Matched as action line")
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            logger.debug(f"  Cleaned result: '{cleaned}'")
            extracted.append(cleaned)
        else:
            logger.debug(f"  Not an action line")
    
    logger.debug(f"After pattern matching: {len(extracted)} item(s)")
    
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        logger.debug(f"No items found by pattern matching, trying imperative fallback...")
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        logger.debug(f"Split into {len(sentences)} sentence(s)")
        for sent_idx, sentence in enumerate(sentences):
            s = sentence.strip()
            if not s:
                logger.debug(f"  Sentence {sent_idx}: skipped (empty)")
                continue
            logger.debug(f"  Sentence {sent_idx}: '{s}'")
            if _looks_imperative(s):
                logger.debug(f"    Looks imperative!")
                extracted.append(s)
            else:
                logger.debug(f"    Not imperative")
    
    logger.debug(f"Before deduplication: {len(extracted)} item(s)")
    
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            logger.debug(f"  Duplicate removed: '{item}'")
            continue
        seen.add(lowered)
        unique.append(item)
    
    logger.info(f"Extracted {len(unique)} unique action item(s)")
    logger.debug(f"Final items: {unique}")
    
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


# ============================================================================
# TODO 1: LLM-Powered Action Item Extraction
# ============================================================================
def extract_action_items_llm(text: str, model: str = "llama3.1:8b") -> List[str]:
    """
    Extract action items from free-form notes using an LLM with structured outputs.
    
    This function sends the user's notes to an Ollama-hosted LLM with a carefully
    crafted prompt and JSON schema, ensuring the response is a valid list of strings.
    
    Args:
        text: Raw note text from user (e.g., meeting notes, brainstorming)
        model: Ollama model name (default: llama3.1:8b for balance of speed/quality)
        
    Returns:
        List[str]: Extracted action items as clean strings, deduplicated
        
    Example:
        >>> notes = "Meeting notes: - Fix bug #123, TODO: Write tests"
        >>> extract_action_items_llm(notes)
        ['Fix bug #123', 'Write tests']
    """
    # TODO 3: Use logging instead of print for production
    logger.info(f"LLM extraction using model: {model}")
    logger.debug(f"Input text (first 100 chars): {text[:100]}...")
    
    # Edge case: Handle empty or whitespace-only input
    if not text or not text.strip():
        logger.warning("Empty input, returning empty list")
        return []
    
    # -------------------------------------------------------------------------
    # Step 1: Construct the system prompt
    # -------------------------------------------------------------------------
    # This prompt instructs the LLM on:
    # - What to extract (actionable tasks, not general statements)
    # - What to ignore (greetings, context, non-actionable content)
    # - Output format expectations (even though JSON schema enforces it)
    system_prompt = """You are an expert assistant that extracts actionable tasks from meeting notes, brainstorming sessions, or free-form text.

**Your task:**
1. Identify sentences or phrases that represent concrete, actionable items (things someone should DO)
2. Extract them as clear, concise action items
3. Remove formatting markers like bullets, checkboxes, or prefixes (e.g., "TODO:", "[ ]")
4. Ignore non-actionable content like greetings, context, or general statements

**Examples of actionable items:**
- "Set up database" → Extract
- "Fix bug #123" → Extract  
- "The meeting was productive" → Ignore (not actionable)
- "Review pull requests by Friday" → Extract

Return only the action items as a JSON array of strings."""

    # -------------------------------------------------------------------------
    # Step 2: Define JSON schema for structured output
    # -------------------------------------------------------------------------
    # This schema FORCES the LLM to return valid JSON in this exact structure:
    # { "action_items": ["item1", "item2", ...] }
    # 
    # Benefits over raw text parsing:
    # - No need for complex regex post-processing
    # - Guaranteed parseable output (no hallucinated markdown/formatting)
    # - Type safety at LLM level
    json_schema = {
        'type': 'object',
        'properties': {
            'action_items': {
                'type': 'array',
                'items': {'type': 'string'},
                'description': 'List of extracted action items as clean strings'
            }
        },
        'required': ['action_items']
    }
    
    # -------------------------------------------------------------------------
    # Step 3: Call Ollama API with structured outputs
    # -------------------------------------------------------------------------
    try:
        logger.debug("Calling Ollama API...")
        response = chat(
            model=model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f"Extract action items from these notes:\n\n{text}"}
            ],
            format=json_schema,  # ← Key feature: enforce JSON structure
            options={
                'temperature': 0.1,  # TODO: Improved - Very low for consistency
            }
        )
        
        # -------------------------------------------------------------------------
        # Step 4: Parse and validate response
        # -------------------------------------------------------------------------
        # Even with structured outputs, we validate defensively
        raw_content = response['message']['content']
        logger.debug(f"Raw LLM response: {raw_content[:200]}...")
        
        parsed = json.loads(raw_content)
        items = parsed.get('action_items', [])
        
        # Type check: ensure all items are strings
        if not isinstance(items, list) or not all(isinstance(item, str) for item in items):
            logger.error("Invalid response format from LLM")
            return []
        
        # -------------------------------------------------------------------------
        # Step 5: Post-process for consistency + quality filtering
        # -------------------------------------------------------------------------
        # TODO: Improved - Filter out ambiguous single-word items
        cleaned = []
        for item in items:
            item = item.strip()
            if not item:
                continue
            
            # Filter out vague single words (e.g., "help", "fix", "do")
            words = item.split()
            if len(words) == 1 and len(item) < 6:
                logger.debug(f"Filtered vague item: '{item}'")
                continue
            
            cleaned.append(item)
        
        # Deduplicate while preserving order
        seen: set[str] = set()
        unique: List[str] = []
        for item in cleaned:
            lowered = item.lower()
            if lowered not in seen:
                seen.add(lowered)
                unique.append(item)
        
        logger.info(f"LLM extracted {len(unique)} action item(s)")
        logger.debug(f"Items: {unique}")
        
        return unique
        
    except Exception as e:
        # Graceful degradation: log error but don't crash the app
        logger.error(f"Error calling LLM: {type(e).__name__}: {e}")
        logger.debug("Falling back to empty list")
        return []
