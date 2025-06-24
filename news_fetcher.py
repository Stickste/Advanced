#from dotenv import load_dotenv
#load_dotenv()

import requests
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

analyzer = SentimentIntensityAnalyzer()

def fetch_stock_news(ticker):
    url = f"https://newsapi.org/v2/everything?q={ticker}&language=en&apiKey={NEWS_API_KEY}&sortBy=relevancy&pageSize=5"

    res = requests.get(url)
    articles = res.json().get("articles", [])

    results = []
    for a in articles:
        title = a.get("title", "")
        description = a.get("description", "")
        source = a.get("source", {}).get("name", "")
        published_at = a.get("publishedAt", "")
        combined_text = f"{title} {description}"
        sentiment_score = analyzer.polarity_scores(combined_text)["compound"]
        results.append({
            "title": title,
            "description": description,
            "source": source,
            "published_at": published_at,
            "sentiment": sentiment_score
        })

    return results
def fetch_macro_news():
    query = "geopolitical OR inflation OR interest rates OR central bank OR war OR recession"
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}&sortBy=relevancy&pageSize=5"
    res = requests.get(url)
    articles = res.json().get("articles", [])

    results = []
    for a in articles:
        title = a.get("title", "")
        description = a.get("description", "") or ""
        source = a.get("source", {}).get("name", "")
        published_at = a.get("publishedAt", "")
        combined_text = f"{title} {description}".strip()
        sentiment_score = analyzer.polarity_scores(combined_text)["compound"] if combined_text else None
        results.append({
            "title": title,
            "description": description,
            "source": source,
            "published_at": published_at,
            "sentiment": round(sentiment_score, 2)
        })

    return results



if __name__ == "__main__":
    print(fetch_stock_news("TSLA"))
    print("\nMacro news:")
    print(fetch_macro_news())