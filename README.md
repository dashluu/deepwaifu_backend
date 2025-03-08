### Uses FastAPI to run the backend

To run the program:
 
1. After pip installing everything, restart your VSCode so that it can detect ollama
2. in terminal, ollama pull llama3
3. fastapi dev server.py

Dependencies: 
1. pip install langchain faiss-cpu chromadb
2. pip install "fastapi[standard]"
3. pip install ollama

To test if llama is running, 
1. in terminal, ollama run llama3

This will check if your model is running (ctrl+d to exit)

tbd: not sure if we need to install ollama from the website
