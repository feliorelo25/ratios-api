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
    info = stock.info

    pe_ratio = info.get("trailingPE")
    ebitda = info.get("ebitda")
    market_cap = info.get("marketCap")
    total_debt = info.get("totalDebt")
    cash = info.get("totalCash")
    price = info.get("currentPrice")
    eps = info.get("trailingEps")

    enterprise_value = (
        market_cap + total_debt - cash if market_cap and total_debt and cash else None
    )
    ev_ebitda = enterprise_value / ebitda if enterprise_value and ebitda else None

    return {
        "ticker": ticker,
        "stockPrice": price,
        "eps": eps,
        "peRatio": pe_ratio,
        "marketCap": market_cap,
        "totalDebt": total_debt,
        "cash": cash,
        "ebitda": ebitda,
        "evEbitda": ev_ebitda,
    }
