from abc import ABC,abstractmethod
from typing import Optional,Any
try:
    from .message import Message
except ImportError:
    from message import Message
from llm import LLMAdaptor

class Agent(ABC):
    def __init__(
            self,
            name:str,
            llm:LLMAdaptor,
            system_prompt:Optional[str] = None,
            ):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
        self._history:list[Message] = []

    @abstractmethod
    def run(self,input_text:str,**kwargs) -> str:
        """运行Agent"""
        pass

    def add_message(self,message:Message):
        """添加消息到历史记录"""
        self._history.append(message)

    def clear_history(self):
        """清空历史记录"""
        self._history.clear()

    def get_history(self):
        """获取历史记录"""
        return self._history.copy()

    def __str__(self) -> str:
        return f"Agent(name={self.name},privider={self.llm.model})"
