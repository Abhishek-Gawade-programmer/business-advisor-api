import os
import asyncio
import json
import re
from typing import List, Dict, Any
from crewai import Agent, Task, Crew, Process
from crewai.tasks.task_output import TaskOutput

# Set any required environment variables for your LLM provider
# For example, if using OpenAI: os.environ["OPENAI_API_KEY"] = "your-api-key"

# Define the financial expert agent
financial_expert = Agent(
    role="Financial Expert",
    goal="Analyze business challenges from a financial perspective and provide capital allocation advice",
    backstory="""You are a seasoned financial expert with decades of experience in investment 
    banking and corporate finance. You excel at analyzing the financial implications of 
    business strategies and providing guidance on capital allocation, funding approaches, 
    and financial risk management.""",
    verbose=True,
    allow_delegation=False,
)

# Define the market strategist agent
market_strategist = Agent(
    role="Market Strategist",
    goal="Analyze market dynamics and provide strategic positioning advice",
    backstory="""You are an experienced market strategist who has helped numerous 
    companies navigate competitive landscapes and identify growth opportunities. 
    You excel at analyzing market trends, customer behavior, and competitive positioning 
    to provide actionable market strategies.""",
    verbose=True,
    allow_delegation=False,
)

# Define the business model innovator agent
business_model_innovator = Agent(
    role="Business Model Innovator",
    goal="Provide innovative business model recommendations to address challenges",
    backstory="""You are a forward-thinking business model innovator who has helped 
    transform companies across various industries. You specialize in identifying opportunities 
    for value creation through innovative business models, revenue streams, and 
    organizational structures.""",
    verbose=True,
    allow_delegation=False,
)


def extract_scores(text: str) -> Dict[str, float]:
    """
    Extract capital, market, and model scores from advisor response text.
    Expected format in text: "...Scores: Capital: 7.5, Market: 8.2, Model: 6.9..."

    Args:
        text: The full response text from an advisor

    Returns:
        Dictionary with extracted scores
    """
    default_scores = {"capital": 5.0, "market": 5.0, "model": 5.0}

    # Look for scores in the format "Capital: 7.5"
    capital_match = re.search(r"Capital:\s*(\d+(\.\d+)?)", text, re.IGNORECASE)
    market_match = re.search(r"Market:\s*(\d+(\.\d+)?)", text, re.IGNORECASE)
    model_match = re.search(r"Model:\s*(\d+(\.\d+)?)", text, re.IGNORECASE)

    if capital_match:
        default_scores["capital"] = float(capital_match.group(1))
    if market_match:
        default_scores["market"] = float(market_match.group(1))
    if model_match:
        default_scores["model"] = float(model_match.group(1))

    return default_scores


def create_advisor_task(agent, challenge: str) -> Task:
    """
    Create a task for an advisor agent to analyze the business challenge.

    Args:
        agent: The crewAI agent to assign the task to
        challenge: The business challenge text

    Returns:
        A crewAI Task object
    """
    return Task(
        description=f"""
        Analyze the following business challenge from your perspective as a {agent.role}:
        
        "{challenge}"
        
        Provide your expert advice and recommendations. 
        
        At the end of your response, include numerical scores (from 1.0 to 10.0) 
        for the following aspects:
        - Capital: Score reflecting capital requirements or financial impact
        - Market: Score reflecting market opportunity or competitive advantage
        - Model: Score reflecting business model innovation or structural changes
        
        Format your scores section at the end like this:
        "Scores: Capital: X.X, Market: X.X, Model: X.X"
        """,
        agent=agent,
        async_execution=True,
        expected_output=f"""
        Detailed analysis of the challenge from a {agent.role.lower()} perspective,
        with specific recommendations and clearly formatted scores.
        """,
    )


async def process_challenge_with_crew(challenge: str) -> List[Dict[str, Any]]:
    """
    Process a business challenge through the advisor crew asynchronously.

    Args:
        challenge: The business challenge text

    Returns:
        A list of advisor responses with their scores
    """
    # Create tasks for each advisor
    financial_task = create_advisor_task(financial_expert, challenge)
    market_task = create_advisor_task(market_strategist, challenge)
    business_model_task = create_advisor_task(business_model_innovator, challenge)

    # Create the crew with async process
    advisor_crew = Crew(
        agents=[financial_expert, market_strategist, business_model_innovator],
        tasks=[financial_task, market_task, business_model_task],
        process=Process.sequential,  # Using sequential for simplicity but could be Process.hierarchical
        verbose=True,
    )

    # Run the crew asynchronously using asyncio.run_in_executor
    # This allows the synchronous kickoff method to run without blocking
    loop = asyncio.get_running_loop()
    crew_results = await loop.run_in_executor(None, advisor_crew.kickoff)

    # Process results to extract scores and format responses
    advisor_responses = []

    # Map task outputs to their respective advisors
    task_outputs = crew_results if isinstance(crew_results, list) else [crew_results]

    # Map agents to their IDs for the API response
    agent_id_map = {
        "Financial Expert": "financial_expert",
        "Market Strategist": "market_strategist",
        "Business Model Innovator": "business_model_innovator",
    }

    for task_output in task_outputs:
        print(task_output)
        if isinstance(task_output, TaskOutput):
            # Get the task and associated agent
            task = task_output.task
            agent = task.agent
            response_text = task_output.raw_output

            # Extract scores from the response
            scores = extract_scores(response_text)

            # Clean up the response text (remove the scores section if desired)
            # This is optional - you might want to keep the scores in the text
            clean_response = re.sub(
                r"Scores:.*$", "", response_text, flags=re.DOTALL
            ).strip()

            advisor_responses.append(
                {
                    "advisor_id": agent_id_map.get(agent.role, "unknown_advisor"),
                    "response": clean_response,
                    "scores": scores,
                }
            )

    return advisor_responses
