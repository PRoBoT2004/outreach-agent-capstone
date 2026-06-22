# ruff: noqa
# Outreach agent — multi-agent pipeline.
#
# Capstone build: an ADK SequentialAgent that chains two specialist LlmAgents:
#   1. research_agent  -> profiles the lead into a short brief (uses a tool)
#   2. writer_agent    -> turns the brief into one on-brand first-touch message
# Wrapped at runtime by a security screen, a safety guard, and human-in-the-loop
# (see app/guards.py and run_review.py). Uses Google AI Studio (Gemini API key).

import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

# Load .env (holds the Gemini API key) before configuring the model.
load_dotenv()

os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "False")
if not os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

MODEL = "gemini-2.5-flash"  # the only model with free-tier quota on this key (5 req/min)


def _model():
    return Gemini(model=MODEL, retry_options=types.HttpRetryOptions(attempts=3))


# One concrete, real operational pain per business type, so the message lands on
# something the prospect actually feels instead of generic praise.
_PAIN_HINTS = {
    "restaurant": "table turnover and slow billing during the dinner rush",
    "cafe": "splitting bills and tallying the daily cash count",
    "retail": "stock counts not matching the register at day end",
    "wholesale": "chasing payments and remembering who owes what",
    "salon": "no-shows and remembering repeat clients' preferences",
    "pharmacy": "expiry tracking and fast counter billing",
    "grocery": "khata (credit) customers and end-of-day cash reconciliation",
    "gym": "lapsed memberships you forget to follow up on",
}


def business_pain_hint(business_type: str) -> str:
    """Return one concrete, real daily pain point for a given type of business.

    The research agent calls this so the outreach is grounded in something the
    prospect actually feels, not generic flattery.

    Args:
        business_type: The kind of business, e.g. "restaurant", "retail shop", "wholesale".

    Returns:
        A short phrase naming a real daily pain point, or a safe generic fallback.
    """
    key = business_type.lower().strip()
    for k, v in _PAIN_HINTS.items():
        if k in key:
            return v
    return "the small daily admin that eats time you would rather spend on customers"


# === Agent 1: research ===================================================
research_agent = LlmAgent(
    name="research_agent",
    model=_model(),
    instruction="""
You are the research step in a B2B outreach pipeline.

The user gives you a business name, a type, and a city. Call the business_pain_hint
tool with the business type to get a real daily pain point. Then produce a short brief
for the writer. Output EXACTLY these four lines and nothing else:

PAIN: <the single sharpest daily operational pain for this business>
HOOK: <one concrete, grounded detail to open with, specific to this type and city>
ANGLE: <the one outcome to imply, e.g. fewer lost orders, faster billing, less admin>
TONE: peer, plain, no hype

Do not write the outreach message yourself. Do not invent facts, numbers, or names.
""".strip(),
    tools=[business_pain_hint],
    output_key="research_brief",
)


# === Agent 2: writer =====================================================
writer_agent = LlmAgent(
    name="writer_agent",
    model=_model(),
    instruction="""
You write ONE short cold first-touch outreach message for a solo founder
who builds simple software tools for small businesses.

Use this research brief from the previous step:
{research_brief}

Rules, no exceptions:
- No em-dashes anywhere. Use periods, commas, parentheses, or colons.
- No hype words (amazing, leading, cutting-edge, revolutionize, thrilled, world-class).
- Peer voice. Sound like a person doing the same kind of work, never an agency.
- Plain words. Use "use" not "utilize", "help" not "facilitate".
- Weave the HOOK in naturally. Never list the brief fields or labels.
- End with the exact question "Want to know more?".
- Never propose a call, visit, or meeting.
- Keep it tight: two or three short sentences, UNDER 55 words total. Cut every spare clause.
- Never invent facts, client names, numbers, or a portfolio link.

Return only the message text, ready to send. No preamble, no sign-off, no notes.
""".strip(),
    output_key="draft",
)


# === The pipeline: research -> writer ====================================
root_agent = SequentialAgent(
    name="outreach_pipeline",
    sub_agents=[research_agent, writer_agent],
)

app = App(
    root_agent=root_agent,
    name="app",
)
