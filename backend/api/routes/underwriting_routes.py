from fastapi import APIRouter
from shared.schemas.loan_application import LoanApplication
from agents.underwriting_agent import graph

router = APIRouter()


@router.post("/underwrite")
def underwrite(application: LoanApplication):
    result = graph.invoke({
        "application": application
    })

    return result["decision"]
