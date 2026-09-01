from typing import Optional,Dict,Any,Literal
from datetime import datetime
from pydantic import BaseModel

# 定义角色 规则审核专员，架构审核专员，审核负责人
MessageRole = Literal['system','developer','user','assistant']

class Message(BaseModel):
    role:MessageRole
    content:str
    timestamp:datetime = None
    metadata:Optional[dict[str,Any]] = None

    def __init__(self, content:str,role:MessageRole, **kawrgs):
        super.__init__(
            content=content,
            timestamp=kawrgs.get('timestamp',datetime.now()),
            metadata=kawrgs.get('metadata',{}),
            role = role
        )

    def to_dict(self) -> Dict[str,Any]:
        return {
            'content':self.content
        }

    def __str__(self) -> str:
        return f"[{self.content}]"