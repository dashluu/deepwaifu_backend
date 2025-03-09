from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from models import MessageModel, CharacterModel, ContextModel, AuthModel
from context_manager import ContextManager
import uuid
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from rag_retriever import RAGRetriever

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

# Initialize RAGRetriever with your JSON data path
retriever = RAGRetriever(json_path="data/dialogues.json")

# Define a Conversational Retrieval Chain using LangChain
prompt_template = PromptTemplate("You are a helpful assistant. Answer the following question: {question}")
conversational_chain = ConversationalRetrievalChain(prompt_template, None, retriever.retrieve)

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

@app.post("/chat", response_model=str)
async def chat_handler(message: MessageModel):
    from character_engine import CharacterEngine  # Import inside the function to avoid circular import
    char_engine = CharacterEngine(MODEL)
    conversational_chain.generator = char_engine.generate_response  # Set the generator method
    ctx = ctx_manager.get_context(message.ctx_id)
    if not ctx:
        raise HTTPException(status_code=404, detail="Context not found")
    response = conversational_chain.run({"question": message.content})
    return StreamingResponse(response)