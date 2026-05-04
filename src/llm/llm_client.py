from typing import Any

from src.personality.runtime_personality import build_runtime_personality


class LLMClient:
    """Stable LLM boundary for future provider integration."""

    def generate(
        self,
        model: str,
        input: str,
        context: dict,
        personality: dict | None,
        tool_results: Any | None,
        plan: object | None,
    ) -> str:
del model, tool_results

if plan is None:
    memory = None
    if isinstance(context, dict):
        memory = context.get("memory")

    personality_prefix = ""
    if personality:
        personality_prefix = build_runtime_personality(personality, memory)

    return f"{personality_prefix}Received: {input}"

intent = getattr(plan, "intent", None)
if intent is None and isinstance(plan, dict):
    intent = plan.get("intent")

intent_label = intent if isinstance(intent, str) and intent else "general"
        return (
            f"[agent-mode:{intent_label}] "
            "[structured_reasoning_placeholder] "
            f"Result: {input}"
        )
