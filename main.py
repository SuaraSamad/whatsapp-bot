from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool
import asyncio
from whatsapp_client import send_message

load_dotenv(override=True)

# Create the tool function

@function_tool
async def whatsapp_tool(phone_number: str, message: str):
    """
    Sends a WhatsApp message using Cloud API.
    """
    result = await send_message(phone_number, message)
    return result

instruction = """
You are a helpful financial advisor.
You are given a user's financial situation and you need to provide
a plan to improve their financial situation.
After generating the advice, send the advice using the WhatsApp tool
to the user's phone number +2349077253495.
"""

agent = Agent(
    name="Advisor",
    model="gpt-4o-mini",
    instructions=instruction,
    tools=[whatsapp_tool]
)

async def main():
    with trace("Give an advice"):
        result = await Runner.run(
            agent,
            "I have a lot of debt and I need to pay it off."
        )

        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
