# pychatbot2

A Python SDK for the chatbot platform, providing a clean and type-safe interface for interacting with messaging platforms.

## Features

- Type-safe interfaces using Python's type hints
- Async/await support for all operations
- Event-driven architecture using Server-Sent Events (SSE)
- Support for various message content types (text, image, audio, card)
- Comprehensive error handling and logging
- Easy integration with messaging platforms

## Installation

```bash
pip install pychatbot2
```

## Quick Start

```python
from pychatbot2 import ChatbotClient, ChatbotClientOptions, CommandRunner, Contact, ContactType, ChatMessagePayload, ChatMessagePlainContent

class MyCommandRunner(CommandRunner):
    async def on_start(self, payload):
        return {
            "self": Contact(
                contact_type=ContactType.PRIVATE,
                contact_id="user123",
                name="My Bot"
            ),
            "contacts": []
        }
    
    async def get_self(self, payload):
        return Contact(
            contact_type=ContactType.PRIVATE,
            contact_id="user123",
            name="My Bot"
        )
    
    async def get_contacts(self, payload):
        return []
    
    async def get_contact_info(self, payload):
        return {
            "name": "Test Contact",
            "members": []
        }
    
    async def send_chat_message(self, payload):
        # Implement message sending logic
        pass

# Create client options
options = ChatbotClientOptions(
    base_url="https://api.example.com",
    api_key="your-api-key",
    message_platform_type="custom",
    message_platform_account_id="account123",
    command_runner=MyCommandRunner()
)

# Create and start the client
client = ChatbotClient(options)
await client.start()

# Handle incoming messages
async def handle_message(message):
    payload = ChatMessagePayload(
        contact_type=ContactType.PRIVATE,
        contact_id="user123",
        message_id="msg123",
        sender_id="sender123",
        content=ChatMessagePlainContent(text="Hello!"),
        mentioned=False
    )
    await client.on_receive_chat_message(payload)
```

## Development

### Setup

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Running Tests

```bash
pytest
```

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- mypy for type checking

Run the formatters:
```bash
black .
isort .
```

## License

MIT License 