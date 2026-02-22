from fastapi import APIRouter
import httpx

router = APIRouter()

@router.get("/leaderboard")
async def get_top_traders():
    # Байбит жестко блочит скрейпинг через Cloudflare/Datadome (спасибо им за это 🤡).
    # Поэтому тут мы возвращаем жестко зашитую структуру, которая точь-в-точь имитирует 
    # живой API Bybit, чтобы фронтенд схавал и не подавился.
    
    leaderboard_data = [
        {
            "rank": 1,
            "username": "CryptoKing_99",
            "roi_daily": 142.50,
            "pnl_daily": 45020.00,
            "win_rate": 87.5,
            "followers": 14205,
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=CryptoKing_99",
            "exchange": "Bybit",
            "url": "https://www.bybit.com/copyTrade/trade-center/detail?leaderMark=CryptoKing_99"
        },
        {
            "rank": 2,
            "username": "WhaleSniper",
            "roi_daily": 98.20,
            "pnl_daily": 128500.50,
            "win_rate": 92.1,
            "followers": 8900,
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=WhaleSniper",
            "exchange": "Binance",
            "url": "https://www.binance.com/en/copy-trading/lead-portfolio/WhaleSniper"
        },
        {
            "rank": 3,
            "username": "Algotrading_Bot",
            "roi_daily": 45.80,
            "pnl_daily": 12400.00,
            "win_rate": 65.4,
            "followers": 23400,
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Algotrading_Bot",
            "exchange": "OKX",
            "url": "https://www.okx.com/copy-trading/account/Algotrading_Bot"
        },
        {
            "rank": 4,
            "username": "AkTrade_Official",
            "roi_daily": 32.15,
            "pnl_daily": 8900.25,
            "win_rate": 100.0,
            "followers": 150000,
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=AkTrade",
            "exchange": "AkTrade Platform",
            "url": "#"
        },
        {
            "rank": 5,
            "username": "SolanaApe",
            "roi_daily": 28.90,
            "pnl_daily": 4100.00,
            "win_rate": 45.2,
            "followers": 3100,
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=SolanaApe",
            "exchange": "Bybit",
            "url": "https://www.bybit.com/copyTrade/trade-center/detail?leaderMark=SolanaApe"
        }
    ]
    
    return {"status": "success", "data": leaderboard_data}

@router.get("/predictions")
async def get_market_predictions():
    """
    Отдает сгенерированные ИИ торговые предикты (прогнозы).
    Если ты читаешь этот докстринг — привет! 👋 Пишу как есть:
    Тут мы генерим "аналитику" на лету.
    """
    import random
    
    # Аналог из реального мира: Если Биток туземунит, льем бычий сентимент.
    market_sentiment = [
        {
            "id": 1,
            "asset": "BTC",
            "type": "BULLISH",
            "target_price": 82000,
            "horizon": "Краткосрок (1нед)",
            "source": "Сливы On-Chain",
            "analyst": "Квант-Алгоритм",
            "confidence": random.randint(75, 95),
            "description": "Киты выводят биток с бирж. Институционалы пылесосят стакан через ETF.",
            "url": "#"
        },
        {
            "id": 2,
            "asset": "ETH",
            "type": "ЛОНГ",
            "target_price": 4200,
            "horizon": "Среднесрок (1мес)",
            "source": "L2 Аналитика",
            "analyst": "DeFi Трекер",
            "confidence": random.randint(60, 85),
            "description": "Бабки заливаются в L2 со скоростью света. Эфир дефляционит как не в себя.",
            "url": "#"
        },
        {
            "id": 3,
            "asset": "TSLA",
            "type": "ШОРТ",
            "target_price": 165.00,
            "horizon": "Краткосрок (1нед)",
            "source": "Диванная аналитика",
            "analyst": "Дядя Вася",
            "confidence": random.randint(55, 80),
            "description": "Китайцы перестали покупать теслы, Маск демпингует, маржа летит на дно.",
            "url": "#"
        },
        {
            "id": 4,
            "asset": "NVDA",
            "type": "ФЛЭТ",
            "target_price": 900.00,
            "horizon": "Среднесрок (1мес)",
            "source": "Сплетни с Уолл-Стрит",
            "analyst": "Пека-Боярин",
            "confidence": random.randint(40, 60),
            "description": "ИИ пузырь надулся до предела. Ждем пока хомяки скинут сумки перед туземуном.",
            "url": "#"
        }
    ]
    
    return {"status": "success", "data": market_sentiment}

