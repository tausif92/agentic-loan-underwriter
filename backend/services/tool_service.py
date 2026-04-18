import requests

from backend.core.logger import logger
import os


class ToolService:

    BASE_URL = os.getenv("MCP_BASE_URL", "http://localhost:8001")

    def get_credit_score(self, applicant_id: str):
        logger.info("Fetching credit score...")
        response = requests.get(f"{self.BASE_URL}/credit-score/{applicant_id}")
        return response.json()

    def verify_identity(self, name: str):
        logger.info("Verifying identity...")
        response = requests.get(
            f"{self.BASE_URL}/verify-identity", params={"name": name})
        return response.json()

    def calculate_dti(self, income: float, loan_amount: float):
        logger.info("Calculating DTI...")
        response = requests.get(
            f"{self.BASE_URL}/calculate-dti",
            params={"income": income, "loan_amount": loan_amount}
        )
        return response.json()
