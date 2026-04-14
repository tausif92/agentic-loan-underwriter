from fastapi import FastAPI
from tools.credit_tool import get_credit_score
from tools.identity_tool import verify_identity
from tools.dti_tool import calculate_dti

app = FastAPI()


@app.get("/")
def home():
    return {"message": "MCP Server API"}


@app.get("/health")
def health():
    return {"status": "MCP Server Running"}


@app.get("/credit-score/{applicant_id}")
def credit_score(applicant_id: str):
    return get_credit_score(applicant_id)


@app.get("/verify-identity")
def identity(name: str):
    return verify_identity(name)


@app.get("/calculate-dti")
def dti(income: float, loan_amount: float):
    return calculate_dti(income, loan_amount)
