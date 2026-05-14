import yfinance as yf

def verify_prediction(instrument, sentiment):

    mapping = {
        "Gold": "GC=F",
        "Silver": "SI=F",
        "Crude Oil": "CL=F",
        "Natural Gas": "NG=F",
        "USDINR": "INR=X",
        "GBPINR": "GBPINR=X",
        "NIFTY": "^NSEI"
    }

    ticker_symbol = mapping.get(instrument)

    if not ticker_symbol:
        return {
            "actual_move": "Unknown",
            "result": "N/A"
        }

    try:

        ticker = yf.Ticker(ticker_symbol)

        hist = ticker.history(period="2d")

        if len(hist) < 2:
            raise Exception("Insufficient data")

        previous = hist["Close"].iloc[-2]
        latest = hist["Close"].iloc[-1]

        pct_change = ((latest - previous) / previous) * 100

        actual_direction = "Bullish" if pct_change > 0 else "Bearish"

        correct = actual_direction == sentiment

        return {
            "actual_move": round(pct_change, 2),
            "actual_direction": actual_direction,
            "prediction_correct": correct
        }

    except Exception as e:

        return {
            "actual_move": "Error",
            "actual_direction": str(e),
            "prediction_correct": False
        }
