# Outreach Agent — Specification

This spec is the source of truth. The code in `app/` is one implementation of it and
is disposable: if it drifts, regenerate it to satisfy the scenarios below.

## Intent

An agent that drafts cold first-touch outreach messages for a solo founder
who builds simple software tools for small businesses. The agent turns a business name and
type into one short, on-brand, ready-to-send message, behind a security screen, a safety
guard, and a human approval step.

## Roles

- **Orchestrator (human):** owns this spec and the final approve/edit/reject decision.
- **Agent:** drafts the message and calls tools.
- **Guards (deterministic code):** screen input and validate output. Never skipped.

## Behavior

```gherkin
Feature: Draft a brand-correct first-touch message

  Scenario: Drafting for a known business type
    Given a business name and a type the agent recognises (restaurant, cafe, retail,
      wholesale, salon, pharmacy, grocery, gym)
    When the agent drafts a message
    Then it calls the business_pain_hint tool for that type
    And it weaves the returned pain point into the message
    And the message ends with the exact question "Want to know more?"

  Scenario: Brand voice rules are always enforced
    Given any drafted message
    When the safety guard validates it
    Then the message contains no em dash or en dash
    And it contains none of the banned hype words (amazing, leading, cutting-edge,
      revolutionize, thrilled, game-changer, world-class)
    And it does not propose a call, meeting, or demo
    And it is 70 words or fewer

  Scenario: Unknown business type still produces a safe message
    Given a business type the agent does not recognise
    When the agent drafts a message
    Then the business_pain_hint tool returns a safe generic pain point
    And the message still passes the safety guard

Feature: Security and human control (Effective Trust)

  Scenario: Prompt injection in the input is blocked
    Given an input that tries to override the agent's instructions
      (for example "ignore your previous instructions")
    When the security screen runs before the model
    Then the input is flagged
    And it is routed to a human instead of being trusted by the model

  Scenario: Clean input is allowed through
    Given an input with no injection patterns
    When the security screen runs
    Then the input is marked clean and passed to the agent

  Scenario: Every draft requires human approval
    Given a drafted and guard-checked message
    When it is presented to the human
    Then the human can approve, edit, or reject it
    And the decision is recorded to decisions.log with a timestamp
    And nothing is treated as sent without an explicit approval
```

## Evaluation

`verify_guards.py` is the executable form of the security and brand-voice scenarios above.
A change is acceptable only if it still scores 4/4 there.

## Out of scope (for now)

- Actually sending messages (WhatsApp/email integration).
- Multi-turn conversation after the first touch.
- Cloud deployment (Day 5 optional codelab, needs a billing account).
