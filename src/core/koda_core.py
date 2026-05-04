from src.llm.llm_client import LLMClient
from src.memory.memory import Memory
from src.core.model_router import ModelRouter
from src.planner.planner import Planner


class KodaCore:
    """Core message loop for Koda."""

    def __init__(self) -> None:
        self.memory = Memory()
        self.llm_client = LLMClient()
        self.model_router = ModelRouter()
        self.planner = Planner()

    def handle_message(self, message: str, mode: str = "conversation") -> str:
        context = self._load_context(message)
        plan = self.planner.generate_plan(message=message, mode=mode)
        selected_model = self.model_router.select(plan)
        response = self.llm_client.generate(
            model=selected_model,
            input=message,
            context=context,
            personality=None,
            plan=plan,
            tool_results=None,
        )

        self._write_memory(message=message, response=response, plan=plan)
        return response

    def _load_context(self, message: str) -> dict:
        del message
        return {"memory": self.memory.get_relevant_memories()}

    def _write_memory(self, message: str, response: str, plan: object) -> None:
        entry = {
            "mode": plan.mode,
            "intent": plan.intent,
            "message": message,
            "response": response,
        }
        self.memory.remember(entry)
