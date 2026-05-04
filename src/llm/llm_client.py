from typing import Any

from src.utils.personality_formatter import format_personality


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
        del model, context, tool_results

        if plan is None:
            personality_prefix = format_personality(personality)
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
