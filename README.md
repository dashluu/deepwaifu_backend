### Uses FastAPI to run the backend

To run the program:

1. in terminal, pip install "fastapi[standard]"
2. in terminal, pip install ollama
3. Make sure to install ollama from https://ollama.com/download/windows
4. Restart your VSCode so that it can detect ollama
5. in terminal, ollama pull llama3
5. fastapi dev server.py

To test if llama is running, 
1. in terminal, ollama run llama3

This will check if your model is running (ctrl+d to exit)

tbd: not sure if we need to install ollama from the website
