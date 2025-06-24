from dotenv import load_dotenv
load_dotenv()

import alpaca_trade_api as tradeapi

import os

api = tradeapi.REST(
    os.getenv("ALPACA_API_KEY"),
    os.getenv("ALPACA_SECRET_KEY"),
    base_url="https://paper-api.alpaca.markets",
    api_version="v2"
)

def execute_trade(ticker):
    try:
        account = api.get_account()
        cash = float(account.cash)
        budget = cash / 3

        try:
            quote = api.get_latest_quote(ticker)
            price = float(quote.ask_price)
            if price <= 0:
                raise ValueError("Ungültiger Preis")
        except Exception:
            price = 1000.0  # Fallback-Wert
            print(f"[{ticker}] ⚠️ Kein valider Preis – Fallback auf $1000")

        qty = int(budget // price)
        if qty < 1:
            print(f"[{ticker}] Nicht genug Budget: Preis={price:.2f}, Budget={budget:.2f}")
            return

        api.submit_order(
            symbol=ticker,
            qty=qty,
            side="buy",
            type="market",
            time_in_force="day"
        )
        print(f"[{ticker}] ✅ Kaufauftrag platziert: {qty} @ {price:.2f}")

    except Exception as e:
        print(f"[{ticker}] ❌ Trade fehlgeschlagen: {e}")



def sell_stock(ticker):
    api.submit_order(
        symbol=ticker,
        qty=1,
        side="sell",
        type="market",
        time_in_force="day"
    )

def get_held_stocks():
    positions = api.list_positions()
    return [position.symbol for position in positions]

if __name__ == "__main__":
    execute_trade("TSLA")
    print(get_held_stocks())
