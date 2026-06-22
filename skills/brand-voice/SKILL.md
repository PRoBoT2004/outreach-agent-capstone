---
name: brand-voice
description: Rewrite, lint, or fix any customer-facing or public copy (outreach messages, landing-page text, social posts, captions, email replies, product microcopy) into a consistent founder brand voice. Use whenever the user asks to clean up, rewrite, tighten, brand-fit, or check text before publishing, or pastes a draft and asks "does this sound right?"
---

# Goal

Take any draft text and return a version that matches the founder's brand voice: direct, peer-level, zero AI-tells. Then list exactly what was changed and why, so the user can learn the pattern.

# Hard rules (non-negotiable)

1. **No em-dashes. Anywhere.** Replace every em-dash with a period, comma, parenthesis, or colon. Em-dashes are the single biggest tell of AI-generated text. This rule has zero exceptions.
2. **No cheerleading.** Delete "great question," "amazing," "exciting," "I'm thrilled," "happy to help," and all encouragement padding. Cut straight to substance.
3. **Peer voice, not studio voice.** Default to "I'm doing this same thing right now" with one real, lived detail. Never claim agency or studio authority unless a real portfolio URL backs it up.
4. **No fake urgency or hype.** No "act now," no exclamation stacks, no "game-changer," no "revolutionary."
5. **Plain words over corporate words.** "use" not "utilize," "help" not "facilitate," "buy" not "purchase," "about" not "regarding."

# Outreach-specific rules (apply when the text is a cold or first-touch message)

- First touch asks one small thing only: "want to know more?" Never propose a call, visit, or meeting on the first message.
- One concrete detail that proves you understand their world. No generic flattery.
- Short. If it scrolls on a phone, it is too long.

# Instructions

1. Read the draft and identify its purpose (outreach / landing copy / social / reply / microcopy).
2. Rewrite it applying every hard rule above, plus outreach rules if relevant.
3. Keep the user's actual meaning and any real facts. Do not invent claims, numbers, or credentials.
4. Output in exactly this format:

   **Rewritten:**
   <the cleaned copy>

   **Changed:**
   - <each change as one line: what + why>

5. If the draft was already clean, say so plainly and list nothing.

# Examples

Input: "We are a leading agency thrilled to help you utilize cutting-edge AI to revolutionize your workflow — let's hop on a call!"

Output:
**Rewritten:**
I build small AI tools for businesses like yours. I'm testing one right now that cuts repetitive workflow steps. Want to know more?

**Changed:**
- Removed "leading agency" and "thrilled": cheerleading + unbacked studio claim.
- "utilize" to "build/cut", "revolutionize" dropped: plain words, no hype.
- Replaced em-dash with a period.
- Removed the call ask: first touch only asks "want to know more?"

# Constraints

- Do not add em-dashes back under any circumstance, including inside the "Changed" notes.
- Do not pad the output with praise for the user's draft.
- Do not lengthen the copy. Shorter is the goal.
- Never fabricate a portfolio link, client name, or metric to sound more authoritative.
