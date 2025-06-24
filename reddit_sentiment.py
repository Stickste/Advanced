from dotenv import load_dotenv
load_dotenv()

import praw
import os

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="overnight-bot"
)

def get_reddit_sentiment(ticker):
    posts = []
    subreddits = ["stocks", "wallstreetbets", "investing", "options", "SecurityAnalysis"]

    for sub in subreddits:
        for submission in reddit.subreddit(sub).hot(limit=10):
            if ticker.upper() in submission.title.upper():
                posts.append({
                    "title": submission.title,
                    "score": submission.score,
                    "subreddit": sub
                })

    # Sort by score and return top 3
    top_posts = sorted(posts, key=lambda x: x["score"], reverse=True)[:3]
    return top_posts

if __name__ == "__main__":
    from pprint import pprint
    pprint(get_reddit_sentiment("TSLA"))