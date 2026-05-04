from typing import Any


class LLMClient:
    """Stable LLM boundary for future provider integration."""

    def generate(
        self,
        model: str,
        input: str,
        context: Any,
        plan: Any,
        tool_results: Any | None,
    ) -> str:
        del model, context, plan, tool_results

        return f"Received: {input}"
