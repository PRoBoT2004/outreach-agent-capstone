"""Run the outreach agent once from the command line and print the draft.

Bypasses the agents-cli web playground (which has a version bug in v0.5.0).
Usage: uv run python run_once.py "Draft outreach for Maple Cafe, a cafe in Pune."
"""

import asyncio
import sys

from dotenv import load_dotenv

load_dotenv()

from google.adk.runners import InMemoryRunner
from google.genai import types

from app.agent import root_agent

APP_NAME = "outreach"
USER_ID = "founder"


async def main() -> None:
    prompt = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "Draft a first-touch outreach message for Maple Cafe, a cafe in Pune."
    )

    runner = InMemoryRunner(agent=root_agent, app_name=APP_NAME)
    session = await runner.session_service.create_session(app_name=APP_NAME, user_id=USER_ID)

    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    print("\n=== PROMPT ===")
    print(prompt)
    print("\n=== AGENT DRAFT ===")
    async for event in runner.run_async(
        user_id=USER_ID, session_id=session.id, new_message=message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
