from typing import Any


class ModelRouter:
    """Selects an LLM model from planner output."""

    CONVERSATION_MODEL = "xiaomi/mimo-v2-flash"
    AGENT_MODEL = "deepseek/deepseek-v4-flash"

    def select(self, plan: Any) -> str:
        routes = {
            "conversation": self.CONVERSATION_MODEL,
            "agent": self.AGENT_MODEL,
        }
        return routes.get(getattr(plan, "mode", "conversation"), self.CONVERSATION_MODEL)
