from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.background import BackgroundTask
from ollama import generate
import asyncio
import json
from message import MessageModel

app = FastAPI()

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


@app.post("/chat", response_model=str)
async def chat_handler(message: MessageModel):
    async def generate_response():
        response = generate(model="llama3", prompt=message.text, stream=True)
        for chunk in response:
            if "response" in chunk:
                yield chunk["response"]
                # Force flush the chunk
                await asyncio.sleep(0)

    return StreamingResponse(generate_response())
