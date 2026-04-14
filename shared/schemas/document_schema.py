from pydantic import BaseModel
from typing import Dict


class ParsedDocument(BaseModel):
    document_id: str
    document_type: str
    extracted_data: Dict  # flexible for different document types
    confidence_score: float
