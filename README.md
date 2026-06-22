# Outreach Agent — a guarded multi-agent system for honest B2B cold outreach

**Kaggle 5-Day AI Agents (Vibe Coding) Capstone · Track: Agents for Business**

A solo founder selling software to small shops has to send a different first message to
every lead. Generic AI copy is obvious and gets ignored. This project is a multi-agent
pipeline that turns one line ("a restaurant in Pune") into a short, grounded,
on-brand first-touch message, behind a security screen, a safety guard, and a human
approval step so nothing wrong ever gets sent.

It is small on purpose. It solves a real problem the author has (cold outreach to small
shops) and it is honest: every claim a guard can check, it checks.

## Course concepts demonstrated

1. **Multi-agent system (ADK).** A `SequentialAgent` chains two specialist `LlmAgent`s:
   a **research agent** profiles the lead into a brief, then a **writer agent** turns that
   brief into the message. State passes between them via `output_key` / `{research_brief}`.
   See [`app/agent.py`](app/agent.py).
2. **Agent skill.** A portable `SKILL.md` (`brand-voice`) encodes the brand rules as a
   reusable skill. See [`skills/brand-voice/SKILL.md`](skills/brand-voice/SKILL.md).
3. **Security + evaluation.** A prompt-injection screen runs **before** the model; a
   deterministic safety guard validates the draft **after** the model; a human approves,
   edits, or rejects every message; a local eval scores the guards. See
   [`app/guards.py`](app/guards.py), [`run_review.py`](run_review.py), [`verify_guards.py`](verify_guards.py).
4. **Agent tools.** A `business_pain_hint` function tool grounds the message in a real pain
   point per business type.

## Architecture

```
user input ("a grocery shop in Indore")
      │
      ▼
[ security screen ]  app/guards.py: blocks prompt injection before the model
      │
      ▼
┌─────────────────────────── ADK SequentialAgent ───────────────────────────┐
│  research_agent  ──(brief via output_key)──►  writer_agent                  │
│  (tool: business_pain_hint)                   (enforces brand-voice)         │
└─────────────────────────────────────────────────────────────────────────────┘
      │
      ▼
[ safety guard ]   app/guards.py: no em-dashes, no hype, ends with "Want to know more?",
      │            no call/meeting on first touch, under length cap
      ▼
[ human-in-the-loop ]  run_review.py: approve / edit / reject, logged to decisions.log
```

## Run it

Prereqs: Python 3.11+, `uv`, and a Google AI Studio API key in `.env`
(`GEMINI_API_KEY=...`, `GOOGLE_GENAI_USE_VERTEXAI=FALSE`).

```bash
uv sync                                  # install dependencies
# quick draft:
uv run python run_once.py "Draft outreach for Maple Cafe, a cafe in Pune."
# with security screen + human approval:
uv run python run_review.py "Draft outreach for Brightside Pharmacy, a pharmacy in Nagpur."
# local evaluation of the guards:
uv run python verify_guards.py
```

## Why "honest"

The safety guard exists so the agent cannot send hype, fake authority, or anything the brand
rules forbid, even if the model drifts. The model is non-deterministic; the guard is not. The
spec ([`spec.md`](spec.md)) is the source of truth, and the code is regenerable from it.

## Layout

| Path | What |
|------|------|
| `app/agent.py` | The multi-agent pipeline (research + writer) |
| `app/guards.py` | Security screen + safety guard |
| `skills/brand-voice/SKILL.md` | The brand-voice agent skill |
| `run_once.py` | One-shot draft |
| `run_review.py` | Human-in-the-loop runner |
| `verify_guards.py` | Local evaluation (scores the guards) |
| `spec.md` | Gherkin behaviour spec (source of truth) |
