from typing import Optional
from typing import Dict
from typing import Any

import pydantic
from openai_redis_vectorstore.schemas import Document as DocumentBase

__all__ = [
    "VSPage",
    "Document",
]


class VSPage(pydantic.BaseModel):
    index_name: str
    kb_id: Optional[str] = None
    doc_id: Optional[str] = None
    page_id: Optional[str] = None
    category: Optional[str] = None
    content: str
    metadata: Optional[Dict[str, Any]] = None


class Document(DocumentBase):
    id: Optional[int] = None
    app_label: Optional[str] = None
    model_name: Optional[str] = None
