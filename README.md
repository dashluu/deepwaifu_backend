### Uses FastAPI to run the backend
Installation
1. clone the repository 
git clone https://github.com/yourusername/deepwaifu_backend.git
cd deepwaifu_backend
2. create and activate a virtual environment: 
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies:

Dependencies: 
1. pip install langchain faiss-cpu chromadb
2. pip install "fastapi[standard]"
3. pip install ollama
4. pip install -U langchain-community
5. pip install sentence-transformers
6. Need to install ollama from the web as well https://ollama.com/download

Running the Backend:
1. in terminal, source venv/bin/activate # On Windows: venv\Scripts\activate
3. ollama serve
4. export OLLAMA_HOST="http://127.0.0.1:11434"  # On Windows: set OLLAMA_HOST=http://127.0.0.1:11434
5. fastapi dev server.py

Testing
To test if llama is running:
$ ollama run llama3 # This will check if your model is running (ctrl+d to exit)
To test the retriever:
$ python test_retriever.py
To test the chat functionality:
$ python test_chat.py

API Endpoints

- POST /new-chat: Create a new chat session
- POST /chat: Send a message and get a response
- POST /auth: Authenticate with an existing chat session
- DELETE /delete-chat: Delete a chat session

Frontend Connection
- The frontend should connect to the backend at http://localhost:8000. 
- Make sure CORS is properly configured if your frontend is running on a different domain or port.

Project Structure
- rag_retriever.py: Implements the RAG retrieval system
- character_engine.py: Handles character-based chat generation
- server.py: FastAPI server implementation
- models.py: Pydantic models for API
- context.py: Context management for chat sessions
- context_manager.py: Manages multiple chat contexts
- data/: Contains dialogue data for the RAG system

Troubleshooting

- Connection refused error: Make sure Ollama is running
- "SentenceTransformerEmbeddings object is not callable": Check that the embeddings class is properly implemented
- 422 Unprocessable Entity: Ensure the message format matches the expected schema