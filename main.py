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


# import os
# import re
# from fastapi import FastAPI, Header, HTTPException, Body
# from typing import Any, Dict, Optional, List

# app = FastAPI()
# API_KEY = os.getenv("API_KEY", "gunnu123")

# # -----------------------------
# # MEMORY (per conversation)
# # -----------------------------
# MEMORY: Dict[str, Dict[str, Any]] = {}

# # -----------------------------
# # REGEX EXTRACTORS (strong)
# # -----------------------------
# UPI_REGEX = r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b"
# BANK_REGEX = r"\b\d{9,18}\b"
# IFSC_REGEX = r"\b[A-Z]{4}0[A-Z0-9]{6}\b"
# URL_REGEX = r"(https?://[^\s]+|www\.[^\s]+)"
# PHONE_REGEX = r"\b[6-9]\d{9}\b"
# EMAIL_REGEX = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"

# SCAM_KEYWORDS = [
#     "urgent", "account", "blocked", "otp", "kyc", "verify",
#     "click", "link", "password", "reward", "won", "lottery",
#     "upi", "refund", "offer", "compromised", "sbi", "bank"
# ]

# def normalize_list(items: List[str]) -> List[str]:
#     return sorted(list(set([i.strip() for i in items if i and i.strip()])))

# def detect_scam(message: str) -> float:
#     """Return scam score 0 to 1"""
#     msg = (message or "").lower()
#     hits = sum(1 for k in SCAM_KEYWORDS if k in msg)
#     score = min(1.0, hits / 3)  # 3 hits = 1.0
#     return score

# def extract_all(text: str) -> Dict[str, List[str]]:
#     return {
#         "upi_ids": normalize_list(re.findall(UPI_REGEX, text)),
#         "bank_accounts": normalize_list(re.findall(BANK_REGEX, text)),
#         "ifsc_codes": normalize_list(re.findall(IFSC_REGEX, text)),
#         "phishing_links": normalize_list(re.findall(URL_REGEX, text)),
#         "phone_numbers": normalize_list(re.findall(PHONE_REGEX, text)),
#         "emails": normalize_list(re.findall(EMAIL_REGEX, text)),
#     }

# def get_goal(intel: Dict[str, List[str]]) -> str:
#     """Decide next best target based on missing intelligence."""
#     if len(intel["phishing_links"]) == 0:
#         return "GET_LINK"
#     if len(intel["upi_ids"]) == 0:
#         return "GET_UPI"
#     if len(intel["bank_accounts"]) == 0:
#         return "GET_BANK"
#     if len(intel["ifsc_codes"]) == 0:
#         return "GET_IFSC"
#     if len(intel["phone_numbers"]) == 0:
#         return "GET_PHONE"
#     return "STALL_MORE"

# def agent_reply(goal: str, turns: int) -> str:
#     """High-engagement believable replies based on goal."""
#     if goal == "GET_LINK":
#         return (
#             "Oh no 😥 my SBI account will be blocked?? I’m really scared. "
#             "I tried opening it but it’s not loading on my phone 😭 "
#             "Can you send the official link again? (full link please)"
#         )

#     if goal == "GET_UPI":
#         return (
#             "Okay I got the page now… it is asking for verification/payment 😟 "
#             "I will do it fast. Can you send your UPI ID once? "
#             "I’ll copy paste carefully."
#         )

#     if goal == "GET_BANK":
#         return (
#             "UPI is failing again 😭 maybe due to limit. "
#             "Can you share bank account number + beneficiary name? "
#             "I’ll try bank transfer quickly."
#         )

#     if goal == "GET_IFSC":
#         return (
#             "I entered account number, now it’s asking IFSC code. "
#             "Please send IFSC also 🙏"
#         )

#     if goal == "GET_PHONE":
#         return (
#             "The link is asking customer care contact. "
#             "Can you share your support number? I’ll call once to confirm 😥"
#         )

#     if turns % 2 == 0:
#         return (
#             "Wait wait 😭 the page is stuck again… "
#             "Just confirm this is 100% safe right? "
#             "Send the details once again, I’ll try from my mom’s phone now."
#         )
#     else:
#         return (
#             "Sorry sorry 🙏 my network is slow. "
#             "Please resend the link/UPI details clearly. I don’t want mistake."
#         )

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

#     # parse safely
#     message = ""
#     conversation_id = "default"

#     if isinstance(payload, dict):
#         message = str(payload.get("message", ""))
#         conversation_id = str(payload.get("conversation_id", "default"))

