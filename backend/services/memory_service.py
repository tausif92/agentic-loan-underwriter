import chromadb
from shared.schemas.decision_schema import Decision
from backend.core.logger import logger
from openai import OpenAI
from backend.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


class MemoryService:

    def __init__(self):
        self.client = chromadb.Client(
            chromadb.config.Settings(
                persist_directory="data/chroma"
            )
        )

        self.collection = self.client.get_or_create_collection(
            name="underwriting_memory"
        )

    # 🔹 Embedding generator
    def generate_embedding(self, text: str):
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    # 🔹 Build structured representation (CRITICAL)
    def build_memory_text(self, application, decision: Decision):
        return f"""
        income: {application.applicant.annual_income}
        employment: {application.applicant.employment_status}
        loan_amount: {application.loan_details.loan_amount}
        loan_purpose: {application.loan_details.loan_purpose}
        decision: {decision.decision}
        risk_score: {decision.risk_score}
        """

    # 🔹 Store decision with context
    def store_decision(self, application, decision: Decision):
        logger.info("Storing decision in memory...")

        try:
            doc_id = decision.application_id

            text = self.build_memory_text(application, decision)
            embedding = self.generate_embedding(text)

            self.collection.add(
                documents=[text],
                embeddings=[embedding],
                ids=[doc_id],
                metadatas=[{
                    "decision": decision.decision,
                    "risk_score": decision.risk_score,
                    "income": application.applicant.annual_income,
                    "loan_amount": application.loan_details.loan_amount,
                    "loan_purpose": application.loan_details.loan_purpose
                }]
            )

            self.client.persist()
            logger.info(f"Stored memory for {doc_id}")

        except Exception as e:
            logger.error(f"Memory store failed: {e}")

    # 🔹 Build query representation (must match storage!)
    def build_query_text(self, application):
        return f"""
        income: {application.applicant.annual_income}
        employment: {application.applicant.employment_status}
        loan_amount: {application.loan_details.loan_amount}
        loan_purpose: {application.loan_details.loan_purpose}
        """

    # 🔹 Retrieve similar cases
    def retrieve_similar_cases(self, application, n_results: int = 3):
        logger.info("Retrieving similar cases...")

        try:
            query_text = self.build_query_text(application)
            query_embedding = self.generate_embedding(query_text)

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )

            documents = results.get("documents", [])
            metadatas = results.get("metadatas", [])

            logger.info(
                f"Retrieved {len(documents[0]) if documents else 0} cases")

            return {
                "documents": documents,
                "metadatas": metadatas
            }

        except Exception as e:
            logger.error(f"Memory retrieval failed: {e}")
            return {"documents": [], "metadatas": []}
