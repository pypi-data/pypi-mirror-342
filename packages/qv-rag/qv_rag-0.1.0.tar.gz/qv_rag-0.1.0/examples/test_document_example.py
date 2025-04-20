"""
Simple example using test_document.txt
"""

from pathlib import Path
from qv_rag.engine import RAGEngine

def main():
    # Initialize the RAG engine
    engine = RAGEngine(
        collection_name="test_document_collection",
        chunk_size=500,
        chunk_overlap=100
    )
    
    # Path to the test document
    test_doc_path = Path(__file__).parent / "test_document.txt"
    
    # Add the test document
    print("Adding test document...")
    engine.add_file(test_doc_path)
    
    # Query about Python
    print("\nQuery: What is Python?")
    results = engine.query("What is Python?")
    for result in results:
        print(f"- {result['text']}")
    
    # Query about machine learning
    print("\nQuery: What is machine learning?")
    results = engine.query("What is machine learning?")
    for result in results:
        print(f"- {result['text']}")
    
    # Query about web development
    print("\nQuery: What is web development?")
    results = engine.query("What is web development?")
    for result in results:
        print(f"- {result['text']}")
    
    # Get engine info
    info = engine.get_info()
    print("\nEngine information:")
    print(f"Total documents: {info['count']}")
    print(f"Collection name: {info['name']}")

if __name__ == "__main__":
    main() 