from typing import Dict, List, Optional, AsyncGenerator
from datetime import datetime
import asyncio
import os
import time
from crewai import Agent, Task
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_openai.chat_models.base import BaseChatOpenAI

# Load environment variables
from .agent_config import AgentConfig
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class SentimentResponse(TypedDict):
    sentiment: str
    confidence: float
    message: str

class IntentResponse(TypedDict):
    intent: str
    confidence: float
    message: str

class CustomerServiceResponse(BaseModel):
    response: str | None = None
    sentiment: str | None = None
    intent: str | None = None

class CustomerServiceOutput(BaseModel):
    """Output format for Customer Serivice task."""
    response: str = Field(
        ...,
        description="Response to customer query",
    )
    intent: str = Field(
        ...,
        description="Intention of customer query, be specific",
    )
    sentiment: str = Field(
        ...,
        description="Sentiment of customer query",
    )

class CustomerContext(BaseModel):
    """Context for customer interaction"""
    use_case: str  # e.g., "support", "sales", "therapy"
    customer_history: Optional[List[Dict]] = []
    knowledge_base: Optional[Dict] = {}
    tone_preferences: Optional[Dict] = {
        "support": "professional and helpful",
        "sales": "enthusiastic and persuasive",
        "therapy": "empathetic and understanding"
    }

class CustomerServiceAgent:
    """A customer service agent that uses LLM to analyze sentiment, understand intent, and provide contextual responses."""
    
    def __init__(self, context: CustomerContext, agent_config: AgentConfig):
        self.context = context
        self.agent = self._create_agent(agent_config)

    def _create_agent(self, agent_config: AgentConfig) -> Agent:
        model_name = agent_config.model_name
        # create llm from model_name
        if model_name not in [
            "gpt-4o-mini", "gpt-4o-mini-2024-01-18", 
            "gpt-4o-mini-2024-02-04", "gpt-o1"]:
            llm = BaseChatOpenAI(
                model=model_name,
                temperature=agent_config.temperature,
                openai_api_key=agent_config.api_key,
                openai_api_base=agent_config.api_base
                
            )
        else:
            llm = ChatOpenAI(model_name=model_name, temperature=agent_config.temperature)
 
        return Agent(
            name="Customer Service Agent",
            role="Customer Service Specialist",
            goal="""As an empathetic customer service agent, I will:
            1. Carefully analyze each customer message to understand their true emotions,
               needs and intentions through tone, word choice and context
            2. Identify the key issues or questions they are trying to communicate
            3. Provide clear, helpful responses that directly address their needs while
               matching their emotional state
            4. Maintain a supportive and understanding tone throughout the conversation
            5. Verify that their concerns have been fully resolved
            6. Learn from each interaction to better serve future customers""",
            backstory=f"""You are an expert {self.context.use_case} specialist with years of 
            experience in customer psychology and communication. You excel at reading between
            the lines to understand customers' true needs and emotions. You know how to adapt
            your communication style to make customers feel heard and supported while efficiently
            resolving their issues.""",
            tools=[
                StructuredTool.from_function(
                    func=self._query_knowledge_base,
                    name="query_knowledge_base",
                    description="Query knowledge base for relevant information",
                    return_direct=False
                ),
                # StructuredTool.from_function(
                #     func=self._analyze_sentiment_intent,
                #     name="analyze_sentiment_intent",
                #     description="Analyze the customer's emotional state and intentions",
                #     return_direct=False
                # )
            ],
            llm = llm,
            verbose=True
        )

    @tool("Analyze sentiment and intent")
    def _analyze_sentiment_intent(self, sentiment:str, intent:str, message: str) -> Dict:
        """Analyze the sentiment of a customer message using LLM function calling"""
        return {
            "sentiment": sentiment,  # Could be frustrated, angry, happy, or neutral
            "intent": intent,    # Could be question, complaint, request, or feedback
            "message": message
        }

    def _analyze_intent(self, message: str) -> IntentResponse:
        """Classify the intent of a customer message using LLM function calling"""
        # The LLM will determine these values through function calling
        return {
            "intent": "question",
            "confidence": 0.8,
            "message": message
        }

    def _query_knowledge_base(self, query: str) -> Dict:
        """Query the knowledge base for relevant information"""
        results = {}
        for category, content in self.context.knowledge_base.items():
            if any(keyword in query.lower() for keyword in content.keys()):
                results[category] = content
        
        return {
            "query": query,
            "results": results
        }

    async def handle_message(self, message: str) -> str:
        """Handle incoming customer message"""
        self.context.customer_history.append({
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        task = Task(
            description=f"""
            Analyze and respond to this customer message: "{message}"
            
            Steps:
            1. Analyze customer sentiment and emotional state:
               - Identify positive/negative/neutral tone
               - Detect urgency level
               - Note any strong emotions (frustration, satisfaction, etc.)
            
            2. Determine customer intent and needs:
               - Classify primary purpose (question, complaint, request, etc.)
               - Identify specific topics/products mentioned
               - Note any implicit needs or concerns
            
            3. Search knowledge base for relevant information:
               - Find matching FAQs and policies
               - Gather product/service details
               - Check for special cases or exceptions
            
            4. Craft a personalized response that:
               - Directly addresses their primary concern first
               - Uses empathetic language matching their emotional state
               - Maintains professional tone appropriate for {self.context.use_case}
               - Incorporates relevant knowledge base information naturally
               - Offers clear next steps or solutions
               - Ends with appropriate reassurance or call-to-action
            
            Current use case: {self.context.use_case}
            Preferred tone: {self.context.tone_preferences[self.context.use_case]}
            Response guidelines:
            - Be concise but thorough
            - Use positive, solution-focused language
            - Show understanding before providing solutions
            - Include specific details from knowledge base
            """,
            expected_output="A detailed response to the customer message, sentiment and customer intention",
            # output_json = CustomerServiceResponse(),
            output_pydantic=CustomerServiceOutput,
            agent=self.agent
        )
        # Execute task and get result
        start_time = time.time()
        result = self.agent.execute_task(task)  # Remove await here
        end_time = time.time()
        print(f"Task execution took {end_time - start_time:.2f} seconds")
        # result["total_latency"] = end_time - start_time
        return result
