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

# import os
# import re
# from fastapi import FastAPI, Header, HTTPException, Body
# from typing import Any, Dict, Optional

# app = FastAPI()

# API_KEY = os.getenv("API_KEY", "gunnu123")

# # ✅ In-memory storage (simple memory)
# MEMORY: Dict[str, Dict[str, Any]] = {}

# # ✅ Regex Extractors
# UPI_REGEX = r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b"
# BANK_REGEX = r"\b\d{9,18}\b"
# URL_REGEX = r"(https?://\S+|www\.\S+)"

# def detect_scam(message: str) -> bool:
#     msg = message.lower()
#     scam_keywords = [
#         "urgent", "account blocked", "otp", "kyc", "verify",
#         "click", "link", "password", "reward", "won", "lottery",
#         "upi", "bank", "sbi", "refund", "offer"
#     ]
#     return any(k in msg for k in scam_keywords)

# def extract_intelligence(text: str) -> Dict[str, list]:
#     upis = re.findall(UPI_REGEX, text)
#     banks = re.findall(BANK_REGEX, text)
#     urls = re.findall(URL_REGEX, text)

#     # remove duplicates
#     return {
#         "upi_ids": list(set(upis)),
#         "bank_accounts": list(set(banks)),
#         "phishing_links": list(set(urls)),
#     }

# def agent_reply(message: str, memory: Dict[str, Any]) -> str:
#     """
#     Smart but innocent replies.
#     Goal: keep scammer engaged + get UPI/bank/link.
#     """
#     turns = memory.get("turns", 0)

#     # first time replies
#     if turns == 0:
#         return (
#             "Oh no 😥 seriously? My account will get blocked? "
#             "Please tell me what I should do now. "
#             "Can you send the official link again?"
#         )

#     # Ask for link repeatedly (good for phishing link extraction)
#     if "link" in message.lower() or turns == 1:
#         return (
#             "I clicked but it is not opening properly 😭 "
#             "Can you resend the link? Also what is the exact process step by step?"
#         )

#     # Ask for UPI ID (good for extraction)
#     if turns == 2:
#         return (
#             "It’s asking payment/verification… 😟 "
#             "Can you share your UPI ID once? I’ll try from my mom’s phone."
#         )

#     # Ask for bank details
#     if turns == 3:
#         return (
#             "UPI is failing again… maybe bank transfer will work. "
#             "Send account number + IFSC please, I will do it quickly 🙏"
#         )

#     # Keep them engaged longer
#     return (
#         "Wait I’m trying… it is loading slow 😭 "
#         "Just confirm once, this is safe right? "
#         "Also send the link/UPI details again, I’ll copy paste properly."
#     )

# @app.get("/")
# def home():
#     return {"message": "Agentic Honeypot API is live ✅"}

# @app.post("/honeypot")
# async def honeypot(
#     payload: Optional[Any] = Body(default=None),
#     x_api_key: Optional[str] = Header(None)
# ):
#     if x_api_key != API_KEY:
#         raise HTTPException(status_code=401, detail="Invalid API key")

#     if payload is None:
#         payload = {}

#     # ✅ Extract message + conversation_id safely
#     message = ""
#     conversation_id = "default"

#     if isinstance(payload, dict):
#         message = str(payload.get("message", ""))
#         conversation_id = str(payload.get("conversation_id", "default"))

#     if conversation_id not in MEMORY:
#         MEMORY[conversation_id] = {
#             "turns": 0,
#             "full_text": "",
#             "scam_detected": False,
#             "intel": {"upi_ids": [], "bank_accounts": [], "phishing_links": []}
#         }

#     conv = MEMORY[conversation_id]

#     # add message to memory text
#     conv["full_text"] += f"\nSCAMMER: {message}\n"

#     # detect scam
#     scam_flag = conv["scam_detected"] or detect_scam(message)
#     conv["scam_detected"] = scam_flag

#     # extract intelligence from entire conversation
#     new_intel = extract_intelligence(conv["full_text"])
#     conv["intel"]["upi_ids"] = list(set(conv["intel"]["upi_ids"] + new_intel["upi_ids"]))
#     conv["intel"]["bank_accounts"] = list(set(conv["intel"]["bank_accounts"] + new_intel["bank_accounts"]))
#     conv["intel"]["phishing_links"] = list(set(conv["intel"]["phishing_links"] + new_intel["phishing_links"]))

#     # decide reply
#     reply = "Hello! How can I help you?"
#     agent_active = False

#     if scam_flag:
#         agent_active = True
#         reply = agent_reply(message, conv)
#     else:
#         reply = "Okay 👍"

#     conv["turns"] += 1
#     conv["full_text"] += f"HONEYPOT: {reply}\n"

#     return {
#         "status": "ok",
#         "conversation_id": conversation_id,
#         "scam_detected": scam_flag,
#         "agent_active": agent_active,
#         "turns": conv["turns"],
#         "reply": reply,
#         "extracted_intelligence": conv["intel"]
#     }

import os
import re
from fastapi import FastAPI, Header, HTTPException, Body
from typing import Any, Dict, Optional, List

app = FastAPI()
API_KEY = os.getenv("API_KEY", "gunnu123")

# -----------------------------
# MEMORY (per conversation)
# -----------------------------
MEMORY: Dict[str, Dict[str, Any]] = {}

