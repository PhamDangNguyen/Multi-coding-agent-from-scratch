import asyncio
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]  
sys.path.append(str(ROOT))
from llm import GeminiClient, OpenAIClient
import os, asyncio
from schemas.llm.llm_message import BaseMessage
from rich import print
from prompts import load_prompt
from dotenv import load_dotenv
load_dotenv()
gemini_prompt = load_prompt("llm_systems/gemini.md")
openai_prompt = load_prompt("llm_systems/openai.md")
async def test_gemini_client():
    """Test GeminiClient, check init + infer capability"""
    gemini_api_key = os.getenv("GEMINI_API")
    gemini_model = os.getenv("GEMINI_MODEL")
    client = GeminiClient(api_key=gemini_api_key, model=gemini_model)
    messages = [
        BaseMessage(role="system", content=gemini_prompt),
        BaseMessage(role="user", content="What is the capital of France?")
    ]
    response = await client.generate(messages)
    print(f"Gemini response: {response}")
    return response

async def test_gemini_client_stream():
    """Test GeminiClient streaming capability"""
    gemini_api_key = os.getenv("GEMINI_API")
    gemini_model = os.getenv("GEMINI_MODEL")
    client = GeminiClient(api_key=gemini_api_key, model=gemini_model)
    messages = [
        BaseMessage(role="system", content=gemini_prompt),
        BaseMessage(role="user", content="tell me a short story 3 sentence about the black dog")
    ]
    async for chunk in client.stream_generate(messages):
        print(f"Gemini stream chunk: {chunk}")

async def test_openai_client():
    """Test OpenAIClient, check init + infer capability"""
    openai_api_key = os.getenv("OPENAI_API")
    openai_model = os.getenv("OPENAI_MODEL")
    client = OpenAIClient(api_key=openai_api_key, model=openai_model)
    messages = [
        BaseMessage(role="system", content=openai_prompt),
        BaseMessage(role="user", content="What is the capital of France?")
    ]
    response = await client.generate(messages)
    print(f"OpenAI response: {response}")
    return response

async def test_openai_client_stream():
    """Test OpenAIClient streaming capability"""
    openai_api_key = os.getenv("OPENAI_API")
    openai_model = os.getenv("OPENAI_MODEL")
    client = OpenAIClient(api_key=openai_api_key, model=openai_model)
    messages = [
        BaseMessage(role="system", content=openai_prompt),
        BaseMessage(role="user", content="tell me a short story 3 sentence about the black dog")
    ]
    async for chunk in client.stream_generate(messages):
        print(f"OpenAI stream chunk: {chunk}")

if __name__ == "__main__":
    print("Testing OpenAIClient...")
    asyncio.run(test_openai_client())