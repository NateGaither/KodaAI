from typing import Any


def _normalize_entries(memory_entries: Any) -> list[dict]:
    if isinstance(memory_entries, list):
        return [entry for entry in memory_entries if isinstance(entry, dict)]

    export_for_signals = getattr(memory_entries, "export_for_signals", None)
    if callable(export_for_signals):
        exported = export_for_signals()
        if isinstance(exported, list):
            return [entry for entry in exported if isinstance(entry, dict)]

    return []


def extract_memory_signals(memory_entries: list[dict]) -> dict:
    """Extract deterministic memory signals from memory entries."""
    normalized_entries = _normalize_entries(memory_entries)

    preference_keywords = ("prefer", "preference", "favorite", "likes", "dislike")
    emotion_keywords = ("happy", "sad", "angry", "anxious", "excited", "stressed", "calm")
    topic_tags = {"code", "music", "gaming", "health", "travel", "work", "study"}

    preferences: list[str] = []
    emotional_patterns: list[str] = []
    recurring_topics: list[str] = []

    for entry in normalized_entries:
        text = str(entry.get("text", "")).strip().lower()
        tags = entry.get("tags", [])
        normalized_tags = [tag.lower() for tag in tags if isinstance(tag, str)] if isinstance(tags, list) else []

        if text and any(keyword in text for keyword in preference_keywords):
            preferences.append(text)

        for emotion in emotion_keywords:
            if text and emotion in text:
                emotional_patterns.append(emotion)

        for tag in normalized_tags:
            if tag in topic_tags:
                recurring_topics.append(tag)

    # Deduplicate while preserving deterministic insertion order.
    preferences = list(dict.fromkeys(preferences))
    emotional_patterns = list(dict.fromkeys(emotional_patterns))
    recurring_topics = list(dict.fromkeys(recurring_topics))

    return {
        "preferences": preferences,
        "emotional_patterns": emotional_patterns,
        "recurring_topics": recurring_topics,
    }
