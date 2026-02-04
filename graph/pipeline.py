from langgraph.graph import StateGraph
from graph.state import ResearchState
from agents.planner import plan_query
from agents.research import research
from agents.summarizer import summarizer
from agents.synthesizer import synthesize
from vector_db.faiss_store import VectorDB
from agents.researcher_async import parallel_research
import asyncio
from agents.grounded_sunthesizer import grounded_synthesize
from agents.evidence_checker import verify

db = VectorDB()

def planner_node(state):
    state["sub_queries"] = plan_query(state["query"])
    return state

def researcher_node(state):
    # state["docs"] = research(state["sub_queries"])
    # return state
    sub_queries=state['sub_queries'][:3]
    docs=asyncio.run(parallel_research(sub_queries))
    state['docs']=docs
    return state

def summarizer_node(state):
    state["summary"] = summarizer(state["docs"])
    db.add(state["summary"], {"query": state["query"]})
    return state

def synthesizer_node(state):
    # state["answer"] = synthesize(state["summary"])
    # return state

    answer=grounded_synthesize(
        summary=state['summary'],
        sources=state['docs']
    )

    verdict=verify(answer,state['docs'])

    if verdict['verdict']=='VALID':
        state['answer']=answer
        return state
    
    repair_prompt=f"""
The following answer has issues:
{verdict['issues']}

Rewrite the answer strictly using the sources.
If not possible, say "Insufficient evidence."
"""
    
    repaired_answer=grounded_synthesize(
        summary=state['summary']+"\n"+repair_prompt,
        sources=state['docs']
    )

    state['answer']=repaired_answer
    return state

graph = StateGraph(ResearchState)

graph.add_node("planner", planner_node)
graph.add_node("researcher", researcher_node)
graph.add_node("summarizer", summarizer_node)
graph.add_node("synthesizer", synthesizer_node)

graph.set_entry_point("planner")
graph.add_edge("planner", "researcher")
graph.add_edge("researcher", "summarizer")
graph.add_edge("summarizer", "synthesizer")

pipeline = graph.compile()
