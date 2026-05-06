import asyncio
from pathlib import Path
import sys
from urllib import response
ROOT = Path(__file__).resolve().parents[2]  
sys.path.append(str(ROOT))
from llm import GeminiClientLangChain, OpenAIClientLangChain
import os, asyncio
from schemas.llm.llm_message import BaseMessage
from rich import print
from prompts import load_prompt
from dotenv import load_dotenv
load_dotenv()
gemini_prompt = load_prompt("llm_systems/gemini.md")
openai_prompt = load_prompt("llm_systems/openai.md")
async def test_langchain_gemini_client():
    """Test GeminiClientLangChain, check init + infer capability"""
    gemini_api_key = os.getenv("GEMINI_API")
    gemini_model = os.getenv("GEMINI_MODEL")
    client = GeminiClientLangChain(api_key=gemini_api_key, model=gemini_model, max_retries=3)
    messages = [
        BaseMessage(role="system", content=gemini_prompt),
        BaseMessage(role="user", content="tell me short story about the dog in 50 words")
    ]
    # response = await client.generate(messages)
    # print(f"Gemini response: {response}")
    async for chunk in client.stream_generate(messages):
        print(f"Gemini stream chunk: {chunk}")
    return response

async def test_langchain_openai_client():
    """Test OpenAIClientLangChain, check init + infer capability"""
    openai_api_key = os.getenv("OPENAI_API")
    openai_model = os.getenv("OPENAI_MODEL")
    client = OpenAIClientLangChain(api_key=openai_api_key, model=openai_model, max_retries=3)
    messages = [
        BaseMessage(role="system", content=openai_prompt),
        BaseMessage(role="user", content="tell me short story about the dog in 50 words")
    ]
    response = await client.generate(messages)
    print(f"OpenAI response: {response}")
    # async for chunk in client.stream_generate(messages):
    #     print(f"OpenAI stream chunk: {chunk}")
    return response

if __name__ == "__main__":
    print("Testing OpenAIClientLangChain...")
    asyncio.run(test_langchain_openai_client())
