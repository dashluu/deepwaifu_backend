from langchain_community.vectorstores import FAISS  # Updated import
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
from langchain.schema import Document

class SentenceTransformerEmbeddings:
    """Wrapper for sentence_transformers embeddings to use with LangChain"""
    
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
        
    def embed_documents(self, texts):
        """Get embeddings for a list of texts"""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()  # Convert numpy array to list
        
    def embed_query(self, text):
        """Get embedding for a single text"""
        embedding = self.model.encode(text)
        return embedding.tolist()  # Convert numpy array to list
    
    def __call__(self, texts):
        """Make the class callable - automatically choose between single and multiple texts"""
        if isinstance(texts, str):
            return self.embed_query(texts)
        return self.embed_documents(texts)

class RAGRetriever:
    def __init__(self, json_path: str):
        self.embedding_model_name = 'all-MiniLM-L6-v2'
        self.embeddings = SentenceTransformerEmbeddings(self.embedding_model_name)
        self.vectorstore = self._load_data(json_path)
        print(f"RAG Retriever initialized with data from {json_path}")

    def _load_data(self, json_path):
        try:
            print(f"Loading data from {json_path}")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            documents = []
            print(f"Processing {len(data)} characters from the dataset")

            for character in data:
                name = character.get("name", "Unknown")
                occupation = character.get("occupation", "Unknown")

                for personality_entry in character.get("personalities", []):
                    personality = personality_entry.get("personality", "Neutral")
                    dialogues = personality_entry.get("dialogues", [])

                    for dialogue in dialogues:
                        text = f"{name} ({occupation}, {personality}): {dialogue}"
                        documents.append(Document(
                            page_content=text, 
                            metadata={
                                "name": name, 
                                "occupation": occupation, 
                                "personality": personality
                            }
                        ))

            print(f"Created {len(documents)} document objects")

            # Split text into smaller chunks for better retrieval
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            split_docs = text_splitter.split_documents(documents)
            print(f"Split into {len(split_docs)} chunks")

            # Create FAISS index using our wrapper
            print("Creating FAISS index...")
            vectorstore = FAISS.from_documents(documents=split_docs, embedding=self.embeddings)
            print("FAISS index created successfully")
            
            return vectorstore
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise

    def retrieve(self, query: str, k=3):
        try:
            print(f"Retrieving relevant context for: {query}")
        
            # The simplest solution: just pass the query directly
            # FAISS will use the embeddings object we provided during initialization
            results = self.vectorstore.similarity_search(query, k=k)
        
            retrieved_texts = [doc.page_content for doc in results]
            print(f"Retrieved {len(retrieved_texts)} relevant text chunks")
            for i, text in enumerate(retrieved_texts):
                print(f"Result {i+1}: {text[:100]}...")
            return retrieved_texts
        except Exception as e:
            print(f"Error during retrieval: {str(e)}")
            # Try a more direct approach if the above failed
            try:
                # Get embeddings for the query
                query_embedding = self.embeddings.embed_query(query)
            
                # Use the embedding directly with FAISS
                docs_and_scores = self.vectorstore.similarity_search_by_vector(
                    query_embedding, 
                    k=k
                )
                retrieved_texts = [doc.page_content for doc in docs_and_scores]
                print(f"Retrieved {len(retrieved_texts)} relevant text chunks (using alternative method)")
                return retrieved_texts
            except Exception as e2:
                print(f"Alternative retrieval also failed: {str(e2)}")
                return []