from fastapi import FastAPI, Security, HTTPException, Request
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Agentic Honey-Pot for Scam Detection")

API_KEY_NAME = "x-api-key"
FAKE_API_KEY = "secret123"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# ---------- Request Schema ----------
class Message(BaseModel):
    sender: str
    text: str
    timestamp: int

class HoneypotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: list
    metadata: dict

# ---------- Endpoint ----------
@app.post("/honeypot")
async def honeypot(
    payload: HoneypotRequest,
    request: Request,
    api_key: str = Security(api_key_header)
):
    if api_key != FAKE_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized access detected")

    attacker_ip = request.client.host
    time = datetime.utcnow().isoformat()

    # Log scam attempt (intelligence extraction)
    print(f"[HONEYPOT] {time} | IP: {attacker_ip}")
    print(f"Scam message: {payload.message.text}")

    # Decoy reply to keep scammer engaged
    reply_text = "Why is my account being suspended?"

    return {
        "status": "success",
        "reply": reply_text
    }
