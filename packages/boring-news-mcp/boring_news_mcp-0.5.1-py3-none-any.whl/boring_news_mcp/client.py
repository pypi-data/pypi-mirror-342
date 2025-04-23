"""
Boring News MCP Client implementation
"""

import json
from typing import Any, List, Dict, Optional, Union
from datetime import datetime
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("articles")

# Constants
API_BASE = "https://api.boring-news.fr"
USER_AGENT = "articles-api/1.0"

async def make_request(method: str, endpoint: str, data: dict[str, Any] = None) -> dict[str, Any] | None:
    """Make a request to the API with proper error handling."""
    print(f"Making {method} request to {endpoint}")
    url = f"{API_BASE}{endpoint}"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, params=data, timeout=30.0)
            else:
                response = await client.post(url, headers=headers, json=data, timeout=30.0)
            print(f"Response status: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making request: {str(e)}")
            return None

def format_article(article: dict) -> str:
    """Format an article into a readable string."""
    return f"""
ID: {article.get('id', 'Unknown')}
Title: {article.get('title', 'Unknown')}
Date: {article.get('article_date', 'Unknown')}
Created at: {article.get('created_at', 'Unknown')}
Origin: {article.get('origin', 'Unknown')}
Category: {article.get('category', 'Unknown')}
Section: {article.get('section', 'Unknown')}
URL: {article.get('original_url', 'Unknown')}
Sentiment: {article.get('sentiment', 'Unknown')} (Polarity: {article.get('polarity', 'Unknown')})
Tags: {', '.join(article.get('tags', []))}
People: {', '.join(article.get('people', []))}
Main Ideas: {', '.join(article.get('main_ideas', []))}
"""

@mcp.tool()
async def get_articles_by_date(date: Optional[str] = None, category: Optional[str] = None, tags: Optional[str] = None) -> str:
    """Get articles for a given date.
    Args:
        date: Target date in YYYY-MM-DD format (optional, defaults to today)
        category: Category to filter articles by (optional)
        tags: Comma-separated list of tags to filter articles by (optional)
    """
    print(f"Getting articles for date: {date}, category: {category}, tags: {tags}")
    params = {}
    if date:
        params['date'] = date
    if category:
        params['category'] = category
    if tags:
        params['tags'] = tags
        
    articles = await make_request("GET", "/api/articles", params)
    if not articles:
        return "Unable to fetch articles or no articles found."

    formatted_articles = list(map(format_article, articles))
    return "\n---\n".join(formatted_articles)

@mcp.tool()
async def get_articles_by_person(person: str) -> str:
    """Get articles mentioning a specific person.
    Args:
        person: Name of the person
    """
    print(f"Getting articles mentioning: {person}")
    params = {'person': person}
    articles = await make_request("GET", "/api/articles/by-person", params)
    if not articles:
        return "Unable to fetch articles or no articles found."

    formatted_articles = list(map(format_article, articles))
    return "\n---\n".join(formatted_articles)

@mcp.tool()
async def get_similar_articles(text: str) -> str:
    """Get articles similar to the provided text.
    Args:
        text: Text to find similar articles for
    """
    print(f"Getting articles similar to: {text}")
    data = {'text': text}
    articles = await make_request("POST", "/api/articles/similar", data)
    if not articles:
        return "Unable to fetch similar articles or no articles found."

    # Sort articles by similarity score
    articles.sort(key=lambda x: x.get('similarity', 0), reverse=True)
    
    # Add similarity score to the formatted output
    formatted_articles = []
    for article in articles:
        similarity = article.get('similarity', 0)
        article_text = format_article(article).strip()
        formatted_articles.append(f"Similarity: {similarity:.2f}\n{article_text}")
    
    return "\n---\n".join(formatted_articles)

@mcp.tool()
async def get_article_groups(date: Optional[str] = None) -> str:
    """Get main articles groups for a specific date.
    article groups are groups of articles that are talking about the same subject.
    Args:
        date: Target date in YYYY-MM-DD format (optional, defaults to today)
    """
    print(f"Getting article groups for date: {date}")
    params = {}
    if date:
        params['date'] = date
        
    groups = await make_request("GET", "/api/article-groups", params)
    if not groups:
        return "Unable to fetch article groups or no groups found."

    formatted_groups = []
    for group in groups:
        # Format categories into a readable string
        categories_str = ", ".join([
            f"{cat['name']} ({cat['count']})"
            for cat in group.get('categories', [])
        ])

        formatted_group = f"""
Group ID: {group.get('id')}
Articles: {group.get('articles_count')} articles
Categories: {categories_str}
Summary: {group.get('summary')}
"""
        formatted_groups.append(formatted_group)

    return "\n---\n".join(formatted_groups)

