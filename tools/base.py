# core/tool.py

from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    name: str = ""
    description: str = ""
    title: str = ""

    def __init__(self):
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        pass

    def schema(self):
        return {
            "name": self.name,
            "description": self.description,
        }