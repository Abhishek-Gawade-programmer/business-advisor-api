from typing import List, Dict, Any
from crewai import Agent, Task, Crew

from schemas import AdvisorResponse
import asyncio


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
        expected_output=f"""
        Detailed analysis of the challenge from a {agent.role.lower()} perspective,
        with specific recommendations and clearly formatted scores.
        """,
        output_pydantic=AdvisorResponse,
        async_execution=True,
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

    advisor_crew_financial = Crew(
        agents=[financial_expert],
        tasks=[financial_task],
        verbose=True,
    )
    advisor_crew_market = Crew(
        agents=[market_strategist],
        tasks=[market_task],
        verbose=True,
    )
    advisor_crew_business_model = Crew(
        agents=[business_model_innovator],
        tasks=[business_model_task],
        verbose=True,
    )

    # Create tasks for parallel execution
    financial_task_future = advisor_crew_financial.kickoff_async()
    market_task_future = advisor_crew_market.kickoff_async()
    business_model_task_future = advisor_crew_business_model.kickoff_async()

    # Wait for all tasks to complete in parallel
    crew_results = await asyncio.gather(
        financial_task_future,
        market_task_future,
        business_model_task_future,
    )

    # Process results to extract scores and format responses
    advisor_responses = []

    # Map task outputs to their respective advisors
    task_outputs = crew_results if isinstance(crew_results, list) else [crew_results]

    for task_output in task_outputs:
        print("task_output", task_output["advisor_id"])

        advisor_responses.append(
            {
                "advisor_id": task_output["advisor_id"],
                "response": task_output["response"],
                "scores": task_output["scores"],
            }
        )

    return advisor_responses
