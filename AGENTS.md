# Koda AI — Agent Operating Rules

This file defines strict rules for Codex and any automated agent working on this repository.

The goal is to prevent merge conflicts, architectural drift, and unintended cross-layer changes.

---

# 1. SYSTEM ARCHITECTURE LAYERS

The codebase is divided into strict layers:

## 🔒 CORE LAYER (LOCKED BY DEFAULT)
These files define system behavior and must NOT be modified unless explicitly working in a CORE session:

- src/core/koda_core.py
- src/planner/planner.py
- src/llm/llm_client.py

Rules:
- Do not change function signatures without explicit instruction
- Do not refactor across modules
- Do not modify memory/personality logic from this layer

---

## 🧠 MEMORY LAYER
- src/memory/memory.py
- src/memory/memory_signals.py

Rules:
- Only affects memory storage, scoring, and export formats
- Must not modify core or LLM logic
- Must preserve deterministic behavior

---

## 🎭 PERSONALITY LAYER
- src/personality/runtime_personality.py

Rules:
- Only handles formatting and signal interpretation
- Must not modify memory storage or core execution logic

---

## 🚀 INFRASTRUCTURE LAYER
- Docker
- Discord bot
- FastAPI / web UI

Rules:
- Must not modify internal AI logic
- Only handles deployment, runtime, and interfaces

---

# 2. CODEx EDITING RULES (CRITICAL)

## ❌ FORBIDDEN BEHAVIOR
Codex must NOT:
- rewrite entire files when only small changes are needed
- move functions between files
- rename variables unless explicitly required
- mix multiple layers in one session
- “clean up” or refactor unrelated code
- change APIs across modules without instruction

---

## ✔ REQUIRED BEHAVIOR

Codex MUST:
- make minimal diffs only
- preserve file structure
- avoid formatting-only rewrites
- keep changes localized to the requested feature
- respect existing function signatures unless explicitly told otherwise

---

# 3. SESSION SCOPING RULE

Every Codex session MUST declare a scope:

Valid scopes:
- CORE_SESSION
- MEMORY_SESSION
- PERSONALITY_SESSION
- INFRA_SESSION

Codex is only allowed to modify files within that scope.

---

# 4. CONTRACT STABILITY RULE

The following functions are considered system contracts:

- Memory.export_for_runtime()
- Planner.generate_plan()
- LLMClient.generate()
- build_runtime_personality()

Rules:
- Inputs/outputs must remain stable
- Internal refactors allowed only within same layer
- Cross-layer behavior changes require explicit review

---

# 5. MERGE CONFLICT PREVENTION RULE

If Codex detects overlapping edits:
- prefer smallest possible diff
- never merge stylistic changes across branches
- do not resolve conflicts by rewriting logic
- preserve one implementation fully instead of blending both

---

# 6. PRIORITY RULE

If rules conflict:

1. System stability overrides feature additions
2. Minimal diffs override refactors
3. Layer isolation overrides convenience
4. Contract stability overrides optimization

---

# 7. GOAL

This system is designed to evolve safely without:
- merge conflicts
- cross-layer corruption
- architectural drift

All contributions must preserve this stability.
