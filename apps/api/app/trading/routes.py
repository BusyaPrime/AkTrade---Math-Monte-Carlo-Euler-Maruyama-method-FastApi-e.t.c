from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class OrderReq(BaseModel):
    symbol: str
    side: str
    type: str
    qty: float
    limitPx: float = None
    stopPx: float = None

@router.post("/orders")
async def create_order(order: OrderReq):
    """
    Тут мы принимаем ордера от мамкиных трейдеров.
    Фронт шлет JSON, мы делаем вид, что исполняем это на Насдаке.
    """
    return {"status": "NEW", "order": order.model_dump()}

@router.get("/orders")
async def get_orders(status: str = "OPEN"):
    return {"status": status, "orders": []}

@router.get("/positions")
async def get_positions():
    """
    Отдаем текущие позы. Если честно, хардкод ради UI, но кто проверит?
    """
    return {"positions": [
        {"symbol": "AAPL", "qty": 10, "avgPx": 145.0},
        {"symbol": "TSLA", "qty": -5, "avgPx": 210.0} # Хаха, шортят теслу, земля пухом
    ]}

@router.post("/watchlists")
async def create_watchlist():
    # Юзер решил, что он инвестор и хочет следить за щитками
    return {"id": "wl_123", "name": "Default"}

@router.put("/watchlists/{id}")
async def update_watchlist(id: str):
    return {"id": id, "status": "updated"}
