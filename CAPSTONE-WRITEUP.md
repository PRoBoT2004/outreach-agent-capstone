# Kaggle Writeup — paste this into the Kaggle Writeup editor

> This is the submission narrative. Paste it into the Kaggle Writeup, then add your code
> link and video link where marked. Edit the [BRACKETS] before submitting.

---

## Title
Outreach Agent: a guarded multi-agent system for honest B2B cold outreach

## Track
Agents for Business

## The problem
A solo founder selling software to small shops (cafes, pharmacies, grocers) has to send a
different first message to every lead. Writing 20 by hand is slow; letting an LLM free-write
them produces generic, hype-filled copy that reads as spam and gets ignored. The real
business problem is **personalised first-touch outreach at volume, without sounding like a
bot and without sending anything off-brand or untrue.**

## The solution
A multi-agent pipeline that turns one line of input ("a restaurant in Pune") into a
short, grounded, on-brand first-touch message, wrapped in guardrails so nothing wrong is
ever sent.

```
input → [security screen] → research agent → writer agent → [safety guard] → human approval
```

## Key concepts demonstrated (more than three)

1. **Multi-agent system with ADK.** An ADK `SequentialAgent` chains two specialist
   `LlmAgent`s. The **research agent** profiles the lead into a four-line brief (PAIN, HOOK,
   ANGLE, TONE) using a function tool, and passes it via `output_key`. The **writer agent**
   reads that brief through `{research_brief}` state interpolation and produces the message.
2. **Agent skill.** The brand voice is encoded as a portable `SKILL.md` (`brand-voice`)
   with progressive-disclosure metadata, reusable by any agent, not hard-coded into one prompt.
3. **Security and evaluation.** A prompt-injection screen runs before the model so a
   malicious lead note cannot hijack the agent. A deterministic safety guard validates the
   draft after the model (no em-dashes, no hype words, must end with "Want to know more?",
   no call/meeting on first touch, length cap). A human approves, edits, or rejects every
   draft (human-in-the-loop), logged to `decisions.log`. A local evaluation script scores the
   guards and the live agent on a small dataset (currently 4/4).
4. **Agent tools.** A `business_pain_hint` function tool grounds each message in a real,
   business-type-specific pain point instead of generic flattery.

## Why this is "Effective Trust", not blind trust
An LLM is non-deterministic, so this system never trusts its input or output blindly. The
input is screened, the output is validated by deterministic code, and a human gates every
send. The behaviour is pinned by a Gherkin spec (`spec.md`) that is the source of truth, and
the code is regenerable from it.

## Example
Input: `"Draft outreach for City Grocers, a grocery shop in Indore."`
Output: *"Running City Grocers in Indore means juggling khata customers and the daily cash
count. I build simple tools that cut that admin down. Want to know more?"*

No em-dashes, peer voice, grounded in a real pain, ends with the soft ask, passed all guards.

## How to run
See the README. `uv run python run_review.py "..."` runs the full pipeline with the security
screen, the guard, and human approval.

## Tech
Google ADK (`SequentialAgent`, `LlmAgent`), Gemini 2.5 Flash via Google AI Studio, Python.

## Links
- Code: [PASTE YOUR PUBLIC GITHUB REPO URL]
- Video: [PASTE YOUR VIDEO URL]

## Author
[YOUR NAME] — [solo / team]