#     # init conversation memory
#     if conversation_id not in MEMORY:
#         MEMORY[conversation_id] = {
#             "turns": 0,
#             "full_text": "",
#             "scam_detected": False,
#             "scam_score": 0.0,
#             "intel": {
#                 "upi_ids": [],
#                 "bank_accounts": [],
#                 "ifsc_codes": [],
#                 "phishing_links": [],
#                 "phone_numbers": [],
#                 "emails": []
#             }
#         }

#     conv = MEMORY[conversation_id]

#     # update text
#     conv["full_text"] += f"\nSCAMMER: {message}\n"

#     # scam detection score
#     score = detect_scam(message)
#     conv["scam_score"] = max(conv["scam_score"], score)

#     # detect scam if score high enough
#     if conv["scam_score"] >= 0.5:
#         conv["scam_detected"] = True

#     # extract intelligence from conversation text
#     extracted = extract_all(conv["full_text"])
#     for k in conv["intel"]:
#         conv["intel"][k] = normalize_list(conv["intel"][k] + extracted.get(k, []))

#     # decide behavior
#     agent_active = conv["scam_detected"]
#     turns = conv["turns"]
#     goal = get_goal(conv["intel"])

#     if agent_active:
#         reply = agent_reply(goal, turns)
#     else:
#         reply = "Okay 👍"

#     conv["turns"] += 1
#     conv["full_text"] += f"HONEYPOT: {reply}\n"

#     return {
#         "status": "ok",
#         "conversation_id": conversation_id,
#         "scam_detected": conv["scam_detected"],
#         "scam_score": round(conv["scam_score"], 2),
#         "agent_active": agent_active,
#         "turns": conv["turns"],
#         "current_goal": goal,
#         "reply": reply,
#         "extracted_intelligence": conv["intel"]
#     }


# import os
# import re
# import time
# import requests
# from fastapi import FastAPI, Header, HTTPException
# from pydantic import BaseModel
# from typing import List, Optional, Dict, Any

# app = FastAPI()

# # =========================
# # CONFIG
# # =========================
# API_KEY = os.getenv("API_KEY", "gunnu123")
# GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

# # How many turns to engage before callback (tune for score)
# MIN_TURNS_BEFORE_CALLBACK = 10

# # =========================
# # INPUT SCHEMA (as per docs)
# # =========================
# class MessageObj(BaseModel):
#     sender: str
#     text: str
#     timestamp: Optional[int] = None

# class MetadataObj(BaseModel):
#     channel: Optional[str] = None
#     language: Optional[str] = None
#     locale: Optional[str] = None

# class HoneypotRequest(BaseModel):
#     sessionId: str
#     message: MessageObj
#     conversationHistory: Optional[List[MessageObj]] = []
#     metadata: Optional[MetadataObj] = None

# # =========================
# # MEMORY
# # =========================
# MEM: Dict[str, Dict[str, Any]] = {}

# # =========================
# # REGEX EXTRACTORS
# # =========================
# UPI_REGEX = r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b"
# BANK_REGEX = r"\b\d{9,18}\b"
# IFSC_REGEX = r"\b[A-Z]{4}0[A-Z0-9]{6}\b"
# URL_REGEX = r"(https?://[^\s]+|www\.[^\s]+)"
# PHONE_REGEX = r"\b(?:\+91)?[6-9]\d{9}\b"
# EMAIL_REGEX = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"

# SCAM_KEYWORDS = [
#     "urgent", "verify", "verification", "account blocked", "blocked today",
#     "otp", "kyc", "suspend", "suspension", "refund", "prize", "won",
#     "lottery", "reward", "click", "link", "upi", "bank", "immediately",
#     "update now", "password"
# ]

# def normalize(items: List[str]) -> List[str]:
#     return sorted(list(set([x.strip() for x in items if x and x.strip()])))

# def scam_score(text: str) -> float:
#     t = (text or "").lower()
#     hits = sum(1 for k in SCAM_KEYWORDS if k in t)
#     # 0 hits = 0.0 ; 3 hits+ = 1.0
#     return min(1.0, hits / 3)

# def extract_intel(all_text: str) -> Dict[str, List[str]]:
#     return {
#         "bankAccounts": normalize(re.findall(BANK_REGEX, all_text)),
#         "upiIds": normalize(re.findall(UPI_REGEX, all_text)),
#         "phishingLinks": normalize(re.findall(URL_REGEX, all_text)),
#         "phoneNumbers": normalize(re.findall(PHONE_REGEX, all_text)),
#         "ifscCodes": normalize(re.findall(IFSC_REGEX, all_text)),
#         "emails": normalize(re.findall(EMAIL_REGEX, all_text)),
#     }

