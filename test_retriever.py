from rag_retriever import RAGRetriever
import os

# Check if the data file exists
data_path = "data/dialogues.json"
if not os.path.exists(data_path):
    print(f"Error: Data file not found at {data_path}")
    print(f"Current working directory: {os.getcwd()}")
    print("Available files in data directory:")
    try:
        print(os.listdir("data"))
    except:
        print("Could not list data directory")
    exit(1)

print(f"Data file found: {data_path}")

# Initialize the retriever
print("Initializing RAG Retriever...")
retriever = RAGRetriever(data_path)

# Test with a few sample queries
test_queries = [
    "Tell me about your day",
    "What are your hobbies?",
    "How do you feel about technology?"
]

for query in test_queries:
    print("\n" + "="*50)
    print(f"TESTING QUERY: '{query}'")
    print("="*50)
    
    results = retriever.retrieve(query, k=3)
    
    if results:
        print(f"\nFound {len(results)} relevant results")
    else:
        print("\nNo results found or an error occurred")

print("\nTest completed")