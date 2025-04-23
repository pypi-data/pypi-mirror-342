# AI Agent2Agent

A Python library for Agent-to-Agent communication.

## Installation

```bash
pip install ai_agent2agent
```

## Usage

### Client

```python
from agent2agent import A2AClient, A2ACardResolver

# Initialize client
client = A2AClient(url="https://your-agent-endpoint.com", api_key="your-api-key")

# Example: Send a task to an agent
response = client.send_task(
    message={
        "role": "user",
        "parts": [{"type": "text", "text": "Hello, Agent!"}]
    }
)

# Print the task ID
print(f"Task ID: {response.id}")
```

### Server

```python
from agent2agent import A2AServer, InMemoryTaskManager

# Initialize server with an in-memory task manager
task_manager = InMemoryTaskManager()
server = A2AServer(task_manager=task_manager)

# Register handler for tasks
@server.handle_task
async def handle_task(task):
    # Process the task
    return {
        "role": "agent",
        "parts": [{"type": "text", "text": "Task completed!"}]
    }

# Run the server (depends on your web framework)
```

## Features

- Client-server architecture for agent communication
- Support for various message types (text, files, data)
- Task management with different states
- In-memory caching
- Push notification support

## License

MIT 