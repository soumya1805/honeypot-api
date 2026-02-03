import os
from fastapi import FastAPI, Header, HTTPException, Body
from typing import Any, Dict, Optional

app = FastAPI()

API_KEY = os.getenv("API_KEY", "gunnu123")

@app.get("/")
def home():
    return {"message": "Honeypot API is live ✅"}

@app.post("/honeypot")
async def honeypot(
    payload: Optional[Any] = Body(default=None),   # ✅ accept ANY kind of body
    x_api_key: Optional[str] = Header(None)
):
    # ✅ API key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # ✅ if body empty, keep safe
    if payload is None:
        payload = {}

    return {
        "status": "ok",
        "scam_detected": False,
        "agent_active": False,
        "reply": "Honeypot working ✅",
        "received": payload
    }
