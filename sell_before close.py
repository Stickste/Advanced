from alpaca_trade_api import REST
import os

#from dotenv import load_dotenv
#load_dotenv()

api = REST(
    os.getenv("ALPACA_API_KEY"),
    os.getenv("ALPACA_SECRET_KEY"),
    base_url="https://paper-api.alpaca.markets"
)

positions = api.list_positions()
for position in positions:
    api.submit_order(
        symbol=position.symbol,
        qty=position.qty,
        side="sell",
        type="market",
        time_in_force="day"
    )

print("✅ Sold all positions before close.")