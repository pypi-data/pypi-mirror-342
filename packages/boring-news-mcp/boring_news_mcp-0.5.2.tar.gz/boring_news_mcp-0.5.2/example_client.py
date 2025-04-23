import asyncio
import json
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="/Users/olivier/.local/bin/uv",  # Executable
    args=[
        "--directory",
        "/Users/olivier/Dev/boring-news/boring-news-mcp/src/",
        "run", 
        "-m", "boring_news_mcp"
    ],  # Server script
    # command="/Users/olivier/.local/bin/uv",  # Executable
    # args=[
    #         "--directory",
    #         "/Users/olivier/python",
    #         "run",
    #         "-m", "boring_news_mcp"
    # ],  # Server script
    env=None,  # Optional environment variables
)

async def get_similar_articles(text: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            articles = await session.call_tool("get_similar_articles", arguments={"text": text})
            for article in articles.content:
                print(article.text)

async def get_articles_by_date(date: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
    
            # Get articles by date
            articles = await session.call_tool(
                "get_articles_by_date", 
                arguments={
                    "date": date,
                    # category": "science",
                    # "tags": "AI,technology"
                }
            )
            print("\nFiltered articles:")
            print(articles.content)
            for article in articles.content:
                print(article.text)
    
async def get_articles_by_tags(tags: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
    
            # Get articles by tags
            articles = await session.call_tool(
                "get_articles_by_date", 
                arguments={
                    "date": "2025-04-16",
                    # category": "science",
                    "tags": tags
                }
            )
            print("\nFiltered articles:")
            print(articles.content)
            for article in articles.content:
                print(article.text)
async def get_article_groups(date: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            article_groups = await session.call_tool("get_article_groups", arguments={"date": date})
            for group in article_groups.content:
                print(group.text)
            #  print("Available article groups:", article_groups)

async def get_tools():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            tools = await session.list_tools()
            print("Available tools:", tools)

async def get_categories():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            categories = await session.call_tool("get_categories", arguments={"date": '2025-04-16'})
            print("Available categories:", categories)

async def run():
    await get_tools()
    # await get_articles_by_date("2025-04-16")
    #await get_articles_by_tags("aston villa")
    #await get_article_groups("2025-04-16")
    #await get_categories()
    await get_similar_articles("aston villa")

            

if __name__ == "__main__":
    asyncio.run(run()) 