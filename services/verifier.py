import yfinance as yf

MAPPING = {

    "Gold": "GC=F",
    "Silver": "SI=F",
    "Crude Oil": "CL=F",
    "Natural Gas": "NG=F",

    "USDINR": "INR=X",
    "GBPINR": "GBPINR=X",

    "NIFTY": "^NSEI"
}

def verify_market_move(instrument, sentiment):

    symbol = MAPPING.get(instrument)

    if not symbol:

        return {
            "move": "Unknown",
            "correct": False
        }

    try:

        ticker = yf.Ticker(symbol)

        hist = ticker.history(period="2d")

        prev_close = hist["Close"].iloc[-2]
        latest = hist["Close"].iloc[-1]

        change = ((latest - prev_close) / prev_close) * 100

        actual = "Bullish" if change > 0 else "Bearish"

        return {
            "move": round(change, 2),
            "actual_direction": actual,
            "correct": actual == sentiment
        }

    except:

        return {
            "move": "Error",
            "correct": False
        }
