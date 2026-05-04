# Mirror Shell AI — Koda Build Plan

**Version**: Final (Operationally Defined + Conversational Intelligence)

---

## 1. Purpose

Koda is a stateful, autonomous AI agent system designed to **think, remember, act, and converse naturally**. This document defines both features *and* the execution logic required to make behavior consistent, intelligent, and emotionally coherent.

---

# 2. Core Architecture (Central Orchestrator)

## The Core Loop

Every interaction flows through a single deterministic pipeline.

### Flow

1. Load context
2. Generate plan (mode + intent)
3. Select model
4. Execute tools (if agent mode)
5. Generate response
6. Write memory

### Implementation

```python
class KodaCore:
    async def handle_message(self, user_input, user_id):
        context = await memory.load_context(user_id)

        plan = await planner.generate_plan(
            input=user_input,
            context=context
        )

        model = model_router.select(plan)

        if plan.mode == "agent":
            results = await tool_executor.run(plan.tools) if plan.tools else None

            response = await llm.generate(
                model=model,
                input=user_input,
                context=context,
                tool_results=results
            )
        else:
            response = await llm.generate(
                model=model,
                input=user_input,
                context=context,
                personality=personality_loader.get(),
                tool_results=None
            )

        await memory.write(user_id, user_input, response, None)

        return response
```

---

# 3. Conversational Intelligence Layer (NEW — CRITICAL)

## Dual-Mode System

Koda operates in two distinct but seamlessly switching modes:

### Conversational Mode (Default)

* Natural dialogue
* Personality-driven
* No tool usage
* Emotion-aware

### Agent Mode

* Task execution
* Tool usage
* Structured reasoning

---

## Planner Output (Updated)

```json
{
  "mode": "conversation | agent",
  "intent": "chat | task | question",
  "tools": [],
  "complexity": 1-10
}
```

---

## Mode Rules

```python
def should_use_tools(plan):
    return plan.mode == "agent" and len(plan.tools) > 0
```

* Conversation mode suppresses tools entirely
* Agent mode enables full capability stack

---

## Personality System (YAML-Based)

### Source

* `personality.yaml`

### Loader

```python
import yaml

class PersonalityLoader:
    def __init__(self, path="personality.yaml"):
        self.path = path
        self.cache = None

    def get(self):
        if not self.cache:
            with open(self.path, "r") as f:
                self.cache = yaml.safe_load(f)
        return self.cache
```

### Usage

* Injected only in conversational mode
* Defines tone, identity, behavior rules

---

# 4. Decision Engine

## Model Routing

```python
def select_model(task):
    if task.mode == "conversation":
        return "xiaomi/mimo-v2-flash"
    if task.type in ["code", "analysis"]:
        return "deepseek/deepseek-v4-flash"
    if task.requires_tools:
        return "deepseek/deepseek-v4-flash"
    return "xiaomi/mimo-v2-flash"
```

---

# 5. Memory System (Refined)

## Structure

* Working Memory (20–30 msgs)
* Recent Summary
* Significant Memory
* Episodic Memory
* Semantic Memory (vector DB)

---

## Write Gate (Critical)

```python
def should_store(entry):
    return score(entry) > 0.7
```

```python
def score(entry):
    score = 0
    if "preference" in entry:
        score += 0.4
    if "emotion" in entry:
        score += 0.3
    if "long_term" in entry:
        score += 0.5
    return min(score, 1.0)
```

---

## Mode-Based Memory Bias

### Conversation Mode Stores:

* Preferences
* Emotions
* Relationship context

### Agent Mode Stores:

* Task results
* Actions taken
* Relevant facts

---

# 6. Tool / Skill System

## Execution Safety

```python
await asyncio.wait_for(tool.run(), timeout=10)
```

## Sandbox Isolation

```python
class PluginSandbox:
    def __init__(self, plugin):
        self.plugin = plugin

    async def execute(self):
        try:
            return await self.plugin.run()
        except Exception:
            return {"error": "Plugin failed safely"}
```

## Permissions

* GREEN → Auto-run
* YELLOW → Confirm
* RED → Explicit approval

---

# 7. Observability & Monitoring

* Prometheus + Grafana
* Token tracking
* Tool logs
* Alerts

---

# 8. Cost Management

```python
if monthly_spend > LIMIT:
    model = "fallback-cheap-model"
```

* Hard caps enforced

---

# 9. Error Handling

* Graceful fallback
* No raw errors
* Offline mode

---

# 10. Plugins & External Data

* `/plugins/` system
* Sandboxed execution
* Read/write separation

---

# 11. Communication Layer

* Discord
* FastAPI Web UI
* Voice (Pipecat)

---

# 12. Reflection & Dream System

* Scheduled processing
* Memory refinement
* Insight generation

---

# 13. Backup & Recovery

* Encrypted backups
* Rollback support

---

# 14. Deployment

* Docker Compose
* Git updates
* Hot reload

---

# 15. Stack

* Python 3.11
* discord.py
* FastAPI
* MongoDB
* OpenRouter
* APScheduler
* Prometheus/Grafana
* Pipecat

---

# Final State

This system now:

* Maintains natural conversation
* Executes complex tasks
* Switches modes seamlessly
* Stores meaningful memory only
* Operates predictably and safely

It is now fully defined and ready for implementation.
