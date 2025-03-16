from context import Context  # convo history
from models import MessageModel  # message from user
from rag_retriever import RAGRetriever  # rag retrieval model
import asyncio  # asynch operations
from ollama import chat  # llama3 model

class CharacterEngine:
    def __init__(self, model="llama3"):
        self._model = model
        self.rag_retriever = RAGRetriever("data/dialogues.json")

    # Asynchronous generator
    async def generate_response(self, ctx: Context, message: MessageModel):
        # Add user's message to conversation history
        ctx.add_message(message.to_chat_message())
        # Add character identity to improve retrieval
        character_info = f"Character: {ctx.character.name}, a {ctx.character.age}-year-old {ctx.character.occupation} who is {ctx.character.personality}."
    
        # Enhanced query with character context
        enhanced_query = f"As {character_info} {message.content}"
        # Retrieve relevant context using RAG
        retrieved_texts = self.rag_retriever.retrieve(enhanced_query, k=2)
        rag_context = "\n".join(retrieved_texts)
        
        # Create system message with RAG context
        system_message = {"role": "system", "content": f"Context:\n{rag_context}\n\nRespond to the user based on this context."}
        
        # Add system message to the beginning of messages list for this request only
        recent_messages = ctx.messages[-5:] 
        messages_with_context = [system_message] + ctx.messages
        
        # Call the model with history & RAG context
        response = chat(model=self._model, messages=messages_with_context, stream=True)
        
        # Create placeholder for assistant's response
        ctx.add_message({"role": "assistant", "content": ""})
        
        response_text = ""
        for chunk in response:
            if "message" in chunk and "content" in chunk["message"]:
                chunk_content = chunk["message"]["content"]
                response_text += chunk_content
                ctx.messages[-1]["content"] = response_text  # Update the entire content each time
                yield chunk_content
                # Force flush the chunk
                await asyncio.sleep(0)