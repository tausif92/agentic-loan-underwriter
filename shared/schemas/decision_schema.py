from pydantic import BaseModel, Field
from typing import List, Dict


class RiskFactor(BaseModel):
    factor: str = Field(..., description="Risk factor name")
    impact: str = Field(..., description="high, medium, low")
    description: str


class Decision(BaseModel):
    application_id: str
    decision: str = Field(..., description="APPROVED / REJECTED / REVIEW")
    risk_score: float = Field(..., ge=0, le=1)
    reasons: List[RiskFactor]
    policy_checks: Dict
    supporting_data: Dict