# -----------------------------
# REGEX EXTRACTORS (strong)
# -----------------------------
UPI_REGEX = r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b"
BANK_REGEX = r"\b\d{9,18}\b"
IFSC_REGEX = r"\b[A-Z]{4}0[A-Z0-9]{6}\b"
URL_REGEX = r"(https?://[^\s]+|www\.[^\s]+)"
PHONE_REGEX = r"\b[6-9]\d{9}\b"
EMAIL_REGEX = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"

SCAM_KEYWORDS = [
    "urgent", "account", "blocked", "otp", "kyc", "verify",
    "click", "link", "password", "reward", "won", "lottery",
    "upi", "refund", "offer", "compromised", "sbi", "bank"
]

def normalize_list(items: List[str]) -> List[str]:
    return sorted(list(set([i.strip() for i in items if i and i.strip()])))

def detect_scam(message: str) -> float:
    """Return scam score 0 to 1"""
    msg = (message or "").lower()
    hits = sum(1 for k in SCAM_KEYWORDS if k in msg)
    score = min(1.0, hits / 3)  # 3 hits = 1.0
    return score

def extract_all(text: str) -> Dict[str, List[str]]:
    return {
        "upi_ids": normalize_list(re.findall(UPI_REGEX, text)),
        "bank_accounts": normalize_list(re.findall(BANK_REGEX, text)),
        "ifsc_codes": normalize_list(re.findall(IFSC_REGEX, text)),
        "phishing_links": normalize_list(re.findall(URL_REGEX, text)),
        "phone_numbers": normalize_list(re.findall(PHONE_REGEX, text)),
        "emails": normalize_list(re.findall(EMAIL_REGEX, text)),
    }

def get_goal(intel: Dict[str, List[str]]) -> str:
    """Decide next best target based on missing intelligence."""
    if len(intel["phishing_links"]) == 0:
        return "GET_LINK"
    if len(intel["upi_ids"]) == 0:
        return "GET_UPI"
    if len(intel["bank_accounts"]) == 0:
        return "GET_BANK"
    if len(intel["ifsc_codes"]) == 0:
        return "GET_IFSC"
    if len(intel["phone_numbers"]) == 0:
        return "GET_PHONE"
    return "STALL_MORE"

def agent_reply(goal: str, turns: int) -> str:
    """High-engagement believable replies based on goal."""
    if goal == "GET_LINK":
        return (
            "Oh no 😥 my SBI account will be blocked?? I’m really scared. "
            "I tried opening it but it’s not loading on my phone 😭 "
            "Can you send the official link again? (full link please)"
        )

    if goal == "GET_UPI":
        return (
            "Okay I got the page now… it is asking for verification/payment 😟 "
            "I will do it fast. Can you send your UPI ID once? "
            "I’ll copy paste carefully."
        )

    if goal == "GET_BANK":
        return (
            "UPI is failing again 😭 maybe due to limit. "
            "Can you share bank account number + beneficiary name? "
            "I’ll try bank transfer quickly."
        )

    if goal == "GET_IFSC":
        return (
            "I entered account number, now it’s asking IFSC code. "
            "Please send IFSC also 🙏"
        )

    if goal == "GET_PHONE":
        return (
            "The link is asking customer care contact. "
            "Can you share your support number? I’ll call once to confirm 😥"
        )

    # STALL MORE = keep them engaged
    if turns % 2 == 0:
        return (
            "Wait wait 😭 the page is stuck again… "
            "Just confirm this is 100% safe right? "
            "Send the details once again, I’ll try from my mom’s phone now."
        )
    else:
        return (
            "Sorry sorry 🙏 my network is slow. "
            "Please resend the link/UPI details clearly. I don’t want mistake."
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

    # parse safely
    message = ""
    conversation_id = "default"

    if isinstance(payload, dict):
        message = str(payload.get("message", ""))
        conversation_id = str(payload.get("conversation_id", "default"))

    # init conversation memory
    if conversation_id not in MEMORY:
        MEMORY[conversation_id] = {
            "turns": 0,
            "full_text": "",
            "scam_detected": False,
            "scam_score": 0.0,
            "intel": {
                "upi_ids": [],
                "bank_accounts": [],
                "ifsc_codes": [],
                "phishing_links": [],
                "phone_numbers": [],
                "emails": []
            }
        }

    conv = MEMORY[conversation_id]

    # update text
    conv["full_text"] += f"\nSCAMMER: {message}\n"

    # scam detection score
    score = detect_scam(message)
    conv["scam_score"] = max(conv["scam_score"], score)

    # detect scam if score high enough
    if conv["scam_score"] >= 0.5:
        conv["scam_detected"] = True

    # extract intelligence from conversation text
    extracted = extract_all(conv["full_text"])
    for k in conv["intel"]:
        conv["intel"][k] = normalize_list(conv["intel"][k] + extracted.get(k, []))

    # decide behavior
    agent_active = conv["scam_detected"]
    turns = conv["turns"]
    goal = get_goal(conv["intel"])

    if agent_active:
        reply = agent_reply(goal, turns)
    else:
        reply = "Okay 👍"

    conv["turns"] += 1
    conv["full_text"] += f"HONEYPOT: {reply}\n"

    return {
        "status": "ok",
        "conversation_id": conversation_id,
        "scam_detected": conv["scam_detected"],
        "scam_score": round(conv["scam_score"], 2),
        "agent_active": agent_active,
        "turns": conv["turns"],
        "current_goal": goal,
        "reply": reply,
        "extracted_intelligence": conv["intel"]
    }

