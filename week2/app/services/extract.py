from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    # DEBUG: Log input text
    print(f"\n🔍 [extract_action_items] Input text (first 100 chars): {text[:100]}...")
    
    lines = text.splitlines()
    print(f"📝 [extract_action_items] Split into {len(lines)} line(s)")
    
    extracted: List[str] = []
    for idx, raw_line in enumerate(lines):
        line = raw_line.strip()
        print(f"  ➜ Line {idx}: '{line}'")
        
        if not line:
            print(f"    ⊘ Skipped: empty line")
            continue
        
        if _is_action_line(line):
            print(f"    ✅ Matched as action line")
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            print(f"    📌 Cleaned result: '{cleaned}'")
            extracted.append(cleaned)
        else:
            print(f"    ❌ Not an action line")
    
    print(f"\n🎯 [extract_action_items] After pattern matching: {len(extracted)} item(s)")
    
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        print(f"⚠️  [extract_action_items] No items found by pattern matching, trying imperative fallback...")
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        print(f"   Split into {len(sentences)} sentence(s)")
        for sent_idx, sentence in enumerate(sentences):
            s = sentence.strip()
            if not s:
                print(f"    Sentence {sent_idx}: skipped (empty)")
                continue
            print(f"    Sentence {sent_idx}: '{s}'")
            if _looks_imperative(s):
                print(f"      ✅ Looks imperative!")
                extracted.append(s)
            else:
                print(f"      ❌ Not imperative")
    
    print(f"\n🔢 [extract_action_items] Before deduplication: {len(extracted)} item(s)")
    
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            print(f"  🗑️  Duplicate removed: '{item}'")
            continue
        seen.add(lowered)
        unique.append(item)
    
    print(f"✨ [extract_action_items] Final result: {len(unique)} unique item(s)")
    for i, item in enumerate(unique, 1):
        print(f"  {i}. {item}")
    
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
