"""
Example usage của Gemini và OpenAI LLM clients
"""
import asyncio
import os
from llm import GeminiClient, OpenAIClient, BaseMessage


async def example_gemini():
    """Example sử dụng Gemini Client"""
    api_key = os.getenv("GOOGLE_API_KEY")
    client = GeminiClient(api_key=api_key)
    
    messages = [
        BaseMessage(role="user", content="What is the capital of France?")
    ]
    
    # Generate response
    response = await client.generate(messages, temperature=0.7)
    print(f"Gemini: {response}")
    
    # Stream response
    print("Gemini (streaming):")
    async for chunk in client.stream_generate(messages):
        print(chunk, end="", flush=True)
    print()


async def example_openai():
    """Example sử dụng OpenAI Client"""
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAIClient(api_key=api_key, model="gpt-4o-mini")
    
    messages = [
        BaseMessage(role="user", content="What is the capital of France?")
    ]
    
    # Generate response
    response = await client.generate(messages, temperature=0.7)
    print(f"OpenAI: {response}")
    
    # Stream response
    print("OpenAI (streaming):")
    async for chunk in client.stream_generate(messages):
        print(chunk, end="", flush=True)
    print()


async def main():
    """Run examples"""
    print("=== Gemini Client ===")
    await example_gemini()
    
    print("\n=== OpenAI Client ===")
    await example_openai()


if __name__ == "__main__":
    asyncio.run(main())
