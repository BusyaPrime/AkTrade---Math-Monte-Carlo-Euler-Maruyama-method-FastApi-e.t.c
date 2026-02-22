from fastapi import APIRouter, HTTPException
import httpx
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

CRYPTOPANIC_API_URL = "https://cryptopanic.com/api/v1/posts/?auth_token=YOUR_API_KEY_HERE"

@router.get("/news")
async def get_market_news():
    """
    Фейковые новости для MVP. Юзеры всё равно читают только заголовки.
    """
    try:
        
        real_news = [
            {
                "id": "news-1",
                "title": "Bitcoin Surges Past Institutional Resistance Levels Amid ETF Inflows",
                "domain": "coindesk.com",
                "source": "CoinDesk",
                "published_at": "10 minutes ago",
                "url": "https://coindesk.com",
                "sentiment": "bullish"
            },
            {
                "id": "news-2",
                "title": "Federal Reserve Signals Potential Rate Cuts by Q3 2026",
                "domain": "bloomberg.com",
                "source": "Bloomberg",
                "published_at": "45 minutes ago",
                "url": "https://bloomberg.com",
                "sentiment": "bullish"
            },
            {
                "id": "news-3",
                "title": "Solana Network Prepares for Major Mainnet Upgrade to Ease Congestion",
                "domain": "decrypt.co",
                "source": "Decrypt",
                "published_at": "2 hours ago",
                "url": "https://decrypt.co",
                "sentiment": "bullish"
            },
            {
                "id": "news-4",
                "title": "SEC Delays Decision on Ethereum Spot ETFs Again",
                "domain": "cointelegraph.com",
                "source": "CoinTelegraph",
                "published_at": "4 hours ago",
                "url": "https://cointelegraph.com",
                "sentiment": "bearish"
            },
            {
                "id": "news-5",
                "title": "Tech Stocks Tumble as AI Sector Faces Profit-Taking Corrections",
                "domain": "wsj.com",
                "source": "Wall Street Journal",
                "published_at": "5 hours ago",
                "url": "https://wsj.com",
                "sentiment": "bearish"
            },
            {
                "id": "news-6",
                "title": "Whale Moves $1.2B in BTC to Unknown Wallet: Market Reacts",
                "domain": "theblock.co",
                "source": "The Block",
                "published_at": "6 hours ago",
                "url": "https://theblock.co",
                "sentiment": "neutral"
            }
        ]
        return {"status": "success", "data": real_news}
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch market news")

@router.get("/news/all")
async def get_all_market_news():
    """
    Генерим кучу фейк кликбейта чтобы страница выглядела живой 📈
    """
    import random
    from datetime import datetime, timedelta
    
    base_titles = [
        "Bitcoin Surges Past Institutional Resistance Levels Amid ETF Inflows",
        "Federal Reserve Signals Potential Rate Cuts by Q3 2026",
        "Solana Network Prepares for Major Mainnet Upgrade to Ease Congestion",
        "SEC Delays Decision on Ethereum Spot ETFs Again",
        "Tech Stocks Tumble as AI Sector Faces Profit-Taking Corrections",
        "Whale Moves $1.2B in BTC to Unknown Wallet: Market Reacts",
        "New Crypto Regulation Bill Proposed in Senate",
        "DeFi Summer 2.0? TVL Hits All-Time Highs Across L2s",
        "Apple Integrates Crypto Payment Options in Latest Update",
        "Meme Coin Frenzy Returns: PEPE and WIF Lead Market Rebound",
        "Binance Announces New Listing: Surge Follows",
        "MicroStrategy Buys Another 5,000 BTC, Doubling Down on Stash",
        "Gold Hits Record High, Correlating With Crypto Haven Demand",
        "European Union Finalizes MiCA Implementation Guidelines",
        "AI Crypto Tokens See 40% Bump After Major Compute Breakthrough"
    ]
    
    sources = [
        ("CoinDesk", "coindesk.com"),
        ("Bloomberg", "bloomberg.com"),
        ("Decrypt", "decrypt.co"),
        ("CoinTelegraph", "cointelegraph.com"),
        ("Wall Street Journal", "wsj.com"),
        ("The Block", "theblock.co"),
        ("Reuters", "reuters.com"),
        ("CNBC", "cnbc.com")
    ]
    
    sentiments = ["bullish", "bearish", "neutral"]
    
    news = []
    for i in range(1, 45):
        source, domain = random.choice(sources)
        minutes_ago = random.randint(1, 2880)
        if minutes_ago < 60:
            time_str = f"{minutes_ago} minutes ago"
        elif minutes_ago < 1440:
            time_str = f"{minutes_ago // 60} hours ago"
        else:
            time_str = f"{minutes_ago // 1440} days ago"
            
        news.append({
            "id": f"news-all-{i}",
            "title": f"{random.choice(base_titles)}{' - Essential Reading' if i % 7 == 0 else ''}",
            "domain": domain,
            "source": source,
            "published_at": time_str,
            "url": f"https://{domain}/news/{i}",
            "sentiment": random.choice(sentiments)
        })
        
    return {"status": "success", "data": news}
