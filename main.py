# import os
# from fastapi import FastAPI, Header, HTTPException, Body
# from typing import Any, Dict, Optional

# app = FastAPI()

# API_KEY = os.getenv("API_KEY", "gunnu123")

# @app.get("/")
# def home():
#     return {"message": "Honeypot API is live ✅"}

# @app.post("/honeypot")
# async def honeypot(
#     payload: Optional[Any] = Body(default=None),   # ✅ accept ANY kind of body
#     x_api_key: Optional[str] = Header(None)
# ):
#     # ✅ API key check
#     if x_api_key != API_KEY:
#         raise HTTPException(status_code=401, detail="Invalid API key")

#     # ✅ if body empty, keep safe
#     if payload is None:
#         payload = {}

#     return {
#         "status": "ok",
#         "scam_detected": False,
#         "agent_active": False,
#         "reply": "Honeypot working ✅",
#         "received": payload
#     }
import os
import re
from fastapi import FastAPI, Header, HTTPException, Body
from typing import Any, Dict, Optional

app = FastAPI()

API_KEY = os.getenv("API_KEY", "gunnu123")

# ✅ In-memory storage (simple memory)
MEMORY: Dict[str, Dict[str, Any]] = {}

# ✅ Regex Extractors
UPI_REGEX = r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b"
BANK_REGEX = r"\b\d{9,18}\b"
URL_REGEX = r"(https?://\S+|www\.\S+)"

def detect_scam(message: str) -> bool:
    msg = message.lower()
    scam_keywords = [
        "urgent", "account blocked", "otp", "kyc", "verify",
        "click", "link", "password", "reward", "won", "lottery",
        "upi", "bank", "sbi", "refund", "offer"
    ]
    return any(k in msg for k in scam_keywords)

def extract_intelligence(text: str) -> Dict[str, list]:
    upis = re.findall(UPI_REGEX, text)
    banks = re.findall(BANK_REGEX, text)
    urls = re.findall(URL_REGEX, text)

    # remove duplicates
    return {
        "upi_ids": list(set(upis)),
        "bank_accounts": list(set(banks)),
        "phishing_links": list(set(urls)),
    }

def agent_reply(message: str, memory: Dict[str, Any]) -> str:
    """
    Smart but innocent replies.
    Goal: keep scammer engaged + get UPI/bank/link.
    """
    turns = memory.get("turns", 0)

    # first time replies
    if turns == 0:
        return (
            "Oh no 😥 seriously? My account will get blocked? "
            "Please tell me what I should do now. "
            "Can you send the official link again?"
        )

    # Ask for link repeatedly (good for phishing link extraction)
    if "link" in message.lower() or turns == 1:
        return (
            "I clicked but it is not opening properly 😭 "
            "Can you resend the link? Also what is the exact process step by step?"
        )

    # Ask for UPI ID (good for extraction)
    if turns == 2:
        return (
            "It’s asking payment/verification… 😟 "
            "Can you share your UPI ID once? I’ll try from my mom’s phone."
        )

    # Ask for bank details
    if turns == 3:
        return (
            "UPI is failing again… maybe bank transfer will work. "
            "Send account number + IFSC please, I will do it quickly 🙏"
        )

    # Keep them engaged longer
    return (
        "Wait I’m trying… it is loading slow 😭 "
        "Just confirm once, this is safe right? "
        "Also send the link/UPI details again, I’ll copy paste properly."
    )

@app.get("/")
def home():
    return {"message": "Agentic Honeypot API is live ✅"}

@app.post("/honeypot")
async def honeypot(
    payload: Optional[Any] = Body(default=None),
    x_api_key: Optional[str] = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if payload is None:
        payload = {}

    # ✅ Extract message + conversation_id safely
    message = ""
    conversation_id = "default"

    if isinstance(payload, dict):
        message = str(payload.get("message", ""))
        conversation_id = str(payload.get("conversation_id", "default"))

    if conversation_id not in MEMORY:
        MEMORY[conversation_id] = {
            "turns": 0,
            "full_text": "",
            "scam_detected": False,
            "intel": {"upi_ids": [], "bank_accounts": [], "phishing_links": []}
        }

    conv = MEMORY[conversation_id]

    # add message to memory text
    conv["full_text"] += f"\nSCAMMER: {message}\n"

    # detect scam
    scam_flag = conv["scam_detected"] or detect_scam(message)
    conv["scam_detected"] = scam_flag

    # extract intelligence from entire conversation
    new_intel = extract_intelligence(conv["full_text"])
    conv["intel"]["upi_ids"] = list(set(conv["intel"]["upi_ids"] + new_intel["upi_ids"]))
    conv["intel"]["bank_accounts"] = list(set(conv["intel"]["bank_accounts"] + new_intel["bank_accounts"]))
    conv["intel"]["phishing_links"] = list(set(conv["intel"]["phishing_links"] + new_intel["phishing_links"]))

    # decide reply
    reply = "Hello! How can I help you?"
    agent_active = False

    if scam_flag:
        agent_active = True
        reply = agent_reply(message, conv)
    else:
        reply = "Okay 👍"

    conv["turns"] += 1
    conv["full_text"] += f"HONEYPOT: {reply}\n"

    return {
        "status": "ok",
        "conversation_id": conversation_id,
        "scam_detected": scam_flag,
        "agent_active": agent_active,
        "turns": conv["turns"],
        "reply": reply,
        "extracted_intelligence": conv["intel"]
    }
