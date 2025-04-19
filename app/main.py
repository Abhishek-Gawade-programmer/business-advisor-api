from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import asyncio
from typing import List, Dict, Any
from advisor_crew import process_challenge_with_crew

app = FastAPI(
    title="Business Advisor API",
    description="A FastAPI application that simulates a business advisor loop using crewAI",
    version="0.1.0",
)


class ChallengeRequest(BaseModel):
    challenge: str

    class Config:
        schema_extra = {
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
        schema_extra = {
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


@app.post("/api/challenge", response_model=ChallengeResponse)
async def api_process_challenge(request: ChallengeRequest):
    """
    Process a business challenge through multiple advisors using crewAI.

    Each advisor provides a text response and numerical scores for Capital, Market, and Model.
    """
    if not request.challenge or len(request.challenge.strip()) == 0:
        raise HTTPException(status_code=400, detail="Challenge text cannot be empty")

    # Process challenge using crewAI
    try:
        advisor_responses = await process_challenge_with_crew(request.challenge)

        return ChallengeResponse(
            challenge=request.challenge, advisor_responses=advisor_responses
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing challenge: {str(e)}"
        )


@app.get("/")
def read_root():
    """Welcome to the Business Advisor API powered by crewAI"""
    return {
        "message": "Welcome to the Business Advisor API. Send POST requests to /api/challenge"
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
