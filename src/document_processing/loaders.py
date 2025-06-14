# Document Loader

from abc import ABC, abstractmethod
from typing import List, Optional
import tempfile
import os
from pathlib import Path
from datetime import datetime

try:
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
    from langchain.schema import Document

except:
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
    from langchain.schema import Document

class BaseDocumentLoader(ABC):
    """Abstract base class for document loaders"""

    @abstractmethod
    def load(self, file_path: str)-> List[Document]:
        pass

class PDFDocumentLoader(BaseDocumentLoader):
    """Load PDF documents"""

    def load(self, file_path: str) -> List[Document]:
        try:
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            return docs
        except Exception as e:
            raise Exception(f"Error loading PDF {file_path}: {str(e)}")

class TextDocumentLoader(BaseDocumentLoader):
    """load text documents"""

    def load(self, file_path: str)-> List[Document]:
        try:
            loader = TextLoader(file_path, encoding='utf-8')
            docs = loader.load()
            return docs
        except Exception as e:
            raise Exception(f"Error loading text file {file_path}: {str(e)}")

class DocumentLoaderFactory:
    """Factory for creating document loaders"""

    _loaders = {
        '.pdf':PDFDocumentLoader,
        '.txt':TextDocumentLoader
    }

    @classmethod
    def get_loader(cls, file_extension: str) -> Optional[BaseDocumentLoader]:
        """Get appropriate loader for file extension"""
        loader_class = cls._loaders.get(file_extension.lower())
        if loader_class:
            return loader_class()
        return None

    @classmethod
    def load_documents(cls, uploaded_files)-> List[Document]:
        """load documents from uploaded files"""
        documents = []

        for uploaded_file in uploaded_files:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            try:
                # Get file extension
                file_ext = Path(uploaded_file.name).suffix

                # Get appropriate loader
                loader = cls.get_loader(file_ext)
                if not loader:
                    raise Exception(f"Unsupported file type: {file_ext}")

                # Load Documents
                docs = loader.load(tmp_path)

                # Add metadata
                for doc in docs:
                    doc.metadata.update({
                        'source': uploaded_file.name,
                        'file_type':file_ext,
                        'upload_time': str(datetime.now())
                    })

                documents.extend(docs)

            finally:
                # Clean up temporary file
                os.unlink(tmp_path)


        return documents