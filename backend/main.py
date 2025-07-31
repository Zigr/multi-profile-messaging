import os
from fastapi import FastAPI, HTTPException
from routers import profile, template, list_manager, logs
from pydantic import BaseModel
from connectors.smtp_connector import SMTPConnector
from connectors.playwright_auth import PlaywrightAuth
from dotenv import load_dotenv

load_dotenv()  # loads .env into os.environ

app = FastAPI(title="Multi-Profile Messaging")

# Initialize SMTP connector from env
smtp = SMTPConnector(
    host=os.getenv("SMTP_HOST", "default_smtp_host"),
    port=int(os.getenv("SMTP_PORT", 587)),
    user=os.getenv("SMTP_USER"),
    password=os.getenv("SMTP_PASSWORD"),
    use_ssl=os.getenv("USE_MAILCATCHER", "false").lower() != "true",
    use_mailcatcher=os.getenv("USE_MAILCATCHER", "false").lower() == "true",
)

# Initialize Playwright auth helper
play_auth = PlaywrightAuth(headless=False)


class EmailRequest(BaseModel):
    to_address: str
    subject: str
    body: str


@app.post("/api/test-email")
def test_email(req: EmailRequest):
    try:
        smtp.send_email(req.to_address, req.subject, req.body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email send failed: {e}")
    return {"status": "sent"}


class AuthRequest(BaseModel):
    login_url: str


@app.post("/api/telegram/login")
def telegram_login(req: AuthRequest):
    """
    Launches a browser for the user to log into Telegram’s web interface
    and returns the cookies JSON.
    """
    try:
        cookies_json = play_auth.login(req.login_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Playwright auth failed: {e}")
    return {"cookies": cookies_json}

# existing endpoints...
app.include_router(profile.router)
app.include_router(template.router)
app.include_router(list_manager.router)
app.include_router(logs.router)