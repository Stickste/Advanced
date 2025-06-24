import json
from datetime import datetime

def log_decision(ticker, input_data, decision):
    with open(f"log_{datetime.now().date()}.json", "a") as f:
        f.write(json.dumps({"ticker": ticker, "decision": decision, "data": input_data}, indent=2))
        f.write(",\n")