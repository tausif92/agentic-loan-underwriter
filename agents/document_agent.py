from shared.schemas.loan_application import Document
from shared.schemas.document_schema import ParsedDocument
from openai import OpenAI
import json
from backend.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


class DocumentAgent:

    def parse_document(self, document: Document) -> ParsedDocument:
        # For now: simulate reading file (later we integrate real PDF parsing)
        file_content = f"Simulated content of {document.document_type}"

        prompt = f"""
        You are a financial document parser.

        Extract structured information from this document:

        Document Type: {document.document_type}
        Content: {file_content}

        Return JSON with key financial fields.
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are an expert financial document parser."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        extracted_text = response.choices[0].message.content

        try:
            extracted_data = json.loads(extracted_text)
            confidence = 0.9
        except:
            extracted_data = {"raw_text": extracted_text}
            confidence = 0.5

        return ParsedDocument(
            document_id=document.document_id,
            document_type=document.document_type,
            extracted_data=extracted_data,
            confidence_score=confidence
        )
