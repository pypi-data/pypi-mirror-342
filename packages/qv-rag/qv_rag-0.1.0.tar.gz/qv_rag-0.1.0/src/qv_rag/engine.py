"""
Main RAG engine
"""

from typing import List, Dict, Optional, Union, Any
from pathlib import Path
from .storage import ChromaStorage
from .text_splitter import TextSplitter


class RAGEngine:
    """Main RAG engine class"""
    
    def __init__(
        self,
        collection_name: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        persist_directory: Optional[str] = None,
    ):
        """
        Initialize the RAG engine.
        
        Args:
            collection_name: Name of the ChromaDB collection
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            persist_directory: Optional directory to persist the database
        """
        self.text_splitter = TextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        self.storage = ChromaStorage(
            collection_name=collection_name,
            persist_directory=persist_directory
        )
    
    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        split_type: str = "text"
    ) -> None:
        """
        Add texts to the RAG engine.
        
        Args:
            texts: List of text documents to add
            metadatas: Optional metadata for each document
            split_type: Type of text splitting ("text", "markdown", "html", "json")
        """
        if not texts:
            return
            
        # Split texts based on type
        if split_type == "text":
            chunks = self.text_splitter.split_texts(texts)
        elif split_type == "markdown":
            chunks = []
            for text in texts:
                chunks.extend(self.text_splitter.split_markdown(text))
        elif split_type == "html":
            chunks = []
            for text in texts:
                chunks.extend(self.text_splitter.split_html_semantic(text))
        elif split_type == "json":
            chunks = []
            for text in texts:
                chunks.extend(self.text_splitter.split_json(text))
        else:
            raise ValueError(f"Unsupported split_type: {split_type}")
        
        # Handle metadata replication if provided
        chunk_metadatas = None
        if metadatas:
            chunk_metadatas = []
            for i, text in enumerate(texts):
                # Get number of chunks for this text
                if split_type == "text":
                    text_chunks = self.text_splitter.split_text(text)
                elif split_type == "markdown":
                    text_chunks = self.text_splitter.split_markdown(text)
                elif split_type == "html":
                    text_chunks = self.text_splitter.split_html_semantic(text)
                elif split_type == "json":
                    text_chunks = self.text_splitter.split_json(text)
                
                # Replicate metadata for each chunk
                for chunk in text_chunks:
                    chunk_metadatas.append(metadatas[i])
        
        # Add chunks to storage
        self.storage.add_texts(chunks, chunk_metadatas)
    
    def add_file(
        self,
        file_path: Union[str, Path],
        metadata: Optional[Dict[str, Any]] = None,
        file_type: Optional[str] = None
    ) -> None:
        """
        Add a file to the RAG engine.
        
        Args:
            file_path: Path to the file
            metadata: Optional metadata for the file
            file_type: Optional file type override
        """
        file_path = Path(file_path)
        
        # Determine file type if not provided
        if file_type is None:
            file_type = file_path.suffix.lower()[1:]  # Remove dot
            
        # Map file extensions to split types
        split_type_map = {
            "txt": "text",
            "md": "markdown",
            "html": "html",
            "htm": "html",
            "json": "json"
        }
        
        # Get the appropriate split type
        split_type = split_type_map.get(file_type, "text")
        
        # Add metadata
        if metadata is None:
            metadata = {}
        metadata["source"] = str(file_path)
        metadata["file_type"] = file_type
        
        # Read and process the file
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        self.add_texts([text], [metadata], split_type=split_type)
    
    def query(
        self,
        query_text: str,
        top_k: int = 5,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Query the RAG engine.
        
        Args:
            query_text: The query text
            top_k: Number of results to return
            where: Optional metadata filter
            where_document: Optional document content filter
            
        Returns:
            List of results with documents and metadata
        """
        return self.storage.query(
            query_text=query_text,
            top_k=top_k,
            where=where,
            where_document=where_document
        )
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the RAG engine.
        
        Returns:
            Dictionary with engine information
        """
        return self.storage.get_collection_info()