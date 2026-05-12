from agents import Agent, Runner, trace
from gmail_function import send_gmail
from serper_tool import google_search # Import remains correct

instruction = """
You are a helpful advisor chatbot.
Respond to user messages with clear, supportive, and actionable advice.
Keep responses concise since they will be read on WhatsApp.

You have the ability to send emails and search the internet for real-time information.
- If a user asks to send an email, ask for the recipient's address, subject, and body if missing.
- Use the google_search tool for any factual questions, news, or topics you aren't certain about.
"""

agent = Agent(
    name="Advisor",
    model="gpt-4o-mini",
    instructions=instruction,
    # ADDED google_search to the tools list below
    tools=[send_gmail, google_search] 
)

async def get_response(user_message: str) -> str:
    """Pass a message to the agent and return its response."""
    # Note: If you still see [Errno 8] connection errors, 
    # try removing the 'with trace' block to simplify the network path.
    with trace("WhatsApp Chatbot"):
        result = await Runner.run(agent, user_message)
        return result.final_output