@mcp.tool()
async def get_categories(date: Optional[str] = None) -> str:
    """Get all categories and their article counts for a specific date.
    Args:
        date: Target date in YYYY-MM-DD format (optional, defaults to today)
    """
    print(f"Getting categories for date: {date}")
    params = {}
    if date:
        params['date'] = date
        
    categories = await make_request("GET", "/api/categories", params)
    if not categories:
        return "Unable to fetch categories or no categories found."

    # Group categories by type
    main_categories = []
    culture_categories = []
    tech_science_categories = []
    other_categories = []

    for cat in categories:
        name = cat['name']
        count = cat['count']
        if name.startswith('culture-'):
            culture_categories.append(f"{name}: {count} articles")
        elif name in ['technologie', 'science', 'intelligence artificielle']:
            tech_science_categories.append(f"{name}: {count} articles")
        elif name in ['international', 'politique', 'economie', 'societe', 'sports']:
            main_categories.append(f"{name}: {count} articles")
        else:
            other_categories.append(f"{name}: {count} articles")

    # Format the output
    output = []
    if main_categories:
        output.append("Main Categories:")
        output.extend(main_categories)
        output.append("")
    
    if tech_science_categories:
        output.append("Tech & Science:")
        output.extend(tech_science_categories)
        output.append("")
    
    if culture_categories:
        output.append("Culture Categories:")
        output.extend(culture_categories)
        output.append("")
    
    if other_categories:
        output.append("Other Categories:")
        output.extend(other_categories)

    return "\n".join(output)

@mcp.prompt()
def daily_news(target_date: str) -> str:
    """Generate a daily news summary focused on tech and culture first.
    Args:
        target_date: Target date in YYYY-MM-DD format
    """
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    return f"""
L'objectif est de faire un résumé des actualités de la journée du {target_date},
Utilise la Liste les categories des articles pour la journée pour filtrer les articles.
Un label d'un lien vers un article doit etre affiché le nom de la source.
Fais un résumé des actualités de la journée en organisant les articles dans cette ordre.
1 - Les informations scientifique et relatives à l'IA. 
2 - puis à l'actualisté geek et culture jeux video,cinema,livre 
3 - puis l'actualité francaise puis internationale. 
Pour l'actualité internationale, evoque la guerre en ukraine ou à gaza uniquement s'il y a des elements significatifs
"""

@mcp.prompt()
def daily_news_summary(target_date: str) -> str:
    """Generate a comprehensive daily news summary grouped by themes.
    Args:
        target_date: Target date in YYYY-MM-DD format
    """
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    return f"""
En tant que journaliste experimenté, fais un résumé concis de la journée du {target_date} par categorie qui capture les points principaux abordés par ces articles en regroupant les articles qui parlent d'un même sujet.

Utilise la Liste les categories des articles pour la journée pour regrouper/filter les articles.
Si deux idées sont très proches, tu peux les regrouper. Sinon laisse les en deux idées distinctes.
Un label d'un lien vers un article doit être affiché avec le nom de la source.

Organise le résumé des actualités dans cet ordre:
1. Les informations scientifiques et relatives à l'IA
2. L'actualité geek et culturelle (jeux vidéo, cinéma, livres)
3. L'actualité française puis internationale
   Note: Pour l'actualité internationale, évoque la guerre en Ukraine ou à Gaza uniquement s'il y a des éléments significatifs
"""

@mcp.prompt()
def daily_news_highlights(target_date: str) -> str:
    """Generate a summary of major news highlights of the day.
    Args:
        target_date: Target date in YYYY-MM-DD format
    """
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    return f"""
En tant que journaliste experimenté, donne un résumé concis de la journée du {target_date} par categorie qui capture les points principaux abordés par ces articles en regroupant les articles qui parlent d'un même sujet.

Utilise la Liste les categories des articles pour la journée pour regrouper/filter les articles.
Si deux idées sont très proches, tu peux les regrouper. Sinon laisse les en deux idées distinctes.
Un label d'un lien vers un article doit être affiché avec le nom de la source.

Organise le résumé des actualités dans cet ordre:
1. Les événements majeurs dans le monde
2. Les événements majeurs en France
3. L'actualité culturelle
4. Les événements nationaux ou internationaux significatifs en sport
"""

@mcp.prompt()
def daily_cultural_news(target_date: str) -> str:
    """Generate a summary focused on cultural news of the day.
    Args:
        target_date: Target date in YYYY-MM-DD format
    """
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    return f"""
En tant que journaliste experimenté, donne un résumé concis de la journée du {target_date} qui capture uniquement les points principaux de l'actualité culturelle, en regroupant les articles qui parlent d'un même sujet.

Utilise la Liste les categories des articles pour la journée pour identifier et filtrer les articles culturels (culture-musique, culture-cinema, culture-livres, culture-jeuxvideo, culture-television, culture-theatre, etc.).
Si deux idées sont très proches, tu peux les regrouper. Sinon laisse les en deux idées distinctes.
Un label d'un lien vers un article doit être affiché avec le nom de la source.

Focus exclusif sur l'actualité culturelle:
- Nouveautés et événements dans le monde du cinéma
- Actualités littéraires et éditoriales
- Actualités musicales et concerts
- Actualités des jeux vidéo
- Actualités du théâtre et du spectacle vivant
- Actualités télévision et streaming
""" 