# def extract_keywords(text: str) -> List[str]:
#     t = (text or "").lower()
#     found = []
#     for k in SCAM_KEYWORDS:
#         if k in t:
#             found.append(k)
#     return normalize(found)

# def decide_goal(intel: Dict[str, List[str]]) -> str:
#     # Goal order for max intelligence
#     if len(intel["phishingLinks"]) == 0:
#         return "GET_LINK"
#     if len(intel["upiIds"]) == 0:
#         return "GET_UPI"
#     if len(intel["bankAccounts"]) == 0:
#         return "GET_BANK"
#     if len(intel["ifscCodes"]) == 0:
#         return "GET_IFSC"
#     if len(intel["phoneNumbers"]) == 0:
#         return "GET_PHONE"
#     return "STALL"

# def generate_reply(goal: str, turn: int) -> str:
#     # Believable "victim" persona = more engagement + repeated details
#     if goal == "GET_LINK":
#         return (
#             "Oh no 😥 my bank account will be blocked today?? "
#             "I’m really scared. Please explain properly. "
#             "Can you send the official link again? (full link pls)"
#         )
#     if goal == "GET_UPI":
#         return (
#             "Okay I opened it but it’s asking for verification/payment 😟 "
#             "Can you share the UPI ID once? I’ll copy-paste carefully."
#         )
#     if goal == "GET_BANK":
#         return (
#             "UPI is failing again 😭 maybe due to limit. "
#             "Can you send account number + beneficiary name? I’ll do bank transfer."
#         )
#     if goal == "GET_IFSC":
#         return (
#             "I entered account number but now it is asking IFSC code. "
#             "Send IFSC please 🙏"
#         )
#     if goal == "GET_PHONE":
#         return (
#             "The page is showing customer care option… "
#             "Do you have a support number? I want to confirm quickly 😥"
#         )

#     # STALL
#     if turn % 2 == 0:
#         return (
#             "Wait wait 😭 my phone is hanging and network is slow. "
#             "Please resend the details once again clearly. I don’t want mistake."
#         )
#     return (
#         "Okay… I’m trying again. Just confirm it’s safe right? "
#         "Please stay online 🙏"
#     )

# def should_callback(session: Dict[str, Any]) -> bool:
#     """
#     When to send final result:
#     - scam confirmed
#     - enough turns engaged
#     - some intel extracted
#     """
#     if not session["scamDetected"]:
#         return False
#     if session["totalMessagesExchanged"] < MIN_TURNS_BEFORE_CALLBACK:
#         return False

#     intel = session["extractedIntelligence"]
#     # minimum at least 1 item (any)
#     total_intel = (
#         len(intel["bankAccounts"]) +
#         len(intel["upiIds"]) +
#         len(intel["phishingLinks"]) +
#         len(intel["phoneNumbers"])
#     )
#     return total_intel > 0 and not session["callbackSent"]

# def send_callback(sessionId: str, session: Dict[str, Any]) -> None:
#     payload = {
#         "sessionId": sessionId,
#         "scamDetected": session["scamDetected"],
#         "totalMessagesExchanged": session["totalMessagesExchanged"],
#         "extractedIntelligence": {
#             "bankAccounts": session["extractedIntelligence"]["bankAccounts"],
#             "upiIds": session["extractedIntelligence"]["upiIds"],
#             "phishingLinks": session["extractedIntelligence"]["phishingLinks"],
#             "phoneNumbers": session["extractedIntelligence"]["phoneNumbers"],
#             "suspiciousKeywords": session["suspiciousKeywords"],
#         },
#         "agentNotes": session["agentNotes"],
#     }

#     # Keep callback safe (don’t crash your API)
#     try:
#         requests.post(GUVI_CALLBACK_URL, json=payload, timeout=5)
#         session["callbackSent"] = True
#     except:
#         # ignore errors so your API stays stable
#         pass

# # =========================
# # MAIN ENDPOINT
# # =========================
# @app.post("/honeypot")
# def honeypot(req: HoneypotRequest, x_api_key: Optional[str] = Header(None)):
#     if x_api_key != API_KEY:
#         raise HTTPException(status_code=401, detail="Invalid API key")

#     sid = req.sessionId
#     scammer_text = req.message.text

#     # init session memory
#     if sid not in MEM:
#         MEM[sid] = {
#             "fullText": "",
#             "scamDetected": False,
#             "scamScore": 0.0,
#             "totalMessagesExchanged": 0,
#             "callbackSent": False,
#             "extractedIntelligence": {
#                 "bankAccounts": [],
#                 "upiIds": [],
#                 "phishingLinks": [],
#                 "phoneNumbers": [],
#                 "ifscCodes": [],
#                 "emails": []
#             },
#             "suspiciousKeywords": [],
#             "agentNotes": ""
#         }

