import asyncio
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_streaming():
    async with httpx.AsyncClient() as client:
        message = "I want to return a product I bought last week"
        
        try:
            # Test streaming endpoint
            logger.info(f"Sending message: {message}")
            async with client.stream(
                'POST', 
                'http://localhost:8000/chat/stream',
                json={"message": message},
                timeout=30.0
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith('data: '):
                        chunk = line[6:]  # Remove 'data: ' prefix
                        print(chunk, end='', flush=True)
                print()  # New line after complete response
                
        except Exception as e:
            logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_streaming()) 