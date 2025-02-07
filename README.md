# Customer Service Agent Example

This is an example of a customer service agent built using crewAI. The agent leverages AI to handle customer inquiries and support requests in a natural and helpful way, demonstrating the power of reactive agents in customer service scenarios.

## Overview

This example showcases how to:
- Create an intelligent customer service agent that understands and responds to customer queries
- Handle common customer service scenarios like product returns, complaints, and general inquiries
- Implement reactive agent behavior for real-time customer interactions
- Integrate with FastAPI for a production-ready REST API

## Features

- Natural language understanding and generation
- Context-aware responses based on customer history
- Configurable knowledge base for FAQs and policies
- Real-time streaming responses
- REST API endpoints for chat integration

## Requirements

- Python 3.8+
- crewAI library (>=0.11.0)
- FastAPI
- uvicorn
- Other dependencies listed in requirements.txt

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/joaomdmoura/crewAI.git
   cd crewAI/examples/CustomerServiceAgent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the src directory with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

1. Start the API server:
   ```bash
   uvicorn src.api:app --reload
   ```

2. Send requests to the API:
   ```bash
   # Chat endpoint
   curl -X POST "http://localhost:8000/chat" \
        -H "Content-Type: application/json" \
        -d '{"message": "What is your return policy?"}'

   # Streaming chat endpoint
   curl -X POST "http://localhost:8000/chat/stream" \
        -H "Content-Type: application/json" \
        -d '{"message": "Tell me about shipping"}'
   ```

## Customization

You can customize the agent's behavior by:
1. Modifying the knowledge base in `src/api.py`
2. Adjusting agent configuration in `src/agent/agent_config.py`
3. Extending agent capabilities in `src/agent/customer_service.py`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.