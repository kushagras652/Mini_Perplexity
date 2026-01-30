from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm=ChatOpenAI(model='gpt-4.1',temperature=0)

def synthesize(summary):
    return llm.invoke(f'Produce final structured answer with citations:\n{summary}').content