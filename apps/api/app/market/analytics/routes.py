from fastapi import APIRouter
from pydantic import BaseModel
import numpy as np
import time

router = APIRouter()

BASE_PRICES = {
    "BTC": 65120.50,
    "ETH": 3450.75,
    "SOL": 145.20,
    "NVDA": 900.00,
    "AAPL": 151.24,
}

from dataclasses import dataclass

@dataclass
class BayesianBatesParams:
    # Байесовские априорные параметры (семплируются для каждого пути симуляции)
    # Байесовские априорные параметры (семплируются для каждого пути симуляции)
    r: np.ndarray       # Безрисковая ставка
    q: np.ndarray       # Дивидендная доходность (на крипте обычно 0, но пусть будет для совместимости)
    v0: np.ndarray      # Начальная дисперсия (насколько нас сейчас штормит)
    kappa: np.ndarray   # Скорость возврата к среднему (рынок всё равно побреет)
    theta: np.ndarray   # Долгосрочная средняя дисперсия
    sigma_v: np.ndarray # Волатильность волатильности (да, тут все сложно)
    rho: np.ndarray     # Корреляция между ценой и волатильностью
    lambda_j: np.ndarray# Интенсивность скачков (как часто Илон Маск твитит)
    mu_j: np.ndarray    # Средний размер скачка
    sigma_j: np.ndarray # Волатильность размера скачка (амплитуда паники)

def draw_bayesian_posteriors(symbol: str, simulations: int) -> BayesianBatesParams:
    """
    Генерация параметров из смоделированных Байесовских апостериорных распределений для каждого пути,
    чтобы учесть экстремальную неопределенность параметров (Эпистемический риск).
    """
    if symbol in ["BTC", "ETH", "SOL"]:
        r = np.random.normal(0.08, 0.02, simulations)
        q = np.zeros(simulations)
        v0 = np.random.lognormal(-1.0, 0.2, simulations)
        kappa = np.random.gamma(15, 0.1, simulations)
        theta = np.random.gamma(36, 0.01, simulations)
        sigma_v = np.random.lognormal(-0.9, 0.1, simulations)
        rho = np.random.uniform(-0.9, -0.4, simulations)
        lambda_j = np.random.gamma(25, 0.2, simulations)
        mu_j = np.random.normal(-0.05, 0.02, simulations)
        sigma_j = np.random.gamma(22.5, 0.006, simulations)
    else:
        r = np.random.normal(0.05, 0.01, simulations)
        q = np.zeros(simulations)
        v0 = np.random.lognormal(-2.7, 0.1, simulations)
        kappa = np.random.gamma(20, 0.1, simulations)
        theta = np.random.gamma(30, 0.002, simulations)
        sigma_v = np.random.lognormal(-2.3, 0.1, simulations)
        rho = np.random.uniform(-0.8, -0.3, simulations)
        lambda_j = np.random.gamma(10, 0.1, simulations)
        mu_j = np.random.normal(-0.02, 0.01, simulations)
        sigma_j = np.random.gamma(12.5, 0.004, simulations)

    return BayesianBatesParams(
        r=r, q=q, v0=v0, kappa=kappa, theta=theta, 
        sigma_v=sigma_v, rho=rho, lambda_j=lambda_j, 
        mu_j=mu_j, sigma_j=sigma_j
    )

