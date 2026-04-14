from langgraph.graph import StateGraph
from typing import TypedDict, List
from shared.schemas.loan_application import LoanApplication
from shared.schemas.document_schema import ParsedDocument
from shared.schemas.decision_schema import Decision
from backend.services.document_service import DocumentService
from backend.services.tool_service import ToolService
from openai import OpenAI
from backend.core.config import OPENAI_API_KEY
import json

client = OpenAI(api_key=OPENAI_API_KEY)


# 🧠 Define State
class UnderwritingState(TypedDict):
    application: LoanApplication
    parsed_documents: List[ParsedDocument]
    tool_results: dict
    decision: dict


document_service = DocumentService()
tool_service = ToolService()


# 🧩 Step 1: Process Documents
def process_documents(state: UnderwritingState):
    parsed_docs = document_service.process_documents(
        state["application"].documents)
    return {"parsed_documents": parsed_docs}


# 🧩 Step 2: Call Tools
def call_tools(state: UnderwritingState):
    app = state["application"]

    credit = tool_service.get_credit_score(app.applicant.applicant_id)
    identity = tool_service.verify_identity(app.applicant.name)
    dti = tool_service.calculate_dti(
        app.applicant.annual_income,
        app.loan_details.loan_amount
    )

    return {
        "tool_results": {
            "credit_score": credit,
            "identity": identity,
            "dti": dti
        }
    }


# 🧩 Step 3: Decision Making
def make_decision(state: UnderwritingState):
    app = state["application"]

    prompt = f"""
    You are an AI loan underwriter.

    Applicant Info:
    {app}

    Parsed Documents:
    {state['parsed_documents']}

    Tool Results:
    {state['tool_results']}

    Return STRICT JSON in this format:
    {{
      "application_id": "...",
      "decision": "APPROVED | REJECTED | REVIEW",
      "risk_score": 0.0 to 1.0,
      "reasons": [
        {{
          "factor": "...",
          "impact": "high | medium | low",
          "description": "..."
        }}
      ],
      "policy_checks": {{}},
      "supporting_data": {{}}
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a strict financial risk decision engine. Always return valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        decision_dict = json.loads(content)

        # 🔒 VALIDATION STEP (CRITICAL)
        decision = Decision(**decision_dict)

        return {"decision": decision.dict()}

    except Exception as e:
        # 🚨 Guardrail fallback
        return {
            "decision": {
                "application_id": app.application_id,
                "decision": "REVIEW",
                "risk_score": 0.5,
                "reasons": [
                    {
                        "factor": "system_error",
                        "impact": "high",
                        "description": "Failed to parse LLM output"
                    }
                ],
                "policy_checks": {},
                "supporting_data": {
                    "error": str(e),
                    "raw_output": content
                }
            }
        }


# 🧠 Build Graph
def build_graph():
    builder = StateGraph(UnderwritingState)

    builder.add_node("process_documents", process_documents)
    builder.add_node("call_tools", call_tools)
    builder.add_node("make_decision", make_decision)

    builder.set_entry_point("process_documents")

    builder.add_edge("process_documents", "call_tools")
    builder.add_edge("call_tools", "make_decision")

    return builder.compile()


graph = build_graph()
