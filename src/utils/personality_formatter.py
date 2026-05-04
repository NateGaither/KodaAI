def format_personality(personality: dict | None) -> str:
    """Build a deterministic personality prefix string."""
    if not personality:
        return ""

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

    details: list[str] = []
    tone = personality.get("tone")
    if isinstance(tone, str) and tone:
        details.append(f"tone: {tone}")

    style = personality.get("style")
    if isinstance(style, str) and style:
        details.append(f"style: {style}")
    elif isinstance(style, list):
        style_items = [item for item in style if isinstance(item, str) and item]
        if style_items:
            details.append(f"style: {', '.join(style_items)}")

    behavior = personality.get("behavior")
    if isinstance(behavior, str) and behavior:
        details.append(f"behavior: {behavior}")
    elif isinstance(behavior, list):
        behavior_items = [item for item in behavior if isinstance(item, str) and item]
        if behavior_items:
            details.append(f"behavior: {', '.join(behavior_items)}")

    if name and details:
        return f"[{name} | {'; '.join(details)}] "
    if name:
        return f"[{name}] "
    if details:
        return f"[{'; '.join(details)}] "

    return ""
