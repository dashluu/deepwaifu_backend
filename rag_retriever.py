from langchain.vectorstores import FAISS # vector database
from langchain.embeddings.openai import OpenAIEmbeddings # numberical representations
from langchain.document_loaders import CSVLoader # loader
from langchain.text_splitter import RecursiveCharacterTextSplitter # text splitter

class RAGRetriever:
    def __init__(self, csv_path: str):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = self._load_data(csv_path)

    def _load_data(self, csv_path):
        loader = CSVLoader(csv_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = text_splitter.split_documents(documents)
        return FAISS.from_documents(split_docs, self.embeddings)

    def retrieve(self, query: str, k=3):
        results = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
