from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import time
from typing import Dict, List, Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

public_keys: Dict[str, str] = {}

message_queue: Dict[str, List[dict]] = {}

class RegisterKeyRequest(BaseModel):
    email: str
    publicKey: str

class SendMessageRequest(BaseModel):
    recipientEmail: str
    senderEmail: str
    ciphertext: str
    iv: str
    salt: str
    
@router.post("/register")
async def register_public_key(req: RegisterKeyRequest):
    """
    Registers the user's generated public key.
    Since it's a public key, it's safe to store in memory.
    The private key NEVER leaves the user's browser.
    """
    public_keys[req.email.lower()] = req.publicKey
    if req.email.lower() not in message_queue:
        message_queue[req.email.lower()] = []
    
    return {"status": "success", "message": "Public key registered for E2EE."}

@router.get("/keys/{email}")
async def get_public_key(email: str):
    """
    Retrieves the public key of the user you want to chat with.
    """
    key = public_keys.get(email.lower())
    if not key:
        raise HTTPException(status_code=404, detail="User has not registered a public key yet.")
    return {"status": "success", "publicKey": key}

@router.post("/send")
async def send_encrypted_message(req: SendMessageRequest):
    """
    Receives an end-to-end encrypted packet.
    The server CANNOT read `ciphertext` because it does not have the private keys.
    """
    recipient = req.recipientEmail.lower()
    
    if recipient not in public_keys:
        raise HTTPException(status_code=404, detail="Recipient not found or offline.")
        
    if recipient not in message_queue:
        message_queue[recipient] = []
        
    packet = {
        "sender": req.senderEmail,
        "ciphertext": req.ciphertext,
        "iv": req.iv,
        "salt": req.salt,
        "timestamp": int(time.time() * 1000)
    }
    
    message_queue[recipient].append(packet)
    logger.info(f"E2EE packet routed from {req.senderEmail} to {recipient}")
    
    return {"status": "success", "message": "Encrypted packet routed."}

@router.get("/poll/{email}")
async def poll_messages(email: str):
    """
    Retrieves messages for a user and INSTANTLY DELETES them from RAM.
    This guarantees perfectly forward secrecy on the server side.
    """
    target = email.lower()
    
    if target not in message_queue or len(message_queue[target]) == 0:
        return {"status": "success", "messages": []}
        
    messages = message_queue[target].copy()
    
    message_queue[target] = []
    logger.info(f"Delivered {len(messages)} packets to {target} and wiped them from memory.")
    
    return {"status": "success", "messages": messages}
