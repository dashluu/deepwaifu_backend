from langchain.vectorstores import FAISS # vector database
# from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter # text splitter
import json
from langchain.schema import Document

#csv 
#class RAGRetriever:
    # def __init__(self, csv_path: str):
    #     self.embeddings = OpenAIEmbeddings()
    #     self.vectorstore = self._load_data(csv_path)

    # def _load_data(self, csv_path):
    #     loader = CSVLoader(csv_path)
    #     documents = loader.load()
    #     text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    #     split_docs = text_splitter.split_documents(documents)
    #     return FAISS.from_documents(split_docs, self.embeddings)

    # def retrieve(self, query: str, k=3):
    #     results = self.vectorstore.similarity_search(query, k=k)
    #     return [doc.page_content for doc in results]

    
#json
class RAGRetriever:
    def __init__(self, json_path: str):
        self.embeddings = OpenAIEmbeddings()
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

        return FAISS.from_documents(split_docs, self.embeddings)

    def retrieve(self, query: str, k=3):
        results = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

