from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from models import MessageModel, CharacterModel, ContextModel, AuthModel
from context_manager import ContextManager
import uuid

app = FastAPI()
MODEL = "llama3"
# Managing chat history for each user
ctx_manager = ContextManager()

# Define origins for CORS
origins = ["http://localhost", "http://localhost:3000"]

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Frontend posts to localhost:port/new-chat
# Input is an object of type CharacterModel
# Output is a string
@app.post("/new-chat", response_model=str)
def new_chat_handler(character: CharacterModel):
    # Create a unique id for each client, or each conversation
    ctx_id = str(uuid.uuid4())
    ctx = ContextModel(id=ctx_id, character=character)
    ctx_manager.add_context(ctx)
    return ctx_id


# Frontend posts to localhost:port/auth
# Input is an object of type AuthModel
# Output is an object of type CharacterModel
@app.post("/auth", response_model=CharacterModel)
def new_chat_handler(auth: AuthModel):
    # TODO: handle invalid context ID, or conversation ID
    return ctx_manager.get_character(auth.ctx_id)


# Frontend posts to localhost:port/chat
# Input is an object of type MessageModel
# Output is a string
@app.post("/chat", response_model=str)
async def chat_handler(message: MessageModel):
    return StreamingResponse(ctx_manager.generate_response(message))
