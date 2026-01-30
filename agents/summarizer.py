from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm=ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0
)

def summarizer(text):
    prompt=f"""
Summarize the following research content concisely.Preserve facts,remove fluff.

TEXT:
{text}
"""
    
    return llm.invoke(prompt).content