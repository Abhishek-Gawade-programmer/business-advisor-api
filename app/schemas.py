from typing import List, Dict, Any
from pydantic import BaseModel


class ChallengeRequest(BaseModel):
    challenge: str

    class Config:
        json_schema_extra = {
            "example": {
                "challenge": "How can we increase our market share in the renewable energy sector?"
            }
        }


class AdvisorScore(BaseModel):
    capital: float
    market: float
    model: float


class AdvisorResponse(BaseModel):
    advisor_id: str
    response: str
    scores: AdvisorScore


class ChallengeResponse(BaseModel):
    challenge: str
    advisor_responses: List[AdvisorResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "challenge": "How can we increase our market share in the renewable energy sector?",
                "advisor_responses": [
                    {
                        "advisor_id": "financial_expert",
                        "response": "You should consider allocating resources to R&D...",
                        "scores": {"capital": 7.5, "market": 8.2, "model": 6.9},
                    }
                ],
            }
        }
