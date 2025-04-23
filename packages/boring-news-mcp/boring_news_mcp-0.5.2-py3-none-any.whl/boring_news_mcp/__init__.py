"""
Boring News MCP Client - A client library for interacting with the Boring News API
"""

__version__ = "0.1.0"

from .client import (
    get_articles_by_date,
    get_articles_by_person,
    get_similar_articles,
    get_article_groups,
    get_categories,
    daily_news,
    daily_news_summary,
    daily_news_highlights,
    daily_cultural_news
) 