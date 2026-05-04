import requests
import os
from datetime import datetime, timedelta
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()


def fetch_stock_news(company_name: str, ticker: str, api_key: str, max_articles: int = 10) -> List[Dict]:
    """Fetch latest news articles about a stock using NewsAPI."""
    try:
        # Search with both company name and ticker
        query = f"{company_name} OR {ticker} stock"
        from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "from": from_date,
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": max_articles,
            "apiKey": api_key,
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") != "ok":
            return []

        articles = []
        for article in data.get("articles", []):
            if article.get("title") and article.get("description"):
                articles.append({
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "content": article.get("content", ""),
                    "url": article.get("url", ""),
                    "published_at": article.get("publishedAt", ""),
                    "source": article.get("source", {}).get("name", "Unknown"),
                })

        return articles

    except Exception as e:
        print(f"Error fetching news: {e}")
        return []


def format_news_for_display(articles: List[Dict]) -> List[Dict]:
    """Format news articles for Streamlit display."""
    formatted = []
    for article in articles:
        pub_date = article.get("published_at", "")
        try:
            dt = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
            formatted_date = dt.strftime("%b %d, %Y %H:%M")
        except:
            formatted_date = pub_date

        formatted.append({
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "url": article.get("url", ""),
            "source": article.get("source", ""),
            "date": formatted_date,
        })
    return formatted


def format_news_for_llm(articles: List[Dict]) -> str:
    """Format news articles as context string for LLM."""
    if not articles:
        return "No recent news articles found for this stock."

    context = f"LATEST NEWS (Last 7 days) - Retrieved on {datetime.now().strftime('%Y-%m-%d %H:%M')}:\n\n"

    for i, article in enumerate(articles[:8], 1):
        pub_date = article.get("published_at", "")
        try:
            dt = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
            formatted_date = dt.strftime("%b %d, %Y")
        except:
            formatted_date = pub_date

        context += f"""Article {i}: [{article.get('source', 'Unknown')} - {formatted_date}]
Title: {article.get('title', '')}
Summary: {article.get('description', '')}
{('Content: ' + article.get('content', '')[:300] + '...') if article.get('content') else ''}

"""

    return context