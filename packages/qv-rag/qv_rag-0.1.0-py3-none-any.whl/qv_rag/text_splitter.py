"""
Text splitter module for the RAG engine
"""

from typing import List, Dict, Optional, Any, Callable, Union
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
    RecursiveJsonSplitter,
    HTMLHeaderTextSplitter,
    HTMLSemanticPreservingSplitter
)
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path


class TextSplitter:
    """Text splitter class for the RAG engine"""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: List[str] = None,
        length_function: Callable[[str], int] = len,
        max_json_chunk_size: int = 300,
        html_headers_to_split_on: List[tuple] = None,
        html_elements_to_preserve: List[str] = None,
        html_custom_handlers: Dict[str, Callable] = None,
    ):
        """
        Initialize the text splitter.
        
        Args:
            chunk_size: The size of each chunk.
            chunk_overlap: The overlap between chunks.
            separators: The separators to use for splitting the text.
                        Defaults to ["\n\n", "\n", " ", ""]
            length_function: Function to measure chunk size. Defaults to len.
            max_json_chunk_size: Maximum size for JSON chunks.
            html_headers_to_split_on: List of tuples for HTML header splitting.
            html_elements_to_preserve: List of HTML elements to preserve.
            html_custom_handlers: Custom handlers for HTML elements.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators
        self.length_function = length_function
        self.max_json_chunk_size = max_json_chunk_size
        
        # Create the recursive character text splitter
        splitter_args = {
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "length_function": self.length_function,
        }
        
        if self.separators:
            splitter_args["separators"] = self.separators
            
        self.splitter = RecursiveCharacterTextSplitter(**splitter_args)
        
        # Create markdown splitter
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ]
        )
        
        # Create JSON splitter
        self.json_splitter = RecursiveJsonSplitter(max_chunk_size=self.max_json_chunk_size)
        
        # Create HTML splitters
        self.html_header_splitter = HTMLHeaderTextSplitter(
            headers_to_split_on=html_headers_to_split_on or [
                ("h1", "Header 1"),
                ("h2", "Header 2"),
                ("h3", "Header 3"),
            ]
        )
        
        self.html_semantic_splitter = HTMLSemanticPreservingSplitter(
            headers_to_split_on=html_headers_to_split_on or [
                ("h1", "Header 1"),
                ("h2", "Header 2"),
                ("h3", "Header 3"),
            ],
            max_chunk_size=self.chunk_size,
            separators=self.separators or ["\n\n", "\n", ". "],
            elements_to_preserve=html_elements_to_preserve or ["table", "ul", "ol"],
            custom_handlers=html_custom_handlers or {},
        )
    
    def split_text(self, text: str) -> List[str]:
        """
        Split a text into chunks.
        
        Args:
            text: The text to split.
            
        Returns:
            A list of text chunks.
        """
        return self.splitter.split_text(text)
    
    def split_texts(self, texts: List[str]) -> List[str]:
        """
        Split multiple texts into chunks.
        
        Args:
            texts: The texts to split.
            
        Returns:
            A list of text chunks.
        """
        chunks = []
        for text in texts:
            chunks.extend(self.split_text(text))
        return chunks
    
    def create_documents(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Split texts and create documents with metadata.
        
        Args:
            texts: The texts to split.
            metadatas: Optional metadata for each text.
            
        Returns:
            A list of documents with text chunks and metadata.
        """
        return self.splitter.create_documents(texts, metadatas)
    
    def split_pdf(self, pdf_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Split a PDF document into chunks with metadata.
        
        Args:
            pdf_path: Path to the PDF file.
            
        Returns:
            A list of documents with text chunks and metadata.
        """
        # Load PDF
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        
        # Extract text and metadata from all pages
        texts = [page.page_content for page in pages]
        metadatas = [{"page": i + 1, "source": str(pdf_path)} for i in range(len(pages))]
        
        # Split and create documents with metadata
        return self.create_documents(texts, metadatas)
    
    def split_markdown(self, markdown_text: str) -> List[Dict[str, Any]]:
        """
        Split a markdown document into chunks with header metadata.
        
        Args:
            markdown_text: The markdown text to split.
            
        Returns:
            A list of documents with text chunks and header metadata.
        """
        return self.markdown_splitter.split_text(markdown_text)
    
    def split_json(self, json_data: Union[str, Dict, List], convert_lists: bool = False) -> List[Dict[str, Any]]:
        """
        Split a JSON document into chunks while preserving structure.
        
        Args:
            json_data: The JSON data to split (can be string, dict, or list).
            convert_lists: Whether to convert lists to dicts for better splitting.
            
        Returns:
            A list of documents with JSON chunks and metadata.
        """
        return self.json_splitter.create_documents(
            texts=[json_data] if isinstance(json_data, (dict, list)) else [json_data],
            convert_lists=convert_lists
        )
    
    def split_html_by_headers(self, html_text: str) -> List[Dict[str, Any]]:
        """
        Split HTML text by headers while preserving header metadata.
        
        Args:
            html_text: The HTML text to split.
            
        Returns:
            A list of documents with text chunks and header metadata.
        """
        return self.html_header_splitter.split_text(html_text)
    
    def split_html_semantic(self, html_text: str) -> List[Dict[str, Any]]:
        """
        Split HTML text while preserving semantic structure.
        
        Args:
            html_text: The HTML text to split.
            
        Returns:
            A list of documents with text chunks and metadata.
        """
        return self.html_semantic_splitter.split_text(html_text) 