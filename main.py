from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

@app.get("/ratios/{ticker}")
def get_ratios(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info

    price = info.get("currentPrice")
    eps = info.get("trailingEps")
    pe_ratio = info.get("trailingPE")
    ebitda = info.get("ebitda")
    market_cap = info.get("marketCap")
    total_debt = info.get("totalDebt")
    cash = info.get("totalCash")
    net_income = info.get("netIncome")
    book_value = info.get("bookValue")
    dividend_yield = info.get("dividendYield")
    buyback_yield = info.get("buybackYield") or 0
    eps_growth = info.get("earningsQuarterlyGrowth") or 0
    pe_change = 0  # default; podrías obtener estimado

    enterprise_value = (market_cap + total_debt - cash
                        if market_cap and total_debt is not None and cash is not None else None)
    ev_ebitda = (enterprise_value / ebitda if enterprise_value and ebitda else None)
    expected_return = (dividend_yield - (-buyback_yield)
                       + eps_growth + pe_change)

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
