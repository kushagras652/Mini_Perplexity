from typing import TypedDict,List

class ResearchState(TypedDict):
    query:str
    sub_queries:List[str]
    docs:List[dict]
    summary:str
    answer:str
