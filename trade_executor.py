#from dotenv import load_dotenv
#load_dotenv()

import alpaca_trade_api as tradeapi
import os

api = tradeapi.REST(
    os.getenv("ALPACA_API_KEY"),
    os.getenv("ALPACA_SECRET_KEY"),
    base_url="https://paper-api.alpaca.markets"
)

def execute_trade(ticker):
    # Schritt 1: Kontostand abrufen
    account = api.get_account()
    cash = float(account.cash)
    budget = cash / 3  # Ein Drittel des verfügbaren Bargelds

    # Schritt 2: Preis der Aktie abrufen
    last_trade = api.get_latest_trade(ticker)
    price = float(last_trade.price)

    # Schritt 3: Stückzahl berechnen (ganzzahlig)
    qty = int(budget // price)
    if qty < 1:
        print(f"Nicht genug Budget für {ticker}, Preis: {price:.2f}, Budget: {budget:.2f}")
        return

    # Schritt 4: Order ausführen
    api.submit_order(
        symbol=ticker,
        qty=qty,
        side="buy",
        type="market",
        time_in_force="day"
    )


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
    print("Gehaltene Aktien:", get_held_stocks())
