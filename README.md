# Business Advisor API using crewAI

A FastAPI application that simulates a business advisor loop using the crewAI framework for agent-based task execution. The application accepts a business challenge and routes it through three advisor agents, each providing specialized advice and numerical scores.

## Features

- FastAPI with Pydantic models for request/response validation
- crewAI for agent-based task execution
- Asynchronous execution of advisor tasks
- Swagger documentation (OpenAPI)
- Three specialized advisor agents:
  - Financial Expert (capital-focused)
  - Market Strategist (market-focused)
  - Business Model Innovator (model-focused)
- Structured JSON responses with scores and advice

## Requirements

- Python 3.12+
- Dependencies listed in `pyproject.toml`

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   uv pip install -e .
   ```
4. Configure your LLM API key:
   - Create a `.env` file in the project root
   - Add your API key (e.g., `OPENAI_API_KEY=your-api-key-here`)

## Running the Application

The server will start at http://localhost:8000

## API Endpoints

### POST /api/challenge

Accepts a business challenge and processes it through the advisor loop.

#### Request Format

```json
{
  "challenge": "How can we increase our market share in the renewable energy sector?"
}
```

#### Response Format

```json
{
  "challenge": "How can we increase our market share in the renewable energy sector?",
  "advisor_responses": [
    {
      "advisor_id": "financial_expert",
      "response": "From a financial perspective, increasing your market share in the renewable energy sector requires careful consideration of capital allocation. I recommend focusing on three key areas...",
      "scores": {
        "capital": 8.5,
        "market": 6.2,
        "model": 5.9
      }
    },
    {
      "advisor_id": "market_strategist",
      "response": "The renewable energy sector presents significant opportunities for market expansion. Based on current trends...",
      "scores": {
        "capital": 5.3,
        "market": 9.1,
        "model": 6.4
      }
    },
    {
      "advisor_id": "business_model_innovator",
      "response": "To increase market share in renewable energy, I suggest rethinking your current business model. Consider shifting from...",
      "scores": {
        "capital": 6.1,
        "market": 7.5,
        "model": 9.2
      }
    }
  ]
}
```

## Documentation

- Interactive API documentation is available at http://localhost:8000/docs
- Alternative documentation is available at http://localhost:8000/redoc

## Code Structure

- `main.py`: Contains the FastAPI application, routes, and Pydantic models
- `advisor_crew.py`: Contains the crewAI agent definitions, tasks, and crew configuration
- `requirements.txt`: Lists all required dependencies

## Implementation Details

### crewAI Integration

The application leverages crewAI's agent-based architecture to create specialized advisors that can process business challenges. Each agent has:

- A defined role and goal
- A detailed backstory to guide their responses
- A specific task to analyze the challenge from their perspective

### Asynchronous Execution

The application uses crewAI's process execution capabilities combined with asyncio to handle advisor tasks concurrently:

```python
async def process_challenge_with_crew(challenge: str) -> List[Dict[str, Any]]:
    """
    Process a business challenge through the advisor crew asynchronously.

    Args:
        challenge: The business challenge text

    Returns:
        List of dictionaries containing advisor responses and scores
    """
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

    crew_results_financial = advisor_crew_financial.kickoff_async()
    crew_results_market = advisor_crew_market.kickoff_async()
    crew_results_business_model = advisor_crew_business_model.kickoff_async()


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
```

https://docs.crewai.com/concepts/tasks#using-output-pydantic Pdantic model that the task output should conform to.

sample payload:

https://privatebin.net/?91b534634e81161a#BZWk77N8pvaxMaS5B28hXfvctUgfNhdCbEUhxAJpwptp
