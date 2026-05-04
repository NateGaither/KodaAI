from typing import Any


def _normalize_entries(memory_entries: Any) -> list[dict]:
    if isinstance(memory_entries, list):
        return [entry for entry in memory_entries if isinstance(entry, dict)]

    export_for_runtime = getattr(memory_entries, "export_for_runtime", None)
    if callable(export_for_runtime):
        exported = export_for_runtime()
        if isinstance(exported, list):
            return [entry for entry in exported if isinstance(entry, dict)]

    return []


def extract_memory_signals(memory_entries: list[dict]) -> dict:
    """Extract deterministic memory signals from high-importance memory entries."""
    normalized_entries = _normalize_entries(memory_entries)
    high_importance_entries = [
        entry for entry in normalized_entries if float(entry.get("importance", 0.0)) >= 0.5
    ]

    preference_keywords = ("prefer", "preference", "favorite", "likes", "dislike")
    emotion_keywords = ("happy", "sad", "angry", "anxious", "excited", "stressed", "calm")
    topic_tags = {"code", "music", "gaming", "health", "travel", "work", "study"}

    preferences: list[str] = []
    emotional_patterns: list[str] = []
    recurring_topics: list[str] = []

    for entry in high_importance_entries:
        text_parts = []
        if isinstance(entry.get("message"), str):
            text_parts.append(entry["message"])
        if isinstance(entry.get("response"), str):
            text_parts.append(entry["response"])
        if isinstance(entry.get("text"), str):
            text_parts.append(entry["text"])

        text = " ".join(text_parts).strip().lower()
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

    preferences = list(dict.fromkeys(preferences))
    emotional_patterns = list(dict.fromkeys(emotional_patterns))
    recurring_topics = list(dict.fromkeys(recurring_topics))

    return {
        "preferences": preferences,
        "emotional_patterns": emotional_patterns,
        "recurring_topics": recurring_topics,
    }