@router.get("/monte-carlo/{symbol}")
async def get_monte_carlo_simulation(symbol: str, days: int = 30, simulations: int = 1000):
    """
    Продвинутая симуляция Монте-Карло с использованием модели Бейтса и параметризацией режимов.
    Рассчитывает Value at Risk (VaR), Conditional Value at Risk (CVaR / Ожидаемые потери)
    и Probability of Profit (Вероятность прибыли).
    
    P.S. Если ты ревьюишь этот код и дочитал до сюда — моё увожение 🤝 
    Формулы ниже сожрут твой проц, но зато графики будут красивые.
    """
    start_time = time.time()
    symbol = symbol.upper()
    S0 = BASE_PRICES.get(symbol, 100.0)
    
    # 1. Тащим массивные параметры (байесовская магия)
    params = draw_bayesian_posteriors(symbol, simulations)
    
    T = days / 365.0  # Временной горизонт в годах
    dt = T / days     # Размер каждого шага
    
    # Инициализация массивов для цены (S) и дисперсии (v)
    # Numpy нулями заполняет со скоростью света
    S = np.zeros((days + 1, simulations))
    v = np.zeros((days + 1, simulations))
    
    S[0] = S0
    v[0] = params.v0
    
    # Вычисляем Холецкого для Броуновского движения (да, тут все серьезно)
    for t in range(1, days + 1):
        # Генерим рандомные шумы
        Z1 = np.random.standard_normal(simulations)
        Z2 = np.random.standard_normal(simulations)
        
        # Скрещиваем (корреляция)
        dW1 = Z1 * np.sqrt(dt)
        dW2 = (params.rho * Z1 + np.sqrt(1 - params.rho**2) * Z2) * np.sqrt(dt)
        
        # 1. Обновление дисперсии (v) с использованием метода Эйлера-Маруямы (дифф. уравнения - наше всё)
        v_prev = np.maximum(v[t-1], 0)
        dv = params.kappa * (params.theta - v_prev) * dt + params.sigma_v * np.sqrt(v_prev) * dW2
        v[t] = v_prev + dv
        
        # Защита от NaN'ов: Убедимся, что дисперсия остается строго положительной для расчета цены
        v_curr = np.maximum(v[t], 1e-8)
        
        # 2. Генерация скачков (когда выходит новость про повышение ставки)
        N = np.random.poisson(params.lambda_j * dt)
        
        J = np.zeros(simulations)
        jump_mask = N > 0
        if np.any(jump_mask):
            J[jump_mask] = np.random.normal(
                params.mu_j[jump_mask] * N[jump_mask], 
                params.sigma_j[jump_mask] * np.sqrt(N[jump_mask])
            )
            
        k = np.exp(params.mu_j + 0.5 * params.sigma_j**2) - 1
        
        # 3. Обновление цены (S)
        drift = (params.r - params.q - params.lambda_j * k - 0.5 * v_curr) * dt
        diffusion = np.sqrt(v_curr) * dW1
        
        S[t] = S[t-1] * np.exp(drift + diffusion + J)

    # Расчет статистики по ценам (смотрим, сколько потеряли)
    final_prices = S[-1, :]
    returns = (final_prices - S0) / S0
    
    percentiles = [1, 5, 25, 50, 75, 95, 99]
    calc_pcts = np.percentile(final_prices, percentiles)
    
    # Продвинутые метрики риск-менеджмента (институциональный уровень)
    # Риски: Value at Risk (VaR) 95% для умников
    var_95_return = np.percentile(returns, 5)
    var_95_value = S0 * -var_95_return # скок бабла потеряем
    
    # Маржинколл зона (CVaR - Expected Shortfall)
    # Среднее значение просадок, когда рынок рили летит в тартарары
    cvar_returns = returns[returns <= var_95_return]
    cvar_95_return = np.mean(cvar_returns) if len(cvar_returns) > 0 else var_95_return
    cvar_95_value = S0 * -cvar_95_return
    
    # Вероятность залутать профит (Probability of Profit - PoP)
    prob_profit = np.mean(final_prices > S0) * 100.0

    statistics = {
        "p01_crash": int(round(calc_pcts[0])),
        "worst_case_5th_pct": int(round(calc_pcts[1])),
        "p25_bear": int(round(calc_pcts[2])),
        "median_target": int(round(calc_pcts[3])),
        "p75_bull": int(round(calc_pcts[4])),
        "best_case_95th_pct": int(round(calc_pcts[5])),
        "p99_moon": int(round(calc_pcts[6])),
        "var_95_amount": max(0, float(round(var_95_value, 2))),
        "cvar_95_amount": max(0, float(round(cvar_95_value, 2))),
        "prob_profit": float(round(prob_profit, 2))
    }
    
    # Ищем конкретные индексы для "Выделенных путей" на фронте
    # Чтобы юзер видел прям конкретную линию развития событий, а не просто среднее по больнице
    # 1. Медианный путь (Самый вероятный)
    median_diffs = np.abs(final_prices - calc_pcts[3])
    idx_median = np.argmin(median_diffs)
    
    # 2. 95-й перцентиль (Тузземун, ищем ламбо)
    p95_diffs = np.abs(final_prices - calc_pcts[5])
    idx_p95 = np.argmin(p95_diffs)
    
    # 3. 5-й перцентиль (Ректуха, ликвидация)
    p5_diffs = np.abs(final_prices - calc_pcts[1])
    idx_p5 = np.argmin(p5_diffs)

    # Форматирование данных для Recharts
    chart_data = []
    display_sims = min(simulations, 100)
    
    # Выбираем случайное подмножество нормальных путей, но ГАРАНТИРУЕМ включение выделенных путей
    highlighted_indices = {idx_median, idx_p95, idx_p5}
    
    # Жадный выбор: Исключаем выделенные пути из общего пула во избежание дублей на UI
    remaining_indices = list(set(range(simulations)) - highlighted_indices)
    np.random.shuffle(remaining_indices)
    selected_normal_indices = remaining_indices[:max(0, display_sims - 3)]
    
    for day_index in range(days + 1):
        day_data = {"day": day_index, "date": f"Day {day_index}"}
        
        # Добавляем выделенные конкретные сценарии
        day_data["path_median"] = float(round(float(S[day_index, idx_median]), 2))
        day_data["path_best_95"] = float(round(float(S[day_index, idx_p95]), 2))
        day_data["path_worst_5"] = float(round(float(S[day_index, idx_p5]), 2))
        
        # Добавляем 'серые' фоновые линии (массовка для графика)
        for i, original_sim_idx in enumerate(selected_normal_indices):
            day_data[f"sim_{i}"] = float(round(float(S[day_index, original_sim_idx]), 2))
        
        chart_data.append(day_data)
        
    execution_time = time.time() - start_time
    
    return {
        "status": "success",
        "symbol": symbol,
        "execution_time_ms": round(execution_time * 1000, 2),
        "parameters": {
            "model": "Advanced Bates (StochVol + Jumps + VaR/CVaR)",
            "current_price": S0,
            "days_simulated": days,
            "num_simulations": simulations,
            "displayed_paths": len(selected_normal_indices) + 3
        },
        "statistics": statistics,
        "chart_data": chart_data
    }
