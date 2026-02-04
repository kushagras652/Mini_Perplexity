from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",  # cheap verifier
    temperature=0
)

SYSTEM_PROMPT = """
You are an evidence verification agent.

TASK:
- Check if every claim in the answer is supported by the sources.
- Identify unsupported or weakly supported claims.

Return STRICT JSON:
{
  "verdict": "VALID" or "INVALID",
  "issues": ["list of problems"]
}
"""

def verify(answer, sources):
    sources_text = "\n".join([f"{s['content']} ({s['url']})" for s in sources])

    prompt = f"""
{SYSTEM_PROMPT}

ANSWER:
{answer}

SOURCES:
{sources_text}
"""

    response = llm.invoke(prompt).content

    try:
        return json.loads(response)
    except:
        return {"verdict": "INVALID", "issues": ["Failed to parse verifier output"]}
