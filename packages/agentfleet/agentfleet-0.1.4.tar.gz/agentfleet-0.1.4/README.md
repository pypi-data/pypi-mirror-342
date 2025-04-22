# AgentFleet

A Python package for managing AI agents and chatrooms that work with LLM-based capabilities.

## Installation

```bash
pip install agentfleet
```

## Usage

```python
from agentfleet import Agent, Chatroom, create_chatroom

# Example: Create an agent
from langchain_openai import ChatOpenAI
llm = ChatOpenAI()
agent = Agent(name="Assistant", llm=llm, sys_prompt="You are a helpful assistant")

# Example: Set up a chatroom
chatroom = Chatroom(llm=llm, agents=[agent], current_agent=agent)
```

### Using Custom Tools

```python
from agentfleet import create_chatroom
from langchain_core.tools import tool

# Define your custom tool functions
@tool
def lookup_data(query: str) -> str:
    """Look up data from a database."""
    # Implementation...
    return f"Data for {query}"
@tool
def process_request(request_id: str) -> str:
    """Process a request with the given ID."""
    # Implementation...
    return f"Processed request {request_id}"

# Create a dictionary mapping tool names to functions
tool_dict = {
    'lookup_data': lookup_data,
    'process_request': process_request
}

# Create a chatroom with tool dictionary
chatroom_config = {
    "states": [...],
    "agents": [
        {
            "name": "support_agent",
            "sys_prompt": "You are a support agent...",
            "util_tools": ["lookup_data", "process_request"],
            "transfer_tools": []
        }
    ],
    "initial_agent": "support_agent"
}

chatroom = create_chatroom(chatroom_config, llm, tool_dict=tool_dict)
```

## Features

- Create AI agents with different capabilities
- Build chatrooms with multiple specialized agents
- Transfer conversation control between agents
- Maintain conversation state across interactions
- Pass custom tools to agents via tool dictionary

## License

MIT License

Copyright (c) 2025 Wei Zhou

## Contributing

Individual Contributor: Wei Zhou

We welcome contributions! Please review our contribution guidelines for details on our code of conduct, and the process for submitting pull requests.
