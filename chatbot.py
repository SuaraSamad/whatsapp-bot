from agents import Agent, Runner, trace
from gmail_function import send_gmail
from serper_tool import google_search
from database import get_chat_history, save_chat_history

# Refined Persona: Focused on task execution and utility
instruction = """
You are a highly efficient personal AI Assistant. 
Your goal is to help the user manage tasks, find information, and handle communications.

CORE BEHAVIOR:
- Be direct, helpful, and organized.
- Keep responses concise and formatted for easy reading on WhatsApp.
- You HAVE a memory: always refer to the provided conversation history to maintain context.
- Never claim you cannot remember information; use the history to retrieve it.

CAPABILITIES:
1. Search: Use 'google_search' for real-time data, news, or facts.
2. Email: Use 'send_gmail' to send emails. Ask for missing details (to, subject, body) only if they aren't in the history.
"""

agent = Agent(
    name="Assistant",
    model="gpt-4o-mini",
    instructions=instruction,
    tools=[send_gmail, google_search] 
)

async def get_response(sender_id: str, user_message: str) -> str:
    """Handles logic for the AI Assistant persona with persistent memory."""
    
    # 1. Retrieve history
    history = get_chat_history(sender_id)
    
    # 2. Append new user message
    history.append({"role": "user", "content": user_message})

    with trace("WhatsApp Chatbot"):
        try:
            # 3. Execute with positional history
            result = await Runner.run(agent, history)
            
            response_text = result.final_output
            
            # 4. Update and Save history
            history.append({"role": "assistant", "content": response_text})
            save_chat_history(sender_id, history[-10:])
            
            return response_text
            
        except Exception as e:
            print(f"Assistant Error: {e}")
            return "I'm sorry, I ran into an issue. Please try again."