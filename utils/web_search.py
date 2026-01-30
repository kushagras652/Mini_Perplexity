import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client=TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

def web_search(query,k=5):
    results=client.search(query=query,max_results=k)
    return results['results']