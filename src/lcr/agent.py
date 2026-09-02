from abc import ABC, abstractmethod
from typing import Any

from .llm import LLMAdaptor
from .message import Message


class Agent(ABC):
    def __init__(
        self,
        name: str,
        llm: LLMAdaptor,
        system_prompt: str | None = None,
    ):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
        self._history: list[Message] = []

    @abstractmethod
    def run(self, input_text: str, **kwargs: Any) -> str:
        """Run the agent."""

    def add_message(self, message: Message) -> None:
        self._history.append(message)

    def clear_history(self) -> None:
        self._history.clear()

    def get_history(self) -> list[Message]:
        return self._history.copy()

    def __str__(self) -> str:
        return f"Agent(name={self.name},provider={self.llm.model})"
