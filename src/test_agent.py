import asyncio
import logging
from agent.customer_service import CustomerServiceAgent, CustomerContext

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_agent():
    try:
        # Create test context
        context = CustomerContext(
            use_case="support",
            knowledge_base={
                "faqs": {
                    "return": "Our return policy allows returns within 30 days of purchase.",
                    "shipping": "We ship worldwide with delivery times of 3-5 business days.",
                }
            }
        )
        
        logger.info("Initializing CustomerServiceAgent...")
        agent = CustomerServiceAgent(context)
        
        # Test messages
        test_messages = [
            "I want to return a product I bought last week",
            "How long does shipping take?",
            "I'm very unhappy with my purchase!"
        ]
        
        for message in test_messages:
            try:
                logger.info(f"\nProcessing test message: {message}")
                response = await agent.handle_message(message)
                logger.info(f"Agent response: {response}")
            except Exception as e:
                logger.error(f"Error processing message '{message}': {str(e)}")
                
    except Exception as e:
        logger.error(f"Error in test_agent: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting agent test...")
    asyncio.run(test_agent()) 