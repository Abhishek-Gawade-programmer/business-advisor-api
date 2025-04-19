import asyncio
import json
from app.advisor_crew import process_challenge_with_crew


async def main():
    """
    Example script to demonstrate using the advisor crew system directly.

    This shows how to process a business challenge asynchronously and get the results
    from all three advisors.
    """
    # Example business challenge
    challenge = "How can we increase our market share in the renewable energy sector?"

    print(f"Processing challenge: {challenge}")
    print("This may take a few minutes as each agent thinks through the problem...")

    # Process the challenge using our async function
    advisor_responses = await process_challenge_with_crew(challenge)

    # Display the formatted results
    print("\n===== ADVISOR RESPONSES =====\n")
    for response in advisor_responses:
        print(f"Advisor: {response['advisor_id']}")
        print("---")
        print(response["response"])
        print("---")
        print(
            f"Scores: Capital: {response['scores']['capital']}, "
            f"Market: {response['scores']['market']}, "
            f"Model: {response['scores']['model']}"
        )
        print("\n" + "=" * 50 + "\n")

    # Also output as JSON for reference
    print("\nJSON Output:")
    print(
        json.dumps(
            {"challenge": challenge, "advisor_responses": advisor_responses}, indent=2
        )
    )


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
