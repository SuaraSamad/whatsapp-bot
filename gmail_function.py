import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from agents import function_tool

load_dotenv(override=True)

# Load these globally so they are available to the function
MY_EMAIL = os.getenv("EMAIL")
MY_APP_PASSWORD = os.getenv("EMAIL_PASSWORD")

@function_tool
def send_gmail(recipient_email: str, subject: str, body: str):
    """
    Sends a simple plain-text email via Gmail's SMTP server.
    
    Args:
        recipient_email: The email address of the receiver.
        subject: The subject line of the email.
        body: The main text content of the email.
    """
    # Use the credentials loaded from the .env file
    if not MY_EMAIL or not MY_APP_PASSWORD:
        return "Failure: Email credentials not found in environment variables."

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = MY_EMAIL
    msg['To'] = recipient_email
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(MY_EMAIL, MY_APP_PASSWORD)
            smtp.send_message(msg)
        return "Success: Email sent!"
    except Exception as e:
        return f"Failure: {e}"

# send_gmail("gallerybysamad@gmail.com", "test", "Testing 1234567890")