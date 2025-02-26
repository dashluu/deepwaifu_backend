from pydantic import BaseModel


class MessageModel(BaseModel):
    ctx_id: str
    sender: str
    receiver: str
    text: str


class CharacterModel(BaseModel):
    name: str
    avatar: str
    occupation: str
    personality: str
    age: int
    keywords: str
    background: str
    interests: str


class ContextModel(BaseModel):
    id: str
    character: CharacterModel


class AuthModel(BaseModel):
    ctx_id: str
