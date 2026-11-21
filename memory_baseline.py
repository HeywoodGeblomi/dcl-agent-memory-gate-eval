"""memory_baseline.py — naive agent memory that drifts.

Just a dict of key -> latest value. New evidence overwrites. No commitment,
no hidden state. This is what most agent memory layers do today.
"""
from __future__ import annotations
from typing import Any

class BaselineMemory:
    def __init__(self):
        self.store: dict[str, Any] = {}

    def write(self, key: str, value: Any) -> None:
        self.store[key] = value

    def read(self, key: str) -> Any:
        return self.store.get(key)

    def snapshot(self) -> dict:
        return dict(self.store)
