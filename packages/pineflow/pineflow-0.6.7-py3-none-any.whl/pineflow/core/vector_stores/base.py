from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from pineflow.core.document.schema import Document


class BaseVectorStore(ABC):
    """An interface for vector store."""

    @classmethod
    def class_name(cls) -> str:
        return "BaseVectorStore"

    @abstractmethod
    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to vector store."""

    @abstractmethod
    def query(self, query: str, top_k: int = 4) -> List[Document]:
        """Query vector store."""

    @abstractmethod
    def delete_documents(self, ids: List[str]) -> None:
        """Delete documents from vector store."""
    
    @abstractmethod
    def get_all_documents(self, include_fields: List[str]) -> List[Dict[str, Dict]]:
        """Get all documents from vector store."""
             
    def get_all_document_hashes(self) -> Tuple[List[str], List[str], List[str]]:
        """Get all ref hashes from vector store."""
        hits = self.get_all_documents(include_fields=["metadata"])
        
        ids = [hit["_source"]["_id"] for hit in hits]
        hashes = [hit["_source"]["metadata"].get("hash") for hit in hits]
        ref_hashes = [hit["_source"]["metadata"].get("ref_doc_hash") for hit in hits]
        
        return ids, hashes, ref_hashes
        