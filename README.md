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
- Dependencies listed in `requirements.txt`

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Configure your LLM API key:
   - Create a `.env` file in the project root
   - Add your API key (e.g., `OPENAI_API_KEY=your-api-key-here`)

## Running the Application

```bash
python main.py
```

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
# Run the crew asynchronously
loop = asyncio.get_event_loop()
crew_results = await loop.run_in_executor(None, advisor_crew.kickoff)
```

### Score Extraction

The application extracts numerical scores from the advisors' responses using regular expressions:

```python
# Look for scores in the format "Capital: 7.5"
capital_match = re.search(r"Capital:\s*(\d+(\.\d+)?)", text, re.IGNORECASE)
```

## Future Enhancements

- Implement hierarchical crew processes for more complex analyses
- Add agent memory for maintaining context across multiple challenges
- Implement agent delegation for specialized sub-tasks
- Add a feedback mechanism to improve advisor responses over time
- Create a web interface for easier interaction with the advisor crew
