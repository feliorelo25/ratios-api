from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "6674e8011398d2a7d1f4bbcf0f9a269c"
BASE_URL = "https://financialmodelingprep.com/api/v3"

@app.get("/ratios/{ticker}")
def get_ratios(ticker: str):
    try:
        url = f"{BASE_URL}/key-metrics-ttm/{ticker.upper()}?apikey={API_KEY}"
        res = requests.get(url)
        data = res.json()

        if not isinstance(data, list) or len(data) == 0:
            return {"error": "Ticker not found or invalid response"}

        d = data[0]

        # Extraer ratios clave
        pe_ratio = d.get("peRatioTTM")
        pb_ratio = d.get("pbRatioTTM")
        ev_ebitda = d.get("enterpriseValueOverEBITDATTM")
        ev_sales = d.get("evToSalesTTM")
        dividend_yield = d.get("dividendYieldTTM") or 0
        buyback_yield = 0  # no disponible
        eps_growth = 0     # no disponible
        pe_change = 0      # no disponible

        expected_return = dividend_yield - (-buyback_yield) + eps_growth + pe_change

        return {
            "ticker": ticker.upper(),
            "peRatio": pe_ratio,
            "pbRatio": pb_ratio,
            "evToEbitda": ev_ebitda,
            "evToSales": ev_sales,
            "dividendYield": dividend_yield,
            "buybackYield": buyback_yield,
            "epsGrowth": eps_growth,
            "peChange": pe_change,
            "expectedReturn": expected_return
        }

    except Exception as e:
        return {"error": str(e)}
