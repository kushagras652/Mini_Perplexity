from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm=ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0
)

SYSTEM_PROMPT = """
You are a grounded research synthesizer.

RULES:
- Use ONLY the provided sources.
- Every factual claim MUST have a citation.
- If sources are insufficient, say: "Insufficient evidence."
- Do NOT use external knowledge.
- Do NOT invent facts or URLs.

Format citations as [1], [2], etc.
"""

def grounded_synthesize(summary,sources):
    sources_text=""
    for i,src in enumerate(sources,1):
        sources_text+=f"[{i}]{src['url']}\n{src['content']}\n\n"

    prompt = f"""
{SYSTEM_PROMPT}

SOURCES:
{sources_text}

SUMMARY:
{summary}

Produce a grounded answer with citations.
"""
    
    return llm.invoke(prompt).content