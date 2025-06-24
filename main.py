print("DEBUG-KEYS:")
print("NEWS_API_KEY:", os.getenv("NEWS_API_KEY"))
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
print("REDDIT_CLIENT_ID:", os.getenv("REDDIT_CLIENT_ID"))
print("ALPACA_API_KEY:", os.getenv("ALPACA_API_KEY"))


import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#from dotenv import load_dotenv
#load_dotenv()

import time

from sp500 import fetch_sp500_tickers
from stock_data import get_stock_metrics
from news_fetcher import fetch_stock_news, fetch_macro_news
from gpt_decider import decide_with_gpt
from trade_executor import get_held_stocks, sell_stock, execute_trade
from reddit_sentiment import get_reddit_sentiment
#from data import data


def main():

    # Schritt 0: Bestehende Positionen verkaufen
    helden = get_held_stocks()
    print("Gehaltene Aktien:", helden)

    for ticker in helden:
        try:
            sell_stock(ticker)
            print(f"Verkauft: {ticker}")
        except Exception as e:
            print(f"Verkauf fehlgeschlagen für {ticker}: {e}")

    # Schritt 1: Ticker laden und analysieren
    tickers = fetch_sp500_tickers()
    
    macro = fetch_macro_news()

    stock_data = []
    for ticker in tickers:
        try:
            metrics = get_stock_metrics(ticker)
            print(ticker)
            stock_data.append((ticker, metrics))
        except Exception as e:
            print(f"{ticker} failed: {e}")

    #stock_data = list(data.items())

    # Schritt 2: Nach Gruppen priorisieren
    sorted_data = sorted(stock_data, key=lambda x: x[1]["group"])

    buy_recommendations = []
    batch_size = 10
    index = 0

    # Schritt 3: In Batches durchgehen und analysieren
    while index < len(sorted_data) and len(buy_recommendations) < 3:
        batch = sorted_data[index:index + batch_size]
        print(f"\nAnalysiere Batch {index // batch_size + 1}...")

        news_results = {}
        for ticker, _ in batch:
            try:
                stock_news = fetch_stock_news(ticker)
                reddit_posts = get_reddit_sentiment(ticker)
                reddit_text = "\n".join([f"- {post['title']} (r/{post['subreddit']})" for post in reddit_posts])
                news_results[ticker] = f"MACRO NEWS:\n{macro}\n\nSTOCK NEWS:\n{stock_news}\n\nREDDIT:\n{reddit_text}"
            except Exception as e:
                print(f"News/Reddit fetch failed for {ticker}: {e}")
                news_results[ticker] = f"MACRO NEWS:\n{macro}"

        for ticker, metrics in batch:
            if len(buy_recommendations) >= 3:
                break

            news_text = news_results.get(ticker, "")
            decision = decide_with_gpt(ticker, metrics, news_text)
            if decision.lower() == "buy":
                print(f"GPT empfiehlt Kauf von {ticker}")
                buy_recommendations.append(ticker)
            else:
                print(f"GPT empfiehlt Kauf von {ticker} nicht")

        index += batch_size

    # Schritt 4: Trades ausführen
    for ticker in buy_recommendations:
        try:
            execute_trade(ticker, action="buy")
            print(f"Gekauft: {ticker}")
        except Exception as e:
            print(f"Trade fehlgeschlagen für {ticker}: {e}")


if __name__ == "__main__":
    main()
