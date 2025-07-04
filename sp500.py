import pandas as pd
import requests
import random

def fetch_sp500_tickers() -> list[str]:
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    df = pd.read_html(requests.get(url).text)[0]
    tickers = df['Symbol'].str.replace('.', '-', regex=False).tolist()
    random.shuffle(tickers)
    return tickers

if __name__ == "__main__":
    tickers = fetch_sp500_tickers()
    print(len(tickers), "Tickers geladen.")