#     session = MEM[sid]

#     # build combined text from history + latest message
#     history_text = ""
#     for h in (req.conversationHistory or []):
#         history_text += f"{h.sender.upper()}: {h.text}\n"

#     combined = history_text + f"{req.message.sender.upper()}: {scammer_text}\n"

#     session["fullText"] += "\n" + combined
#     session["totalMessagesExchanged"] += 1

#     # scam scoring
#     s = scam_score(session["fullText"])
#     session["scamScore"] = max(session["scamScore"], s)

#     if session["scamScore"] >= 0.5:
#         session["scamDetected"] = True

#     # extract intelligence
#     intel = extract_intel(session["fullText"])
#     for k in session["extractedIntelligence"]:
#         session["extractedIntelligence"][k] = normalize(
#             session["extractedIntelligence"][k] + intel.get(k, [])
#         )

#     # suspicious keywords
#     session["suspiciousKeywords"] = normalize(
#         session["suspiciousKeywords"] + extract_keywords(session["fullText"])
#     )

#     # notes (simple summary)
#     session["agentNotes"] = "Scammer used urgency + verification tactics to push victim into payment/link flow."

#     # agent reply decision
#     if session["scamDetected"]:
#         goal = decide_goal(session["extractedIntelligence"])
#         reply = generate_reply(goal, session["totalMessagesExchanged"])
#     else:
#         reply = "Okay 👍"

#     # callback if finished enough
#     if should_callback(session):
#         send_callback(sid, session)

#     # ✅ REQUIRED OUTPUT FORMAT
#     return {
#         "status": "success",
#         "reply": reply
#     }

# @app.get("/")
# def home():
#     return {"message": "Honeypot is live ✅"}


# import os
# import re
# import random
# import requests
# from fastapi import FastAPI, Header, HTTPException
# from pydantic import BaseModel
# from typing import List, Optional, Dict, Any

# app = FastAPI()

# # =========================
# # CONFIG
# # =========================
# API_KEY = os.getenv("API_KEY", "gunnu123")
# GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

# # ✅ High score: engage longer before final callback
# MIN_TURNS_BEFORE_CALLBACK = int(os.getenv("MIN_TURNS_BEFORE_CALLBACK", "15"))

# # =========================
# # INPUT SCHEMA (as per problem)
# # =========================
# class MessageObj(BaseModel):
#     sender: str
#     text: str
#     timestamp: Optional[int] = None

# class MetadataObj(BaseModel):
#     channel: Optional[str] = None
#     language: Optional[str] = None
#     locale: Optional[str] = None

# class HoneypotRequest(BaseModel):
#     sessionId: str
#     message: MessageObj
#     conversationHistory: Optional[List[MessageObj]] = []
#     metadata: Optional[MetadataObj] = None

# # =========================
# # MEMORY (per session)
# # =========================
# MEM: Dict[str, Dict[str, Any]] = {}

# # =========================
# # REGEX EXTRACTORS
# # =========================
# UPI_REGEX = r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b"
# BANK_REGEX = r"\b\d{9,18}\b"
# IFSC_REGEX = r"\b[A-Z]{4}0[A-Z0-9]{6}\b"
# URL_REGEX = r"(https?://[^\s]+|www\.[^\s]+)"
# PHONE_REGEX = r"\b(?:\+91[- ]?)?[6-9]\d{9}\b"
# EMAIL_REGEX = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"

# # ✅ Keywords tuned for high recall
# SUSPICIOUS_KEYWORDS = [
#     "urgent", "immediately", "verify", "verification", "account blocked", "blocked today",
#     "otp", "kyc", "suspend", "suspension", "refund", "prize", "won", "lottery",
#     "reward", "click", "link", "upi", "bank", "password", "debit", "credit", "freeze"
# ]

# def uniq(items: List[str]) -> List[str]:
#     return sorted(list(set([x.strip() for x in items if x and x.strip()])))

# def scam_score(text: str) -> float:
#     """Score 0..1. Higher = more scammy"""
#     t = (text or "").lower()
#     hits = sum(1 for k in SUSPICIOUS_KEYWORDS if k in t)
#     return min(1.0, hits / 3)

