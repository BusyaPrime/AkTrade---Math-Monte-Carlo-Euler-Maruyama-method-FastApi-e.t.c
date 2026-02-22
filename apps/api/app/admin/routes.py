from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import time
from typing import List, Dict, Optional
import uuid

router = APIRouter()

# Храним тикеты саппорта прямо в памяти (да-да, In-Memory DB 😎).
# По-хорошему тут должна быть нормальная реляционка (Postgres), но пока и так сойдет.
SUPPORT_TICKETS: List[Dict] = []

class TicketSubmitRequest(BaseModel):
    subject: str
    message: str
    email: str

class AdminLoginRequest(BaseModel):
    username: str
    password: str

@router.post("/support/ticket")
async def submit_support_ticket(req: TicketSubmitRequest):
    """
    Создает новый тикет в админку. Юзеры жалуются — мы делаем вид, что читаем.
    """
    new_ticket = {
        "id": str(uuid.uuid4())[:8],
        "subject": req.subject,
        "message": req.message,
        "email": req.email,
        "status": "New", # Статусы: New (игнорируем), In Progress (типа делаем), Resolved (забили)
        "timestamp": int(time.time() * 1000)
    }
    
    # Кидаем в начало списка, чтобы самые злые юзеры были первыми
    SUPPORT_TICKETS.insert(0, new_ticket)
    
    return {"status": "success", "ticket_id": new_ticket["id"]}

@router.post("/login")
async def admin_login(req: AdminLoginRequest):
    """
    Супер-мега-секретная авторизация для админов (admin / admin).
    """
    if req.username == "admin" and req.password == "admin":
        return {
            "status": "success", 
            "token": "aktrade_admin_token_xyz987"
        }
    
    # Если кто-то не угадал пароль admin/admin
    raise HTTPException(status_code=401, detail="Invalid admin credentials.")

@router.get("/support/tickets")
async def get_support_tickets(token: Optional[str] = None):
    """
    Отдает все тикеты. Эндпоинт для дашборда.
    """
    return {"status": "success", "data": SUPPORT_TICKETS}
