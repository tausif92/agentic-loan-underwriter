from pydantic import BaseModel, Field
from typing import List, Optional


class Applicant(BaseModel):
    applicant_id: str
    name: str
    age: int
    employment_status: str
    annual_income: float


class LoanDetails(BaseModel):
    loan_amount: float
    loan_purpose: str
    tenure_months: int


class Document(BaseModel):
    document_id: str
    document_type: str  # bank_statement, tax_return, id_proof
    file_path: str


class LoanApplication(BaseModel):
    application_id: str
    applicant: Applicant
    loan_details: LoanDetails
    documents: List[Document]
