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
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
    except Exception:
        return {"error": "Failed to fetch data"}

    # Valores con fallback
    price = info.get("currentPrice")
    eps = info.get("trailingEps")
    pe_ratio = info.get("trailingPE")
    ebitda = info.get("ebitda")
    market_cap = info.get("marketCap")
    total_debt = info.get("totalDebt", 0)
    cash = info.get("totalCash", 0)
    net_income = info.get("netIncome")
    book_value = info.get("bookValue")
    dividend_yield = info.get("dividendYield") or 0
    buyback_yield = info.get("buybackYield") or 0
    eps_growth = info.get("earningsQuarterlyGrowth") or 0
    pe_change = 0

    enterprise_value = (
        market_cap + total_debt - cash
        if market_cap is not None else None
    )
    ev_ebitda = (
        enterprise_value / ebitda
        if enterprise_value is not None and ebitda else None
    )
    expected_return = (
        dividend_yield - (-buyback_yield)
        + eps_growth + pe_change
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
        "expectedReturn": expected_return
    }
