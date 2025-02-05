import asyncio
import logging
from src.agent.customer_service import CustomerServiceAgent, CustomerContext

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
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
    
    # Test single message
    message = "I want to return a product I bought last week"
    
    try:
        logger.info("Initializing agent...")
        agent = CustomerServiceAgent(context)
        
        logger.info(f"Processing message: {message}")
        response = await agent.handle_message(message)
        logger.info(f"Response: {response}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main()) 