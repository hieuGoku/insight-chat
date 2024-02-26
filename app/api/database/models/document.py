from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel


class BaseDocumentSchema(BaseModel):
    text: str
    metadata: Dict[str, str]
    excluded_embed_metadata_keys: Optional[list]
    excluded_llm_metadata_keys: Optional[list]
    relationships: Dict[str, str]


class DocumentCreateSchema(BaseDocumentSchema):
    pass


class DocumentUpdateSchema(BaseDocumentSchema):
    id: str


class DocumentSchema(BaseDocumentSchema):
    id: str
    # created_at: datetime.now()
    # updated_at: datetime.now()


