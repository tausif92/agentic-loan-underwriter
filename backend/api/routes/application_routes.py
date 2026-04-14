from fastapi import APIRouter
from shared.schemas.loan_application import LoanApplication
from backend.services.document_service import DocumentService
from backend.services.tool_service import ToolService

tool_service = ToolService()
router = APIRouter()
document_service = DocumentService()


@router.post("/applications")
def submit_application(application: LoanApplication):
    return {
        "application_id": application.application_id,
        "status": "submitted"
    }


@router.post("/applications/process-documents")
def process_documents(application: LoanApplication):
    parsed_docs = document_service.process_documents(application.documents)

    return {
        "application_id": application.application_id,
        "parsed_documents": parsed_docs
    }


@router.get("/test-tools")
def test_tools():
    return {
        "credit_score": tool_service.get_credit_score("user_001"),
        "identity": tool_service.verify_identity("John Doe"),
        "dti": tool_service.calculate_dti(120000, 50000)
    }
