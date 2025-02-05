import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .agent.customer_service import CustomerServiceAgent, CustomerContext
from .agent.agent_config import AgentConfig

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = FastAPI(title="Customer Service API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent
context = CustomerContext(
    use_case="support",
    knowledge_base={
        "faqs": {
            "return": "Our return policy allows returns within 30 days of purchase.",
            "shipping": "We ship worldwide with delivery times of 3-5 business days.",
        },
        "policies": {
            "privacy": "We protect your data and never share it with third parties.",
            "terms": "Our terms of service ensure fair usage of our platform."
        },
        "products": {
            "electronics": "We offer a wide range of electronic products.",
            "clothing": "Our clothing line includes sizes XS to XXL."
        }
    }
)

agent_config = AgentConfig.default_config()
# agent_config = AgentConfig(
#     model_name="deepseek/deepseek-v3",
#     temperature=0,
# )
agent = CustomerServiceAgent(context, agent_config)

class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        response = await agent.handle_message(chat_message.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream(chat_message: ChatMessage):
    try:
        async def generate():
            async for chunk in agent.handle_message_stream(chat_message.message):
                yield f"data: {chunk}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 