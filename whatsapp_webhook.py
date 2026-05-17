from fastapi import FastAPI, Request, BackgroundTasks
from whatsapp_client import send_message
from chatbot import get_response
from database import init_db  # <--- NEW: Import your DB init
import os

app = FastAPI()

VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "my_secret_token")

# --- NEW: Initialize Database on Startup ---
@app.on_event("startup")
async def startup_event():
    print("Initializing Database...")
    init_db()

@app.get("/")
def root():
    return {"status": "WhatsApp AI Chatbot is running"}

@app.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params.get("hub.challenge"))
    return {"error": "Invalid token"}

async def handle_agent_logic(sender: str, text: str):
    try:
        # UPDATED: Now passing 'sender' to get_response for SQLite memory
        response = await get_response(sender, text) 
        print(f"Agent response for {sender}: {response}")

        await send_message(sender, response)
    except Exception as e:
        # This will catch your "Unknown tool type" error if it persists
        print(f"Error in background task for {sender}: {e}")

@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    
    try:
        changes = data["entry"][0]["changes"][0]["value"]

        if "messages" not in changes:
            return {"status": "ok"}

        msg = changes["messages"][0]
        if msg.get("type") != "text":
            return {"status": "ok"}

        sender = msg["from"]
        text = msg["text"]["body"]
        
        # Hand off the AI work with the sender's phone number
        background_tasks.add_task(handle_agent_logic, sender, text)

    except (KeyError, IndexError) as e:
        print(f"Error parsing webhook: {e}")

    return {"status": "ok"}