import os
from dotenv import load_dotenv
from src.gemini_agent import Agent

load_dotenv()

def test_basic_operations():
    # Define some basic math operations
    @Agent.description("Multiplies two numbers.")
    @Agent.parameters({
        'a': {'type': int, 'description': 'The first number'},
        'b': {'type': int, 'description': 'The second number'}
    })
    def multiply(a: int, b: int) -> int:
        return a * b

    @Agent.description("Adds two numbers.")
    @Agent.parameters({
        'a': {'type': int, 'description': 'The first number'},
        'b': {'type': int, 'description': 'The second number'}
    })
    def add(a: int, b: int) -> int:
        return a + b

    # Create an agent with the math tools
    agent = Agent(
        api_key=os.getenv("GEMINI_API_KEY"),
        tools=[multiply, add]
    )

    # Test a simple multiplication
    response = agent.prompt("Multiply 3 and 7")
    print(f"Multiplication result: {response}")  # Should be 21

    # Test a complex operation
    response = agent.prompt(
        "Multiply 3 and 7, then add 4 to the result",
        response_structure={
            "type": "object",
            "properties": {
                "result": {"type": "number"}
            }
        }
    )
    print(f"Complex operation result: {response}")  # Should be {"result": 25}

if __name__ == "__main__":
    test_basic_operations() 