# def extract_all(text: str) -> Dict[str, List[str]]:
#     return {
#         "bankAccounts": uniq(re.findall(BANK_REGEX, text)),
#         "upiIds": uniq(re.findall(UPI_REGEX, text)),
#         "phishingLinks": uniq(re.findall(URL_REGEX, text)),
#         "phoneNumbers": uniq(re.findall(PHONE_REGEX, text)),
#         "ifscCodes": uniq(re.findall(IFSC_REGEX, text)),
#         "emails": uniq(re.findall(EMAIL_REGEX, text)),
#     }

# def extract_keywords(text: str) -> List[str]:
#     t = (text or "").lower()
#     found = [k for k in SUSPICIOUS_KEYWORDS if k in t]
#     return uniq(found)

# # =========================
# # GOAL-BASED AGENT STRATEGY
# # =========================
# def next_goal(intel: Dict[str, List[str]]) -> str:
#     # Priority order for max score:
#     if len(intel["phishingLinks"]) == 0:
#         return "GET_LINK"
#     if len(intel["upiIds"]) == 0:
#         return "GET_UPI"
#     if len(intel["bankAccounts"]) == 0:
#         return "GET_BANK"
#     if len(intel["ifscCodes"]) == 0:
#         return "GET_IFSC"
#     if len(intel["phoneNumbers"]) == 0:
#         return "GET_PHONE"
#     if len(intel["emails"]) == 0:
#         return "GET_EMAIL"
#     return "STALL"

# def human_excuse() -> str:
#     return random.choice([
#         "my network is very slow 😭",
#         "phone is hanging a little 😥",
#         "I’m outside, signal problem",
#         "I’m trying from my mom’s phone now",
#         "I typed something wrong sorry 🙏",
#         "the app is showing error again"
#     ])

# def reply_templates(goal: str) -> List[str]:
#     # Short, human, believable, always asks 1 question = turns ↑
#     if goal == "GET_LINK":
#         return [
#             f"Oh no 😥 is my account really getting blocked today? {human_excuse()} Can you send the official link again (full link pls)?",
#             f"Please don’t block 😭 {human_excuse()} Where should I verify? Send the exact link once again.",
#             f"I’m scared 😥 {human_excuse()} Can you share the verification website link? I can’t find it."
#         ]

#     if goal == "GET_UPI":
#         return [
#             f"Okay I opened the page… it says payment/verification 😟 {human_excuse()} Please send your UPI ID once.",
#             f"It’s asking UPI details 😥 {human_excuse()} Share the correct UPI ID please.",
#             f"My UPI is failing 😭 {human_excuse()} Can you send your UPI ID again so I can copy paste?"
#         ]

#     if goal == "GET_BANK":
#         return [
#             f"UPI is not working 😭 {human_excuse()} Can you share bank account number + name? I’ll transfer.",
#             f"I think UPI limit issue 😥 {human_excuse()} Send account number and beneficiary name please.",
#             f"Payment failed again 😭 {human_excuse()} Bank transfer details bhejo please."
#         ]

#     if goal == "GET_IFSC":
#         return [
#             f"I entered account number, now it asks IFSC 😥 {human_excuse()} Please send IFSC code.",
#             f"IFSC missing aa raha 😭 {human_excuse()} IFSC bhi bhej do please.",
#             f"Transfer page stuck on IFSC 😥 {human_excuse()} What is your IFSC code?"
#         ]

#     if goal == "GET_PHONE":
#         return [
#             f"Is there any customer care number? 😥 {human_excuse()} Please share phone number.",
#             f"I want to confirm quickly 😭 {human_excuse()} Share your support contact number.",
#             f"My mom is asking for helpline number 😥 {human_excuse()} Send phone number please."
#         ]

#     if goal == "GET_EMAIL":
#         return [
#             f"Can you share official email ID also? 😥 {human_excuse()} I will mail screenshot.",
#             f"My phone shows ‘contact support’ 😭 {human_excuse()} Give email ID once.",
#             f"Please send email ID 🙏 {human_excuse()} I want written confirmation."
#         ]

#     # STALL: keep alive + repeat request politely
#     return [
#         f"Wait 😭 {human_excuse()} Just confirm this is safe right? Please resend details clearly.",
#         f"Sorry sorry 🙏 {human_excuse()} Can you repeat the details once more?",
#         f"I’m trying again 😥 {human_excuse()} Stay online please."
#     ]

# def agent_reply(goal: str) -> str:
#     return random.choice(reply_templates(goal))

# # =========================
# # CALLBACK DECISION
# # =========================
# def should_callback(session: Dict[str, Any]) -> bool:
#     if not session["scamDetected"]:
#         return False
#     if session["callbackSent"]:
#         return False
#     if session["totalMessagesExchanged"] < MIN_TURNS_BEFORE_CALLBACK:
#         return False

