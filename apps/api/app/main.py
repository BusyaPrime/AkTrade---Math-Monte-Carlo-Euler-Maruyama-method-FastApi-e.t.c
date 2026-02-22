from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.market.routes import router as market_router
from app.market.social.routes import router as social_router
from app.market.social.news import router as news_router
from app.market.analytics.routes import router as analytics_router
from app.trading.routes import router as trading_router
from app.ws.routes import router as ws_router
from app.chat.routes import router as chat_router
from app.admin.routes import router as admin_router

app = FastAPI(
    title="AkTrade API",
    version="1.0.0",
    description="Premium Trading Terminal API"
)

# Настройки CORS (чтоб локальный некст не орал кровоточащими ошибками в консоль)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3003"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market_router, prefix="/v1")
app.include_router(social_router, prefix="/v1/social")
app.include_router(news_router, prefix="/v1/social")
app.include_router(analytics_router, prefix="/v1/analytics")
app.include_router(trading_router, prefix="/v1")
app.include_router(ws_router, prefix="/v1")
app.include_router(chat_router, prefix="/v1/chat")
app.include_router(admin_router, prefix="/v1/admin")

@app.get("/health")
async def health_check():
    """
    Пингуем живой ли сервак. Спойлер: пока живой, кубернетес еще не прибил под.
    """
    return {"status": "ok"}
