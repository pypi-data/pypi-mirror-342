import os
from dotenv import load_dotenv
from gemini_agent import Agent

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

    # Use the agent
    response = agent.prompt(user_prompt="multiply 3 and 7 then add 5 to the result" ,
    system_prompt="You are a helpful assistant give your response always with ❤️ at the start of the line. in your response you should mention the function you used." ,
    response_structure=
    {
        "type": "object",
        "properties": {
            "used_functions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "function_name": {"type": "string"},
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "a": {"type": "integer"},
                                "b": {"type": "integer"}
                            }
                        }
                    }
                }
            },
            "answer": {"type": "string"}
            
        }
    }
    )
    print(response)  # Should output 21

if __name__ == "__main__":
    test_basic_operations() 