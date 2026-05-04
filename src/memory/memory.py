from typing import Any


MemoryEntry = dict[str, Any]


class Memory:
    """In-memory placeholder with a structured write gate."""

    def __init__(self) -> None:
        self._entries: list[MemoryEntry] = []

    def context_for(self, message: str) -> dict[str, list[MemoryEntry]]:
        del message
        return {"recent": self._entries}

    def score(self, entry: MemoryEntry) -> float:
        score = 0.0

        if entry.get("intent") == "task":
            score += 0.5
        if entry.get("intent") == "question":
            score += 0.2
        if entry.get("mode") == "agent":
            score += 0.3

        return min(score, 1.0)

    def should_store(self, entry: MemoryEntry) -> bool:
        return self.score(entry) > 0.7

    def remember(self, entry: MemoryEntry) -> bool:
        if not self.should_store(entry):
            return False

        self._entries.append(entry)
        return True

    def export_for_signals(self) -> list[dict]:
        """Return a stable, flat copy of entries for signal extraction."""
        return [dict(entry) for entry in self._entries if isinstance(entry, dict)]
