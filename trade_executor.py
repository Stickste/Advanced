from dotenv import load_dotenv
load_dotenv()

import alpaca_trade_api as tradeapi
import os

api = tradeapi.REST(
    os.getenv("ALPACA_API_KEY"),
    os.getenv("ALPACA_SECRET_KEY"),
    base_url="https://paper-api.alpaca.markets"
)

def execute_trade(ticker):
    api.submit_order(
        symbol=ticker,
        qty=1,
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