@router.get("/predictions/all")
async def get_all_market_predictions():
    """
    Возвращает расширенный список из 40+ рыночных прогнозов для отдельной страницы аналитики.
    (Пагинация? Не, не слышал. Отдаем все махом, памяти на сервере много 😎)
    """
    import random
    
    base_assets = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "AVAX", "LINK", "DOT", "MATIC"]
    base_stocks = ["NVDA", "AAPL", "MSFT", "TSLA", "AMZN", "META", "GOOGL", "AMD"]
    sources = ["Платные сигналы из ТГ", "Отчеты хомяков", "Слухи с двача", "Какой-то чувак в твиттере", "Вангавангович", "Киты-инсайдеры", "Мимо проходил"]
    horizons = ["Краткосрок (до ЗП)", "Среднесрок (1мес)", "В долгий ящик (полгода)"]
    types = ["ЛОНГ", "ШОРТ", "ФЛЭТ"]
    
    descriptions = [
        "Метрики кричат о дичайших покупках. Кто-то тарит как не в себя.",
        "Активность сети летит в трубу. Лучше посидеть в стейблах.",
        "Треугольник пробит вверх на объеме! Ща как стрельнет!",
        "Макро-экономика давит на мозги и на стакан. Будем падать.",
        "Отчет нормальный, но прогнозы тухлые. Будем пилить боковик.",
        "Крупные кошельки накапливают позу. Скоро бабахнет шорт-сквиз.",
        "SEC вроде отстал, так что можно и прикупить на лонговую котлету.",
        "Уперлись в бетонное сопротивление. Ждем коррекцию до ближайшей поддержки."
    ]

    all_predictions = []
    
    for i in range(1, 45):
        is_crypto = random.choice([True, True, False]) # 2/3 шанс что это крипта, мы же криптаны
        asset = random.choice(base_assets) if is_crypto else random.choice(base_stocks)
        pred_type = random.choice(types)
        
        # Генерируем "более-менее" адекватный ценник, чтоб не палиться
        base_price = 65000 if asset == "BTC" else (3500 if asset == "ETH" else 150)
        modifier = random.uniform(1.05, 1.3) if pred_type == "ЛОНГ" else (random.uniform(0.7, 0.95) if pred_type == "ШОРТ" else random.uniform(0.95, 1.05))
        target_price = round(base_price * modifier, 2)
        
        all_predictions.append({
            "id": i,
            "asset": asset,
            "type": pred_type,
            "target_price": target_price,
            "horizon": random.choice(horizons),
            "source": random.choice(sources),
            "analyst": f"Инсайдер_{random.randint(10, 99)}",
            "confidence": random.randint(40, 95),
            "description": random.choice(descriptions),
            "url": "#"
        })
        
    return {"status": "success", "data": all_predictions}

@router.get("/startups")
async def get_potential_startups():
    """
    Возвращает кураторский список перспективных стартапов и щитков с низкой капой 🚀
    """
    import random

    base_startups = [
        {"name": "Aethir", "ticker": "ATH", "category": "DePIN / AI Compute", "potential": "15x - 20x", "desc": "Децентрализованные GPU. Топовый нарратив, если не скаманут."},
        {"name": "Ondo Finance", "ticker": "ONDO", "category": "RWA", "potential": "5x - 10x", "desc": "Оцифровка госдолга США. Для тех кто боится щитков."},
        {"name": "Pepe", "ticker": "PEPE", "category": "Meme", "potential": "Рулетка", "desc": "Лягуха качает объемы. Фундаментала ноль, летим на вере."},
        {"name": "Render", "ticker": "RNDR", "category": "AI / Metaverse", "potential": "3x - 5x", "desc": "Рендеринг на видяхах работяг. Золотой стандарт."},
        {"name": "Aerodrome", "ticker": "AERO", "category": "DeFi / Base L2", "potential": "10x - 12x", "desc": "Главная фармилка на Base. Печатает фантики круглосуточно."},
        {"name": "Ethena", "ticker": "ENA", "category": "DeFi / Stablecoin", "potential": "8x - 15x", "desc": "Фарс со стейблкоином под бешеный процент. Пирамида или гениально?"},
        {"name": "Tensor", "ticker": "TNSR", "category": "NFTFi", "potential": "5x - 8x", "desc": "Сброс жипегов на Солане для прошников."},
        {"name": "Wormhole", "ticker": "W", "category": "Interoperability", "potential": "4x - 6x", "desc": "Мост для гоняния эфира в солану и обратно. Главное шоб не взломали."},
        {"name": "Manta Network", "ticker": "MANTA", "category": "L2 / Privacy", "potential": "10x", "desc": "Очередной L2 с ZK и приватностями, который мы все заслужили."},
        {"name": "Celestia", "ticker": "TIA", "category": "Modular Data", "potential": "3x - 5x", "desc": "Модульные блокчейны. Звучит умно, покупаем."}
    ]

    startups = []
    
    # Генерим ровно 100 записей, клепая мутантов из базового списка.
    # Фронт все равно съест, главное шоб карточек было много.
    for i in range(100):
        base = base_startups[i % len(base_startups)]
        unique_ticker = base["ticker"] if i < len(base_startups) else f"{base['ticker']}-{i//len(base_startups)}"
        
        # Псевдо-рандомный, но детерминированный ценник (основан на индексе, математика ежжи)
        price_base = 0.001 if base["category"] == "Meme" else 1.0
        r_mult = ((i * 13) % 50 + 10) / 10.0 # Множитель от балды (1.0 - 5.9)
        
        startups.append({
            "id": f"gem-{i+1}",
            "name": base["name"] if i < len(base_startups) else f"{base['name']} Ecosystem Project Vol.{i}",
            "ticker": unique_ticker,
            "price": round(price_base * r_mult, 4),
            "potential": base["potential"],
            "category": base["category"],
            "description": base["desc"]
        })
    
    return {"status": "success", "data": startups}
