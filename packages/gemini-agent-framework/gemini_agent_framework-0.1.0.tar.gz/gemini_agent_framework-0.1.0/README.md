# Gemini Agent Framework

A Python framework for building agents that use Gemini's function calling capabilities. This framework allows you to easily create agents that can break down complex tasks into sequential steps using available tools.

## Installation

```bash
pip install gemini-agent-framework
```

## Quick Start

```python
from gemini_agent import Agent
from dotenv import load_dotenv

load_dotenv()

# Define your tools
@Agent.description("Multiplies two numbers.")
@Agent.parameters({
    'a': {'type': int, 'description': 'The first number'},
    'b': {'type': int, 'description': 'The second number'}
})
def multiply(a: int, b: int) -> int:
    return a * b

# Create an agent instance
agent = Agent(api_key="your-api-key", tools=[multiply])

# Use the agent
response = agent.prompt("Multiply 3 and 7")
print(response)  # Should output 21
```

## Features

- Easy tool definition using decorators
- Automatic sequential task breakdown
- Support for structured responses
- Intermediate result handling
- Error handling and recovery

## Documentation

For more detailed documentation, please visit the [documentation page](https://github.com/yourusername/gemini-agent-framework#readme).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 