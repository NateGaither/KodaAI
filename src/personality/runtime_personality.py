from src.memory.memory_signals import extract_memory_signals


def _collect_text_list(value: object) -> list[str]:
    if isinstance(value, str) and value:
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str) and item]
    return []


def _memory_entries_from_memory(memory: object) -> list[dict]:
    """
    Normalizes all supported memory shapes into a flat list[dict].
    Supports:
    - list[dict]
    - {"memory": [...]}
    - {"entries": [...]}
    """

    if isinstance(memory, list):
        return [item for item in memory if isinstance(item, dict)]

    if isinstance(memory, dict):
        direct_memory = memory.get("memory")
        if isinstance(direct_memory, list):
            return [item for item in direct_memory if isinstance(item, dict)]

        entries = memory.get("entries")
        if isinstance(entries, list):
            return [item for item in entries if isinstance(item, dict)]

    return []


def build_runtime_personality(personality: dict | None, memory: object) -> str:
    """Build deterministic personality prefix with subtle memory influence."""
    personality = personality or {}

    identity = personality.get("identity")
    name = ""

    if isinstance(identity, dict):
        identity_name = identity.get("name")
        if isinstance(identity_name, str):
            name = identity_name

    if not name:
        raw_name = personality.get("name")
        if isinstance(raw_name, str):
            name = raw_name

    tone_descriptors = _collect_text_list(personality.get("tone"))
    style_descriptors = _collect_text_list(personality.get("style"))
    behavior_descriptors = _collect_text_list(personality.get("behavior"))

    extracted = extract_memory_signals(_memory_entries_from_memory(memory))

    preferences = extracted.get("preferences", [])
    emotional_patterns = extracted.get("emotional_patterns", [])
    recurring_topics = extracted.get("recurring_topics", [])

    memory_signals: list[str] = []

    if preferences:
        tone_descriptors.append("preference-aware")
        memory_signals.append(f"preferences: {', '.join(preferences)}")

    if emotional_patterns:
        tone_descriptors.append("emotion-attuned")
        memory_signals.append(f"emotions: {', '.join(emotional_patterns)}")

    if recurring_topics:
        tone_descriptors.append("topic-consistent")
        memory_signals.append(f"topics: {', '.join(recurring_topics)}")

    # Preserve deterministic order while removing duplicates
    tone_descriptors = list(dict.fromkeys(tone_descriptors))

    details: list[str] = []

    if tone_descriptors:
        details.append(f"tone: {', '.join(tone_descriptors)}")

    if style_descriptors:
        details.append(f"style: {', '.join(style_descriptors)}")

    if behavior_descriptors:
        details.append(f"behavior: {', '.join(behavior_descriptors)}")

    if memory_signals:
        details.append(f"memory: {'; '.join(memory_signals)}")

    if name and details:
        return f"[{name} | {'; '.join(details)}] "

    if name:
        return f"[{name}] "

    if details:
        return f"[{'; '.join(details)}] "

    return ""