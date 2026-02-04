from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json

load_dotenv()

llm=ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0
)

SYSTEM_PROMPT = """
You are a research critic agent.

TASK:
Evaluate the answer quality and completeness.

Identify:
- Missing important subtopics
- Weak or shallow explanations
- Areas needing more evidence

Return STRICT JSON:
{
  "needs_followup": true/false,
  "followup_queries": ["query1", "query2"]
}

Rules:
- Max 2 follow-up queries
- Only suggest queries if they materially improve the answer
"""


def critique(answer:str):
    response=llm.invoke(f"{SYSTEM_PROMPT}\nANSWER:\n{answer}").content

    try:
        return json.loads(response)
    except:
        return {"needs_followup":False,'following_queries':[]}
    
