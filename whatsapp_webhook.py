from fastapi import FastAPI, Request, BackgroundTasks # 1. Import BackgroundTasks
from whatsapp_client import send_message
from chatbot import get_response
import os

app = FastAPI()

VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "my_secret_token")

@app.get("/")
def root():
    return {"status": "WhatsApp AI Chatbot is running"}

@app.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params.get("hub.challenge"))
    return {"error": "Invalid token"}

# 2. Create a helper function to handle the long-running AI logic
async def handle_agent_logic(sender: str, text: str):
    try:
        # Get response from AI agent
        response = await get_response(text)
        print(f"Agent response: {response}")

        # Send response back via WhatsApp
        await send_message(sender, response)
    except Exception as e:
        print(f"Error in background task: {e}")

@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks): # 3. Inject background_tasks
    data = await request.json()
    print("Incoming webhook:", data)

    try:
        changes = data["entry"][0]["changes"][0]["value"]

        # If it's a status update (delivered/read), ignore it early
        if "messages" not in changes:
            return {"status": "ok"}

        msg = changes["messages"][0]
        if msg.get("type") != "text":
            return {"status": "ok"}

        sender = msg["from"]
        text = msg["text"]["body"]
        print(f"Message from {sender}: {text}")

        # 4. Hand off the AI work to the background
        background_tasks.add_task(handle_agent_logic, sender, text)

    except (KeyError, IndexError) as e:
        print(f"Error parsing webhook: {e}")

    # 5. Return IMMEDIATELY. WhatsApp is now happy.
    return {"status": "ok"}