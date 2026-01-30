from langchain_openai import ChatOpenAI
import json
from dotenv import load_dotenv


load_dotenv()


llm=ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0 
)

SYSTEM_PROMPT = """
You are a research planning agent.
Decompose the user query into 3 precise research sub-queries.
Return ONLY valid JSON list of strings.
No explanations.
"""

def plan_query(user_query:str):
    prompt=f"{SYSTEM_PROMPT}\nUser query:{user_query}"
    response=llm.invoke(prompt).content

    try:
        return json.loads(response)
    except:
        return [user_query]