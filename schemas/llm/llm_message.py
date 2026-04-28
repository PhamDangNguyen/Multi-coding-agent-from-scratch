from pydantic import BaseModel

class BaseMessage(BaseModel):
    """Message schema, which contains information for each message"""
    role: str
    content: str