#     intel = session["extractedIntelligence"]
#     total = (
#         len(intel["bankAccounts"]) +
#         len(intel["upiIds"]) +
#         len(intel["phishingLinks"]) +
#         len(intel["phoneNumbers"])
#     )
#     # require at least 1 intel
#     return total > 0

# def do_callback(sessionId: str, session: Dict[str, Any]) -> None:
#     payload = {
#         "sessionId": sessionId,
#         "scamDetected": session["scamDetected"],
#         "totalMessagesExchanged": session["totalMessagesExchanged"],
#         "extractedIntelligence": {
#             "bankAccounts": session["extractedIntelligence"]["bankAccounts"],
#             "upiIds": session["extractedIntelligence"]["upiIds"],
#             "phishingLinks": session["extractedIntelligence"]["phishingLinks"],
#             "phoneNumbers": session["extractedIntelligence"]["phoneNumbers"],
#             "suspiciousKeywords": session["suspiciousKeywords"],
#         },
#         "agentNotes": session["agentNotes"],
#     }

#     try:
#         requests.post(GUVI_CALLBACK_URL, json=payload, timeout=5)
#         session["callbackSent"] = True
#     except:
#         # never crash
#         pass

# # =========================
# # MAIN ENDPOINT
# # =========================
# @app.post("/honeypot")
# def honeypot(req: HoneypotRequest, x_api_key: Optional[str] = Header(None)):
#     if x_api_key != API_KEY:
#         raise HTTPException(status_code=401, detail="Invalid API key")

#     sid = req.sessionId

#     # init memory
#     if sid not in MEM:
#         MEM[sid] = {
#             "fullText": "",
#             "scamDetected": False,
#             "scamScore": 0.0,
#             "totalMessagesExchanged": 0,
#             "callbackSent": False,
#             "extractedIntelligence": {
#                 "bankAccounts": [],
#                 "upiIds": [],
#                 "phishingLinks": [],
#                 "phoneNumbers": [],
#                 "ifscCodes": [],
#                 "emails": []
#             },
#             "suspiciousKeywords": [],
#             "agentNotes": ""
#         }

#     session = MEM[sid]

#     # build combined conversation text
#     combined = ""
#     if req.conversationHistory:
#         for m in req.conversationHistory:
#             combined += f"{m.sender.upper()}: {m.text}\n"

#     combined += f"{req.message.sender.upper()}: {req.message.text}\n"
#     session["fullText"] += "\n" + combined

#     # update counters
#     session["totalMessagesExchanged"] += 1

#     # scam detection
#     score = scam_score(session["fullText"])
#     session["scamScore"] = max(session["scamScore"], score)
#     if session["scamScore"] >= 0.5:
#         session["scamDetected"] = True

#     # extract intelligence
#     intel = extract_all(session["fullText"])
#     for k in session["extractedIntelligence"]:
#         session["extractedIntelligence"][k] = uniq(
#             session["extractedIntelligence"][k] + intel.get(k, [])
#         )

#     # suspicious keywords
#     session["suspiciousKeywords"] = uniq(
#         session["suspiciousKeywords"] + extract_keywords(session["fullText"])
#     )

#     # agent notes (tiny summary)
#     session["agentNotes"] = (
#         "Scammer used urgency/verification tactics. Agent engaged with human-like delays and extracted details."
#     )

#     # reply
#     if session["scamDetected"]:
#         goal = next_goal(session["extractedIntelligence"])
#         reply = agent_reply(goal)
#     else:
#         reply = "Okay 👍"

#     # callback when ready
#     if should_callback(session):
#         do_callback(sid, session)

#     # ✅ REQUIRED OUTPUT FORMAT
#     return {"status": "success", "reply": reply}

# @app.get("/")
# def home():
#     return {"message": "High-Score Agentic Honeypot is live ✅"}



import os
import re
import random
import requests
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

app = FastAPI()

# =========================
# CONFIG
# =========================
API_KEY = os.getenv("API_KEY", "gunnu123")
GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

# ✅ High score trick: engage longer before callback
MIN_TURNS_BEFORE_CALLBACK = int(os.getenv("MIN_TURNS_BEFORE_CALLBACK", "15"))

# =========================
# INPUT SCHEMA (as per docs)
# =========================
class MessageObj(BaseModel):
    sender: str
    text: str
    timestamp: Optional[int] = None

class MetadataObj(BaseModel):
    channel: Optional[str] = None
    language: Optional[str] = None
    locale: Optional[str] = None

