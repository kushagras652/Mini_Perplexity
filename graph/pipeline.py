from langgraph.graph import StateGraph
from graph.state import ResearchState
from agents.planner import plan_query
from agents.research import research
from agents.summarizer import summarizer
from agents.synthesizer import synthesize
from vector_db.faiss_store import VectorDB

db = VectorDB()

def planner_node(state):
    state["sub_queries"] = plan_query(state["query"])
    return state

def researcher_node(state):
    state["docs"] = research(state["sub_queries"])
    return state

def summarizer_node(state):
    state["summary"] = summarizer(state["docs"])
    db.add(state["summary"], {"query": state["query"]})
    return state

def synthesizer_node(state):
    state["answer"] = synthesize(state["summary"])
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
