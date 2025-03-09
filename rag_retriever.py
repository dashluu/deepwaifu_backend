from langchain.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
from langchain.schema import Document

class RAGRetriever:
    def __init__(self, json_path: str):
        self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.vectorstore = self._load_data(json_path)

    def _load_data(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        documents = []

        for character in data:
            name = character.get("name", "Unknown")
            occupation = character.get("occupation", "Unknown")

            for personality_entry in character.get("personalities", []):
                personality = personality_entry.get("personality", "Neutral")
                dialogues = personality_entry.get("dialogues", [])

                for dialogue in dialogues:
                    text = f"{name} ({occupation}, {personality}): {dialogue}"
                    documents.append(Document(page_content=text))

        # Split text into smaller chunks for better retrieval
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = text_splitter.split_documents(documents)

        # Generate embeddings for the documents
        texts = [doc.page_content for doc in split_docs]
        embeddings = self.embeddings_model.encode(texts)
        return FAISS.from_documents(split_docs, embeddings)

    def retrieve(self, query: str, k=3):
        query_embedding = self.embeddings_model.encode([query])
        results = self.vectorstore.similarity_search(query_embedding, k=k)
        return [doc.page_content for doc in results]