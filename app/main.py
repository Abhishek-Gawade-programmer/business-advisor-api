from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from advisor_crew import process_challenge_with_crew
from app.schemas import ChallengeRequest, ChallengeResponse


app = FastAPI(
    title="Business Advisor API",
    description="A FastAPI application that simulates a business advisor loop using crewAI",
    version="0.1.0",
)


@app.post("/api/challenge", response_model=ChallengeResponse)
async def api_process_challenge(request: ChallengeRequest):
    """
    Process a business challenge through multiple advisors using crewAI.

    Each advisor provides a text response and numerical scores for Capital, Market, and Model.
    """
    if not request.challenge or len(request.challenge.strip()) == 0:
        raise HTTPException(status_code=400, detail="Challenge text cannot be empty")

    advisor_responses = await process_challenge_with_crew(request.challenge)

    return {
        "challenge": request.challenge,
        "advisor_responses": advisor_responses,
    }


@app.get("/")
def read_root():
    """Welcome to the Business Advisor API powered by crewAI"""
    return {
        "message": "Welcome to the Business Advisor API. Send POST requests to /api/challenge"
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
