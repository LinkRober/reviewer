from .agent import Agent
from .llm import LLMAdaptor


class Reviewer(Agent):
    def __init__(
        self,
        name: str,
        llm: LLMAdaptor,
        system_prompt: str | None = None,
    ):
        super().__init__(name, llm, system_prompt)

    def run(self, input_text: str, **kwargs: object) -> str:
        if not isinstance(input_text, str) or not input_text.strip():
            raise ValueError("缺少待审核内容")

        messages = []
        if self.system_prompt:
            messages.append({
                "role": "system",
                "content": self.system_prompt,
            })
        messages.append({
            "role": "user",
            "content": input_text,
        })
        return self.llm.think(messages)
