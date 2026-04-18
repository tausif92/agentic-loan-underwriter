from typing import List
from shared.schemas.loan_application import Document
from shared.schemas.document_schema import ParsedDocument
from agents.document_agent import DocumentAgent
from backend.core.logger import logger


class DocumentService:

    def __init__(self):
        self.agent = DocumentAgent()

    def process_documents(self, documents: List[Document]) -> List[ParsedDocument]:
        logger.info("Processing documents...")
        parsed_docs = []

        for doc in documents:
            parsed = self.agent.parse_document(doc)
            parsed_docs.append(parsed)

        return parsed_docs
