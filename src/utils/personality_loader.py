from pathlib import Path
from typing import Any

import yaml


class PersonalityLoader:
    """Loads Koda personality data for conversational mode."""

    def __init__(self, path: str | Path = "personality.yaml") -> None:
        self.path = Path(path)
        self._cache: dict[str, Any] | None = None

    def load(self) -> dict[str, Any]:
        if self._cache is None:
            self._cache = self._load_yaml()

        return self._cache

    def _load_yaml(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}

        with self.path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if data is None:
            return {}

        if not isinstance(data, dict):
            raise ValueError("Personality file must contain a YAML mapping.")

        return data
