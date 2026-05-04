from typing import Any


class LLMClient:
    """Stable LLM boundary for future provider integration."""

    def generate(
        self,
        model: str,
        input: str,
        context: dict,
        personality: dict | None,
        tool_results: Any | None,
        plan: object | None,
    ) -> str:
        del model, context, tool_results

        if plan is None:
            personality_prefix = ""
            if personality:
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
                    personality_prefix = f"[{name} | {'; '.join(details)}] "
                elif name:
                    personality_prefix = f"[{name}] "
                elif details:
                    personality_prefix = f"[{'; '.join(details)}] "

            return f"{personality_prefix}Received: {input}"

        intent = getattr(plan, "intent", None)
        if intent is None and isinstance(plan, dict):
            intent = plan.get("intent")
        intent_label = intent if isinstance(intent, str) and intent else "general"

        return (
            f"[agent-mode:{intent_label}] "
            "[structured_reasoning_placeholder] "
            f"Result: {input}"
        )
