import httpx 
from dotenv import load_dotenv
import os
import asyncio
from fastapi import FastAPI, Request

load_dotenv(override=True)

WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
BASE_URL = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_NUMBER_ID}"

app = FastAPI()

async def send_message(phone_number: str, message: str):
    url = f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {os.getenv('WHATSAPP_TOKEN')}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {
            "body": message
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        return response.json()

VERIFY_TOKEN = "my_secret_token"

@app.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params.get("hub.challenge"))
    return {"error": "Invalid token"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("Incoming message:",data)
    if "messages" in data["entry"][0]["changes"][0]["value"]:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = msg["from"]
        text = msg["text"]["body"]

        
        # Call chatbot logic here, for now just echo back
        await send_message(sender, f"You said: {text}")

    return {"status": "received"}




if __name__ == "__main__":
    response = asyncio.run(send_message("+2349077253495", "Hello from WhatsApp Cloud API!"))
    print(response)




    # data = {
    #     "messaging_product": "whatsapp",
    #     "to": phone_number,
    #     "type": "text",