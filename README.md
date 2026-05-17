# WhatsApp AI Assistant 🤖

A personal AI assistant that runs directly inside WhatsApp. It can search the web, send emails, remember conversations, and reply to messages automatically.

## Features

- 🔍 Real-time web search via Serper
- 📧 Send emails via Gmail
- 🧠 Persistent memory across conversations (SQLite)
- 💬 Auto-reply to incoming WhatsApp messages
- 🔁 Manual / Automatic / Standby mode switching

## Tech Stack

- Python
- OpenAI Agents SDK
- WhatsApp Business API
- Serper API
- SQLite
- SMTP / Gmail

## Setup

1. Clone the repo
```bash
   git clone https://github.com/SuaraSamad/whatsapp-bot.git
   cd whatsapp-bot
```

2. Create and activate virtual environment
```bash
   uv venv
   source .venv/bin/activate
```

3. Install dependencies
```bash
   uv pip install -r requirements.txt
```

4. Create a `.env` file and add your keys
```
   OPENAI_API_KEY=your_openai_key
   SERPER_API_KEY=your_serper_key
   EMAIL=your_gmail
   EMAIL_PASSWORD=your_app_password
```

5. Run the bot
```bash
   uv run python main.py
```

## Project Structure

```
whatsapp-bot/
├── chatbot.py          # Core agent and persona
├── whatsapp_webhook.py # Webhook handler
├── whatsapp_client.py  # WhatsApp API client
├── serper_tool.py      # Web search tool
├── gmail_function.py   # Email tool
├── database.py         # SQLite memory
└── main.py             # Entry point
```

## Author

Abdulsamad Suara — [GitHub](https://github.com/SuaraSamad)
