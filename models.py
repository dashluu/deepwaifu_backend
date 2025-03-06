from pydantic import BaseModel

# represents a chat message
class MessageModel(BaseModel):
    ctx_id: str # id of chat session
    sender: str
    receiver: str
    text: str

# represents a character
class CharacterModel(BaseModel):
    name: str
    avatar: str # image
    occupation: str
    personality: str
    age: int
    keywords: str
    background: str
    interests: str

# represents a chat session
class ContextModel(BaseModel):
    id: str # id of chat session
    character: CharacterModel # character in chat session

# represents an authentication request
class AuthModel(BaseModel):
    ctx_id: str
