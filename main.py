from fastapi import FastAPI, Security, HTTPException, Request
from fastapi.security.api_key import APIKeyHeader
from datetime import datetime

app = FastAPI(title="Agentic HoneyPot API")

API_KEY_NAME = "x-api-key"
FAKE_API_KEY = "secret123"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

@app.get("/honeypot")
async def honeypot(
    request: Request,
    api_key: str = Security(api_key_header)
):
    attacker_ip = request.client.host
    time = datetime.utcnow().isoformat()

    if api_key != FAKE_API_KEY:
        print(f"[ALERT] Unauthorized access from {attacker_ip} at {time}")
        raise HTTPException(status_code=401, detail="Unauthorized access detected")

    return {
        "status": "ok",
        "message": "Honeypot endpoint reached",
        "timestamp": time
    }
