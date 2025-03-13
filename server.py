from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from models import MessageModel, CharacterModel, ContextModel, AuthModel
from context_manager import ContextManager
import uuid
import asyncio

app = FastAPI()
MODEL = "llama3"
# Managing chat history for each user
ctx_manager = ContextManager()

# Define origins for CORS (frontend access)
origins = ["http://localhost", "http://localhost:3000"]

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/new-chat", response_model=str)
def new_chat_handler(character: CharacterModel):
    # Create a unique id for each client, or each conversation
    ctx_id = str(uuid.uuid4())
    ctx = ContextModel(id=ctx_id, character=character)
    ctx_manager.add_context(ctx)
    return ctx_id

@app.delete("/delete-chat", response_model=str)
def delete_chat_handler(auth: AuthModel):
    ctx_manager.delete_context(auth.ctx_id)
    return auth.ctx_id

@app.post("/auth", response_model=CharacterModel)
def auth_handler(auth: AuthModel):
    ctx = ctx_manager.get_context(auth.ctx_id)
    ctx.clear_all()
    return ctx.character

@app.post("/chat")
async def chat_handler(message: MessageModel):
    from character_engine import CharacterEngine  # Import inside the function to avoid circular import
    
    ctx = ctx_manager.get_context(message.ctx_id)
    if not ctx:
        raise HTTPException(status_code=404, detail="Context not found")
    
    char_engine = CharacterEngine(MODEL)
    
    # Create the streaming response
    async def response_generator():
        try:
            async for chunk in char_engine.generate_response(ctx, message):
                # Make sure we're yielding valid content
                if chunk:
                    # Add proper formatting for SSE
                    yield f"data: {chunk}\n\n"
                await asyncio.sleep(0.01)  # Small delay to avoid overwhelming the connection
            
            # Signal the end of the stream
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            print(f"Error in response generator: {str(e)}")
            yield f"data: Error: {str(e)}\n\n"
    
    return StreamingResponse(
        response_generator(), 
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )