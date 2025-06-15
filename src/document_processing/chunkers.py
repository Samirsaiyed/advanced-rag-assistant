# Text chunking strategies

from abc import ABC, abstractmethod
from typing import List
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    SentenceTransformersTokenTextSplitter
)
from  langchain.schema import Document

class BaseChunker(ABC):
    """Abstract base class for document chunkers"""

    @abstractmethod
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        pass

class RecursiveChunker(BaseChunker):
    """Recursive character-based chunking"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function = len,
            separators=["\n\n","\n"," ", ""]
        )

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        return self.splitter.split_documents(documents)

class SentenceChunker(BaseChunker):
    """Sentence-aware chunking"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = SentenceTransformersTokenTextSplitter(
            chunk_overlap=chunk_overlap,
            tokens_per_chunk=chunk_size // 4
        )

class CharacterChunker(BaseChunker):
    """Simple charcter-based chunking"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = CharacterChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator="\n"
        )        

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        return self.splitter.split_documents(documents)

class ChunkerFactory:
    """Factory for creating chunker"""

    _chunkers = {
        'recursive': RecursiveChunker,
        'sentence': SentenceChunker,
        'character': CharacterChunker
    }

    @classmethod
    def get_chunker(cls, chunker_type: str, **kwargs) -> BaseChunker:
        """Get chunk by type"""
        chunker_class = cls._chunkers(chunker_type, RecursiveChunker)
        return chunker_class(**kwargs)