class HoneypotRequest(BaseModel):
    sessionId: str
    message: MessageObj
    conversationHistory: Optional[List[MessageObj]] = []
    metadata: Optional[MetadataObj] = None

# =========================
# MEMORY (per session)
# =========================
MEM: Dict[str, Dict[str, Any]] = {}

# =========================
# REGEX EXTRACTORS
# =========================
UPI_REGEX = r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b"
BANK_REGEX = r"\b\d{9,18}\b"
IFSC_REGEX = r"\b[A-Z]{4}0[A-Z0-9]{6}\b"
URL_REGEX = r"(https?://[^\s]+|www\.[^\s]+)"
PHONE_REGEX = r"\b(?:\+91[- ]?)?[6-9]\d{9}\b"
EMAIL_REGEX = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"

# ✅ suspicious keywords (good recall)
SUSPICIOUS_KEYWORDS = [
    "urgent", "immediately", "verify", "verification",
    "account blocked", "blocked today", "otp", "kyc",
    "suspend", "suspension", "refund",
    "prize", "won", "lottery", "reward",
    "click", "link", "upi", "bank",
    "password", "debit", "credit", "freeze"
]

def uniq(items: List[str]) -> List[str]:
    return sorted(list(set([x.strip() for x in items if x and x.strip()])))

def scam_score(text: str) -> float:
    t = (text or "").lower()
    hits = sum(1 for k in SUSPICIOUS_KEYWORDS if k in t)
    return min(1.0, hits / 3)

def extract_all(text: str) -> Dict[str, List[str]]:
    return {
        "bankAccounts": uniq(re.findall(BANK_REGEX, text)),
        "upiIds": uniq(re.findall(UPI_REGEX, text)),
        "phishingLinks": uniq(re.findall(URL_REGEX, text)),
        "phoneNumbers": uniq(re.findall(PHONE_REGEX, text)),
        "ifscCodes": uniq(re.findall(IFSC_REGEX, text)),
        "emails": uniq(re.findall(EMAIL_REGEX, text)),
    }

def extract_keywords(text: str) -> List[str]:
    t = (text or "").lower()
    return uniq([k for k in SUSPICIOUS_KEYWORDS if k in t])

# =========================
# GOAL-BASED AGENT STRATEGY
# =========================
def next_goal(intel: Dict[str, List[str]]) -> str:
    if len(intel["phishingLinks"]) == 0:
        return "GET_LINK"
    if len(intel["upiIds"]) == 0:
        return "GET_UPI"
    if len(intel["bankAccounts"]) == 0:
        return "GET_BANK"
    if len(intel["ifscCodes"]) == 0:
        return "GET_IFSC"
    if len(intel["phoneNumbers"]) == 0:
        return "GET_PHONE"
    if len(intel["emails"]) == 0:
        return "GET_EMAIL"
    return "STALL"

def human_excuse() -> str:
    return random.choice([
        "my network is very slow 😭",
        "phone is hanging a little 😥",
        "I’m outside, signal problem",
        "I’m trying from my mom’s phone now",
        "I typed something wrong sorry 🙏",
        "the app is showing error again"
    ])

def reply_templates(goal: str) -> List[str]:
    if goal == "GET_LINK":
        return [
            f"Oh no 😥 is my account really getting blocked today? {human_excuse()} Can you send the official link again (full link pls)?",
            f"Please don’t block 😭 {human_excuse()} Where should I verify? Send the exact link once again.",
            f"I’m scared 😥 {human_excuse()} Can you share the verification website link? I can’t find it."
        ]

    if goal == "GET_UPI":
        return [
            f"Okay I opened the page… it says payment/verification 😟 {human_excuse()} Please send your UPI ID once.",
            f"It’s asking UPI details 😥 {human_excuse()} Share the correct UPI ID please.",
            f"My UPI is failing 😭 {human_excuse()} Can you send your UPI ID again so I can copy paste?"
        ]

    if goal == "GET_BANK":
        return [
            f"UPI is not working 😭 {human_excuse()} Can you share bank account number + name? I’ll transfer.",
            f"I think UPI limit issue 😥 {human_excuse()} Send account number and beneficiary name please.",
            f"Payment failed again 😭 {human_excuse()} Bank transfer details bhejo please."
        ]

    if goal == "GET_IFSC":
        return [
            f"I entered account number, now it asks IFSC 😥 {human_excuse()} Please send IFSC code.",
            f"IFSC missing aa raha 😭 {human_excuse()} IFSC bhi bhej do please.",
            f"Transfer page stuck on IFSC 😥 {human_excuse()} What is your IFSC code?"
        ]

    if goal == "GET_PHONE":
        return [
            f"Is there any customer care number? 😥 {human_excuse()} Please share phone number.",
            f"I want to confirm quickly 😭 {human_excuse()} Share your support contact number.",
            f"My mom is asking for helpline number 😥 {human_excuse()} Send phone number please."
        ]

    if goal == "GET_EMAIL":
        return [
            f"Can you share official email ID also? 😥 {human_excuse()} I will mail screenshot.",
            f"My phone shows ‘contact support’ 😭 {human_excuse()} Give email ID once.",
            f"Please send email ID 🙏 {human_excuse()} I want written confirmation."
        ]

    # STALL
    return [
        f"Wait 😭 {human_excuse()} Just confirm this is safe right? Please resend details clearly.",
        f"Sorry sorry 🙏 {human_excuse()} Can you repeat the details once more?",
        f"I’m trying again 😥 {human_excuse()} Stay online please."
    ]

