import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Plan:
    mode: str
    intent: str
    tools: list[str]
    complexity: int
    personality: bool


class Planner:
    """Selects the execution mode before KodaCore performs work."""

    VALID_MODES = frozenset({"conversation", "agent"})
    VALID_INTENTS = frozenset({"chat", "question", "task"})
    ACTION_KEYWORDS = frozenset(
        {"run", "check", "get", "list", "show", "find", "restart", "start", "stop"}
    )
    QUESTION_WORDS = frozenset({"what", "why", "how", "when", "where", "who"})

    def generate_plan(self, message: str, mode: str = "conversation") -> Plan:
        normalized_mode = self._normalize_mode(mode)
        normalized_message = message.strip().lower()

        if normalized_mode == "agent" or self._is_action_request(normalized_message):
            return self._create_plan(
                mode="agent",
                intent="task",
                tools=[],
                complexity=7,
                personality=False,
            )

        if self._is_question(normalized_message):
            return self._create_plan(
                mode="conversation",
                intent="question",
                tools=[],
                complexity=4,
                personality=True,
            )

        return self._create_plan(
            mode="conversation",
            intent="chat",
            tools=[],
            complexity=2,
            personality=True,
        )

    def _is_action_request(self, message: str) -> bool:
        words = set(re.findall(r"\b\w+\b", message))
        return bool(words & self.ACTION_KEYWORDS)

    def _is_question(self, message: str) -> bool:
        if message.endswith("?"):
            return True

        first_word = message.split(maxsplit=1)[0] if message else ""
        return first_word in self.QUESTION_WORDS

    def _create_plan(
        self,
        mode: str,
        intent: str,
        tools: object,
        complexity: object,
        personality: object,
    ) -> Plan:
        return Plan(
            mode=self._normalize_mode(mode),
            intent=self._normalize_intent(intent),
            tools=self._normalize_tools(tools),
            complexity=self._normalize_complexity(complexity),
            personality=bool(personality),
        )

    def _normalize_mode(self, mode: str) -> str:
        if mode in self.VALID_MODES:
            return mode

        return "conversation"

    def _normalize_intent(self, intent: str) -> str:
        if intent in self.VALID_INTENTS:
            return intent

        return "chat"

    def _normalize_tools(self, tools: object) -> list[str]:
        if not isinstance(tools, list):
            return []

        return [tool for tool in tools if isinstance(tool, str)]

    def _normalize_complexity(self, complexity: object) -> int:
        if not isinstance(complexity, int):
            return 1

        return min(max(complexity, 1), 10)
