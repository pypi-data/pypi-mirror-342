from typing import Optional
import pydantic

__all__ = [
    "Document",
]


class Document(pydantic.BaseModel):
    """基础文档对象"""

    vs_embedding: Optional[bytes] = None
    vs_page_content: Optional[str] = None
    vs_embeddings_score: Optional[float] = None
    vs_rerank_score: Optional[float] = None
    vs_index_name: Optional[str] = None
    vs_kb_id: Optional[str] = None
    vs_doc_id: Optional[str] = None
    vs_page_id: Optional[str] = None
    vs_category: Optional[str] = None
    vs_uid: Optional[str] = None