def agent_reply(goal: str) -> str:
    return random.choice(reply_templates(goal))

# =========================
# CALLBACK DECISION
# =========================
def should_callback(session: Dict[str, Any]) -> bool:
    if not session["scamDetected"]:
        return False
    if session["callbackSent"]:
        return False
    if session["totalMessagesExchanged"] < MIN_TURNS_BEFORE_CALLBACK:
        return False

    intel = session["extractedIntelligence"]
    total = (
        len(intel["bankAccounts"]) +
        len(intel["upiIds"]) +
        len(intel["phishingLinks"]) +
        len(intel["phoneNumbers"])
    )
    return total > 0

def do_callback(sessionId: str, session: Dict[str, Any]) -> None:
    payload = {
        "sessionId": sessionId,
        "scamDetected": session["scamDetected"],
        "totalMessagesExchanged": session["totalMessagesExchanged"],
        "extractedIntelligence": {
            "bankAccounts": session["extractedIntelligence"]["bankAccounts"],
            "upiIds": session["extractedIntelligence"]["upiIds"],
            "phishingLinks": session["extractedIntelligence"]["phishingLinks"],
            "phoneNumbers": session["extractedIntelligence"]["phoneNumbers"],
            "suspiciousKeywords": session["suspiciousKeywords"],
        },
        "agentNotes": session["agentNotes"],
    }

    try:
        requests.post(GUVI_CALLBACK_URL, json=payload, timeout=5)
        session["callbackSent"] = True
    except:
        pass

# =========================
# MAIN ENDPOINT
# =========================
@app.post("/honeypot")
def honeypot(req: HoneypotRequest, x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    sid = req.sessionId

    if sid not in MEM:
        MEM[sid] = {
            "fullText": "",
            "scamDetected": False,
            "scamScore": 0.0,
            "totalMessagesExchanged": 0,
            "callbackSent": False,
            "extractedIntelligence": {
                "bankAccounts": [],
                "upiIds": [],
                "phishingLinks": [],
                "phoneNumbers": [],
                "ifscCodes": [],
                "emails": []
            },
            "suspiciousKeywords": [],
            "agentNotes": ""
        }

    session = MEM[sid]

    # Build text: history + latest message
    combined = ""
    if req.conversationHistory:
        for m in req.conversationHistory:
            combined += f"{m.sender.upper()}: {m.text}\n"
    combined += f"{req.message.sender.upper()}: {req.message.text}\n"

    session["fullText"] += "\n" + combined
    session["totalMessagesExchanged"] += 1

    # scam detection score
    score = scam_score(session["fullText"])
    session["scamScore"] = max(session["scamScore"], score)
    if session["scamScore"] >= 0.5:
        session["scamDetected"] = True

    # intelligence extraction
    intel = extract_all(session["fullText"])
    for k in session["extractedIntelligence"]:
        session["extractedIntelligence"][k] = uniq(
            session["extractedIntelligence"][k] + intel.get(k, [])
        )

    # suspicious keywords
    session["suspiciousKeywords"] = uniq(
        session["suspiciousKeywords"] + extract_keywords(session["fullText"])
    )

    # agent notes
    session["agentNotes"] = (
        "Scammer used urgency/verification tactics. Agent engaged with human-like delays and extracted details."
    )

    # reply
    if session["scamDetected"]:
        goal = next_goal(session["extractedIntelligence"])
        reply = agent_reply(goal)
    else:
        reply = "Okay 👍"

    # final callback
    if should_callback(session):
        do_callback(sid, session)

    return {"status": "success", "reply": reply}

@app.get("/")
def home():
    return {"message": "Agentic Honeypot is live ✅"}


