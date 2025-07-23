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
        url = f"{BASE_URL}/ratios-ttm/{ticker.upper()}?apikey={API_KEY}"
        res = requests.get(url)
        data = res.json()

        if not isinstance(data, list) or len(data) == 0:
            return {"error": "Ticker not found or invalid response"}

        d = data[0]

        # Datos del modelo Grinold-Kroner (asumimos todos en TTM)
        dividend_yield = d.get("dividendYielTTM") or 0
        buyback_yield = d.get("buyBackYieldTTM") or 0  # si está disponible
        eps_growth = d.get("epsGrowthTTM") or 0
        pe_change = 0  # no lo reporta la API, lo mantenemos manual

        expected_return = (
            dividend_yield - (-buyback_yield)
            + eps_growth + pe_change
        )

        return {
            "ticker": d.get("symbol"),
            "date": d.get("date"),
            "peRatio": d.get("peRatioTTM"),
            "pbRatio": d.get("pbRatioTTM"),
            "evToEbitda": d.get("evToEbitdaTTM"),
            "evToSales": d.get("evToSalesTTM"),
            "dividendYield": dividend_yield,
            "buybackYield": buyback_yield,
            "epsGrowth": eps_growth,
            "peChange": pe_change,
            "expectedReturn": expected_return
        }

    except Exception as e:
        return {"error": str(e)}
