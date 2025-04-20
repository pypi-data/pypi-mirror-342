"""
Storage module for the RAG engine using ChromaDB
"""

from typing import List, Dict, Optional, Any
from pathlib import Path
import chromadb
from chromadb.config import Settings


class ChromaStorage:
    """Storage implementation using ChromaDB"""
    
    def __init__(
        self,
        collection_name: str,
        persist_directory: Optional[str] = None
    ):
        """
        Initialize ChromaDB storage.
        
        Args:
            collection_name: Name of the collection
            persist_directory: Optional directory to persist the database
        """
        # Initialize ChromaDB client
        if persist_directory:
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(allow_reset=True)
            )
        else:
            self.client = chromadb.Client(
                settings=Settings(allow_reset=True)
            )
        
        # Create or get collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
        except chromadb.errors.NotFoundError:
            # Collection doesn't exist, create it
            self.collection = self.client.create_collection(name=collection_name)
    
    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> None:
        """
        Add texts to the collection.
        
        Args:
            texts: List of texts to add
            metadatas: Optional metadata for each text
            ids: Optional IDs for each text
        """
        if not texts:
            return
            
        # Generate IDs if not provided
        if ids is None:
            ids = [f"doc{i}" for i in range(len(texts))]
        
        # Ensure metadatas is a list of the same length as texts
        if metadatas is None:
            metadatas = [{} for _ in texts]
        elif len(metadatas) != len(texts):
            # If metadatas is shorter, pad with empty dicts
            metadatas = metadatas + [{} for _ in range(len(texts) - len(metadatas))]
        
        # Add to collection
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(
        self,
        query_text: str,
        top_k: int = 5,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Query the collection.
        
        Args:
            query_text: The query text
            top_k: Number of results to return
            where: Optional metadata filter
            where_document: Optional document content filter
            
        Returns:
            List of results with documents and metadata
        """
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=top_k,
                where=where,
                where_document=where_document
            )
            
            # Format results
            formatted_results = []
            if results and "documents" in results and results["documents"]:
                for i in range(len(results["documents"][0])):
                    result = {
                        "text": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i] if results.get("metadatas") and results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results.get("distances") and results["distances"] else None
                    }
                    formatted_results.append(result)
            
            return formatted_results
        except Exception as e:
            print(f"Error querying collection: {e}")
            return []
    
    def delete(
        self,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Delete documents from the collection.
        
        Args:
            where: Optional metadata filter
            where_document: Optional document content filter
        """
        self.collection.delete(
            where=where,
            where_document=where_document
        )
    
    def update(
        self,
        ids: List[str],
        texts: Optional[List[str]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """
        Update documents in the collection.
        
        Args:
            ids: List of document IDs to update
            texts: Optional new texts
            metadatas: Optional new metadata
        """
        self.collection.update(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection.
        
        Returns:
            Dictionary with collection information
        """
        try:
            return {
                "name": self.collection.name,
                "count": self.collection.count()
            }
        except Exception as e:
            print(f"Error getting collection info: {e}")
            return {"name": "unknown", "count": 0}