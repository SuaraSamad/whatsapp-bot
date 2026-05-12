import httpx
import os
import json
from agents import function_tool

@function_tool
async def google_search(query: str):
    """
    Search Google for real-time information, news, and facts.
    Use this when the user asks about current events or specific details 
    about companies, people, or stock prices.
    """
    url = "https://google.serper.dev/search"
    api_key = os.getenv("SERPER_API_KEY")
    
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json={"q": query})
        if response.status_code == 200:
            data = response.json()
            # Extract snippets so the AI can read them easily
            snippets = [item.get("snippet", "") for item in data.get("organic", [])[:3]]
            return "\n".join(snippets)
        return f"Search failed with status: {response.status_code}"