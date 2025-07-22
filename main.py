from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ratios/{ticker}")
def get_ratios(ticker: str):
    stock = yf.Ticker(ticker)
    try:
        info = stock.info
    except Exception:
        return {"error": "Failed to fetch data"}

    # Valores financieros (con fallbacks y chequeo)
    price = info.get("currentPrice")
    eps = info.get("trailingEps")
    pe_ratio = info.get("trailingPE")
    ebitda = info.get("ebitda")
    market_cap = info.get("marketCap")
    total_debt = info.get("totalDebt", 0)
    cash = info.get("totalCash", 0)
    net_income = info.get("netIncome")
    book_value = info.get("bookValue")
    dividend_yield = info.get("dividendYield")
    buyback_yield = info.get("buybackYield") or 0
    eps_growth = info.get("earningsQuarterlyGrowth") or 0
    pe_change = 0  # se mantiene como input manual

    # EV y múltiplos (protegidos)
    enterprise_value = (
        market_cap + total_debt - cash
        if market_cap is not None and total_debt is not None and cash is not None
        else None
    )
    ev_ebitda = enterprise_value / ebitda if enterprise_value and ebitda else None

    # Retorno esperado (con fallback a None si falta lo esencial)
    expected_return = (
        (dividend_yield if dividend_yield is not None else 0)
        - (-buyback_yield)
        + (eps_growth if eps_growth is not None else 0)
        + pe_change
    )

    return {
        "ticker": ticker,
        "stockPrice": price,
        "eps": eps,
        "peRatio": pe_ratio,
        "marketCap": market_cap,
        "totalDebt": total_debt,
        "cash": cash,
        "ebitda": ebitda,
        "enterpriseValue": enterprise_value,
        "evEbitda": ev_ebitda,
        "bookValue": book_value,
        "netIncome": net_income,
        "dividendYield": dividend_yield,
        "buybackYield": buyback_yield,
        "epsGrowth": eps_growth,
        "peChange": pe_change,
        "expectedReturn": expected_return,
    }
