import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands
from finvizfinance.quote import finvizfinance
from sp500 import fetch_sp500_tickers

#def get_short_interest(ticker):
#    try:
#        stock = finvizfinance(ticker)
#        data = stock.ticker_fundament()
#        short_val = data.get("Short Float", "N/A")
#        return short_val
#    except Exception:
#        return "N/A"


def get_stock_metrics(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="60d")
    df.dropna(inplace=True)

    # RSI
    rsi = RSIIndicator(close=df["Close"])
    df["RSI"] = rsi.rsi()

    # MACD
    macd = MACD(close=df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_signal"] = macd.macd_signal()
    df["MACD_hist"] = macd.macd_diff()

    # ATR
    atr = df["High"].rolling(14).max().iloc[-1] - df["Low"].rolling(14).min().iloc[-1]

    # Bollinger Bands
    bb = BollingerBands(close=df["Close"])
    df["BB_upper"] = bb.bollinger_hband()
    df["BB_lower"] = bb.bollinger_lband()
    df["BB_bandwidth"] = df["BB_upper"] - df["BB_lower"]

    latest = df.iloc[-1]
    macd_signal = df["MACD_signal"].iloc[-1]
    macd_rising_above = (
        df["MACD"].iloc[-1] > df["MACD_signal"].iloc[-1]
        and df["MACD_hist"].iloc[-1] > df["MACD_hist"].iloc[-2]
    )
    rsi_ok = 45 <= df["RSI"].iloc[-1] <= 65
    atr_ok = atr > df["Close"].mean() * 0.01
    touch_lower = latest["Close"] <= latest["BB_lower"]
    squeeze = latest["BB_bandwidth"] < df["BB_bandwidth"].rolling(20).mean().iloc[-1] * 0.7

    # Sounds good, doesn't work
    
    #short_ok = False
    #short_interest_str = get_short_interest(ticker)
    #try:
    #    short_val = float(short_interest_str.replace('%', ''))
    #    short_ok = short_val > 10
    #except:
    #    short_val = None

    short_val=None
    short_ok=False

    # Gruppenzuordnung
    group = 5  # Standardgruppe
    if rsi_ok and macd_rising_above and atr_ok and touch_lower and short_ok:
        group = 1
    elif rsi_ok and macd_rising_above and atr_ok and touch_lower:
        group = 2
    elif rsi_ok and macd_rising_above and touch_lower:
        group = 3
    elif rsi_ok and macd_rising_above:
        group = 4

    beta = stock.info.get("beta", 1.0)
    try:
        earnings_date = stock.calendar.index[0].strftime("%Y-%m-%d")
    except Exception:
        earnings_date = None

    result = {
        "rsi": round(df["RSI"].iloc[-1], 2),
        "macd": round(df["MACD"].iloc[-1], 2),
        "macd_rising_above": macd_rising_above,
        "atr": round(atr, 2),
        "beta": beta,
        "group": group,
    }

#    if short_ok:
#        result["short_interest"] = short_interest_str
    if earnings_date:
        result["earnings"] = earnings_date

    print(ticker)

    return result

if __name__ == "__main__":
    tickers = fetch_sp500_tickers()
    
    print(len(tickers), "Tickers geladen.")

    results = {}
    for ticker in tickers:
        try:
            metrics = get_stock_metrics(ticker)
            
            results[ticker] = metrics
        except Exception as e:
            print(f"{ticker} failed: {e}")

    # Speichern in data.py
    with open("data.py", "w", encoding="utf-8") as f:
        f.write("# Auto-generierte Datei mit Ticker-Metriken\n")
        f.write("data = {\n")
        for ticker, metrics in results.items():
            f.write(f"    {repr(ticker)}: {repr(metrics)},\n")
        f.write("}\n")