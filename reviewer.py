from agent import Agent
from llm   import LLMAdaptor
from message import Message

class RuleReviewer(Agent):
    def __init__(self, name, llm:LLMAdaptor,system_prompt = None):
        super().__init__(name, llm, system_prompt)

    def run(self, code_diff: str = None):
        if not code_diff:
            raise ValueError("缺少待审核的代码差异")

        messages = []
        if self.system_prompt:
            messages.append({
                "role": "system",
                "content": self.system_prompt,
            })
        messages.append({
            "role": "user",
            "content": code_diff,
        })
        return self.llm.think(messages)

        
