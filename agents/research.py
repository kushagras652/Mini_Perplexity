from utils.web_search import web_search

def research(sub_queries):
    docs=[]

    for q in sub_queries:
        results=web_search(q)
        for r in results:
            docs.append({
                'url':r['url'],
                'content':r['content']
            })
    return docs