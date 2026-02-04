import asyncio
from utils.web_search import web_search

async def search_async(query):
    return await asyncio.to_thread(web_search,query)

async def parallel_research(sub_queries):
    tasks=[search_async(q) for q in sub_queries]
    results=await asyncio.gather(*tasks)

    docs=[]
    for res in results:
        for r in res:
            docs.append({
                'url':r['url'],
                'content':r['content']
            })
    return docs