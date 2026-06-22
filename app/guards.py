"""Day 4 security + safety guards for the outreach agent.

Two layers of "Effective Trust". An LLM is non-deterministic, so we never trust
its input or its output without a deterministic check around it.

  1. screen_input  runs BEFORE the model. Catches prompt injection so a malicious
     lead name or note cannot hijack the agent. Flagged input is routed to a human;
     the model is never handed it blindly.
  2. validate_draft runs AFTER the model, BEFORE anything is treated as sendable.
     A deterministic gate that the draft obeys the hard brand rules.
"""

import re

# Patterns that signal someone is trying to override the agent's instructions.
INJECTION_PATTERNS = [
    r"ignore (the |your |all )?(previous|prior|above)",
    r"disregard (the |your |all )?",
    r"forget (your|the|all|everything)",
    r"system prompt",
    r"you are now",
    r"new instructions",
    r"override",
    r"bypass",
    r"reveal your",
    r"instead,? write",
    r"act as",
]

EMDASH = "—"  # em dash
ENDASH = "–"  # en dash

BANNED_HYPE = [
    "amazing", "leading", "cutting-edge", "cutting edge", "revolutionize",
    "revolutionise", "thrilled", "game-changer", "game changer", "world-class",
]

# Phrases that propose a call/meeting, which the first-touch rule forbids.
MEETING_WORDS = [
    "hop on", "schedule a call", "schedule a meeting", "book a call",
    "set up a call", "jump on a call", "let's meet", "lets meet",
    "quick call", "get on a call", "give me a call",
]


def screen_input(text: str):
    """Return (ok, reason). ok=False means route to a human and do not trust the model."""
    low = text.lower()
    for pat in INJECTION_PATTERNS:
        if re.search(pat, low):
            return False, f"possible prompt injection (matched /{pat}/)"
    return True, "clean"


def validate_draft(draft: str):
    """Return (ok, violations). Deterministic brand-rule gate on the model's output."""
    violations = []
    if EMDASH in draft or ENDASH in draft:
        violations.append("contains an em/en dash (banned)")
    low = draft.lower()
    if "want to know more?" not in low:
        violations.append("missing the required first-touch close 'Want to know more?'")
    for w in BANNED_HYPE:
        if w in low:
            violations.append(f"banned hype word: '{w}'")
    for w in MEETING_WORDS:
        if w in low:
            violations.append(f"proposes a call/meeting on first touch: '{w}'")
    word_count = len(draft.split())
    if word_count > 70:
        violations.append(f"too long: {word_count} words")
    return (len(violations) == 0), violations
