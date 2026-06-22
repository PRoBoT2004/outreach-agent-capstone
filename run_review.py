"""Day 4: outreach agent with security screen, safety guard, and human-in-the-loop.

Flow:
  your input -> screen_input (security) -> agent draft -> validate_draft (safety)
             -> YOU approve / edit / reject -> decision logged to decisions.log

Usage:
  uv run python run_review.py "Draft outreach for Maple Cafe, a cafe in Pune."
"""

import asyncio
import datetime
import json
import sys

from dotenv import load_dotenv

load_dotenv()

from google.adk.runners import InMemoryRunner
from google.genai import types

from app.agent import root_agent
from app.guards import screen_input, validate_draft

APP_NAME = "outreach"
USER_ID = "founder"


async def draft(prompt: str) -> str:
    runner = InMemoryRunner(agent=root_agent, app_name=APP_NAME)
    session = await runner.session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    out = ""
    async for event in runner.run_async(
        user_id=USER_ID, session_id=session.id, new_message=message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            out = event.content.parts[0].text
    return out.strip()


def log_decision(record: dict) -> None:
    record["at"] = datetime.datetime.now().isoformat(timespec="seconds")
    with open("decisions.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    prompt = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "Draft a first-touch outreach message for Maple Cafe, a cafe in Pune."
    )

    # 1. SECURITY SCREEN (before the model)
    ok, reason = screen_input(prompt)
    if not ok:
        print(f"\n[SECURITY] Input flagged: {reason}")
        print("[SECURITY] Routing to human. The model was not trusted with this input.")
        log_decision({"prompt": prompt, "stage": "input_screen", "result": "flagged", "reason": reason})
        choice = input("Override and continue anyway? (y/N): ").strip().lower()
        if choice != "y":
            print("Stopped.")
            return

    # 2. AGENT DRAFTS
    print("\nDrafting...")
    message = asyncio.run(draft(prompt))
    print("\n=== DRAFT ===")
    print(message)

    # 3. SAFETY GUARD (after the model)
    clean, violations = validate_draft(message)
    if clean:
        print("\n[GUARD] Passed all brand rules.")
    else:
        print("\n[GUARD] Rule violations found:")
        for v in violations:
            print(f"  - {v}")

    # 4. HUMAN IN THE LOOP
    print("\nApprove this draft?  [a]pprove  [e]dit  [r]eject")
    decision = input("> ").strip().lower()
    if decision == "e":
        edited = input("Type your edited version:\n> ").strip()
        log_decision({"prompt": prompt, "draft": message, "decision": "edited", "final": edited})
        print("\nSaved your edited version.")
    elif decision == "a":
        log_decision({"prompt": prompt, "draft": message, "decision": "approved", "clean": clean})
        print("\nApproved. Ready to send.")
    else:
        log_decision({"prompt": prompt, "draft": message, "decision": "rejected"})
        print("\nRejected. Nothing sent.")


if __name__ == "__main__":
    main()
