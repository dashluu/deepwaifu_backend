from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from models import MessageModel, CharacterModel, ContextModel, AuthModel
from context_manager import ContextManager
from character_engine import CharacterEngine
import uuid

app = FastAPI()
MODEL = "llama3"
# Managing chat history for each user
ctx_manager = ContextManager()
char_engine = CharacterEngine(MODEL)

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


# Frontend posts to localhost:port/delete-chat
# Input is an object of type AuthModel
# Output is a string
@app.delete("/delete-chat", response_model=str)
def delete_chat_handler(auth: AuthModel):
    ctx_manager.delete_context(auth.ctx_id)
    # Check whether the context is removed
    # print(ctx_manager)
    return auth.ctx_id


# Frontend posts to localhost:port/auth
# Input is an object of type AuthModel
# Output is an object of type CharacterModel
@app.post("/auth", response_model=CharacterModel)
def new_chat_handler(auth: AuthModel):
    # TODO: handle invalid context ID, or conversation ID
    ctx = ctx_manager.get_context(auth.ctx_id)
    # Call this in case the context should be cleared when the user refreshes the page
    ctx.clear_all()
    return ctx.character


# Frontend posts to localhost:port/chat
# Input is an object of type MessageModel
# Output is a string
@app.post("/chat", response_model=str)
async def chat_handler(message: MessageModel):
    # TODO: handle invalid context ID, or conversation ID
    ctx = ctx_manager.get_context(message.ctx_id)
    return StreamingResponse(char_engine.generate_response(ctx, message))
