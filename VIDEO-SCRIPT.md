# Video script — record this on screen (about 2.5 minutes)

The capstone needs a video explanation. Keep it under 3 minutes. Screen-record your terminal
+ editor and talk over it. You do not need to be on camera. Use OBS, the Xbox Game Bar
(Win+G), or any screen recorder.

Before recording: open a terminal in the project folder and run once so it is warm.
`cd ~/Desktop/outreach-agent`

---

## Scene 1 — The problem (20 sec)
**Show:** a sample lead list, or just talk to camera.
**Say:**
"I sell software to small shops and cafes. Every lead needs a different first
message. Writing them by hand is slow, and letting an AI free-write them sounds like spam.
So I built a multi-agent system that drafts honest, on-brand outreach, with guardrails."

## Scene 2 — The architecture (30 sec)
**Show:** `README.md` (the architecture diagram) and `app/agent.py`.
**Say:**
"It is an ADK SequentialAgent with two agents. A research agent profiles the lead into a
brief using a tool. A writer agent turns that brief into the message. The brief passes
between them through ADK session state. Around them are security and safety guards."

## Scene 3 — Run it live (50 sec)
**Show:** the terminal. Run:
`uv run python run_review.py "Draft outreach for Maple Cafe, a cafe in Pune."`
**Say (as it runs):**
"The input is screened for prompt injection first. Then the research agent runs, then the
writer. Here is the draft. Notice: no em-dashes, peer voice, grounded in a real restaurant
pain, and it ends with a soft ask. The safety guard checked it against my brand rules, and
now it asks me to approve, edit, or reject before anything is sent."
Press **a** to approve.

## Scene 4 — Security + evaluation (40 sec)
**Show:** run `uv run python verify_guards.py`
**Say:**
"This is my local evaluation. It proves the security screen blocks a prompt-injection input,
the safety guard rejects a rule-breaking draft, and the live agent's output passes. Four out
of four. The model is non-deterministic, so I never trust it blindly. Deterministic guards
and a human gate every message."
**Show briefly:** `skills/brand-voice/SKILL.md`.
**Say:** "The brand voice is a reusable agent skill, not a hard-coded prompt."

## Scene 5 — Close (15 sec)
**Say:**
"So: a multi-agent ADK pipeline, an agent skill, and real security and evaluation, solving an
actual business problem I have. Thanks for watching."

---

## After recording
- Upload to YouTube (Unlisted is fine) or Google Drive (link sharing on).
- Put the link in `CAPSTONE-WRITEUP.md` where it says [PASTE YOUR VIDEO URL].
