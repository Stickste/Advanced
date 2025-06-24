#from dotenv import load_dotenv
#load_dotenv()

from openai import OpenAI
import os

client = OpenAI()

def decide_with_gpt(ticker, metrics, news_text):
    prompt = f"""Bewerte, ob folgende Aktie für einen Kauf heute, bei Markeröffnung geeignet ist um sie wieder kurz vor Marktschluss zu verkaufen:
Ticker: {ticker}
Technische Daten: {metrics}
Nachrichtenlage: {news_text}

Antwort bitte nur mit "Buy" oder "Pass".
"""
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    print("Test")