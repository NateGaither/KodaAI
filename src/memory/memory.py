from typing import Any


MemoryEntry = dict[str, Any]


def score_memory(entry: dict) -> float:
    """Deterministically score memory importance between 0 and 1."""
    text_parts: list[str] = []
    for key in ("message", "response", "text"):
        value = entry.get(key)
        if isinstance(value, str) and value:
            text_parts.append(value.lower())
    text = " ".join(text_parts)

    score = 0.0

    preference_keywords = ("prefer", "preference", "favorite", "like", "dislike")
    emotional_keywords = ("happy", "sad", "angry", "anxious", "excited", "stressed", "calm")

    if any(keyword in text for keyword in preference_keywords):
        score += 0.4

    if any(keyword in text for keyword in emotional_keywords):
        score += 0.3

    if entry.get("_is_duplicate") is True:
        score += 0.2

    # Recency bonus is deterministic at write-time: newly scored entry is latest.
    score += 0.1

    return min(max(score, 0.0), 1.0)


def validate_memory_entry(entry: dict) -> bool:
    """Validate runtime memory export schema without raising exceptions."""
    try:
        if not isinstance(entry, dict):
            return False

        required_keys = ("mode", "intent", "message", "response")
        for key in required_keys:
            if key not in entry:
                return False
            if entry.get(key) is None:
                return False

        return True
    except Exception:
        return False


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

        existing_messages = {e.get("message") for e in self._entries if isinstance(e, dict)}
        existing_responses = {e.get("response") for e in self._entries if isinstance(e, dict)}

        is_duplicate = entry.get("message") in existing_messages or entry.get("response") in existing_responses

        scored_entry = dict(entry)
        scored_entry["_is_duplicate"] = is_duplicate
        entry["importance"] = score_memory(scored_entry)

        self._entries.append(entry)
        return True

def get_relevant_memories(self, limit: int = 10, min_score: float = 0.5) -> list[dict]:
    filtered = [
        dict(entry)
        for entry in self._entries
        if isinstance(entry, dict)
        and float(entry.get("importance", 0.0)) >= min_score
    ]

    filtered.sort(
        key=lambda entry: float(entry.get("importance", 0.0)),
        reverse=True
    )

    return filtered[:limit]


def export_for_runtime(self) -> list[dict]:
    """Return a stable flat list with runtime memory contract fields."""
    exported: list[dict] = []

    for entry in self._entries:
        if not isinstance(entry, dict):
            continue

        runtime_entry = {
            "mode": entry.get("mode"),
            "intent": entry.get("intent"),
            "message": entry.get("message"),
            "response": entry.get("response"),
        }

        if "importance" in entry:
            runtime_entry["importance"] = entry.get("importance")

        if not validate_memory_entry(runtime_entry):
            continue

        exported.append(runtime_entry)

    return exported


def export_for_signals(self) -> list[dict]:
    """Signal extraction uses runtime contract only."""
    return self.export_for_runtime()
