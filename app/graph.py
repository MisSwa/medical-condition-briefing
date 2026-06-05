from langgraph.graph import END, START, StateGraph

from app.nodes import format_output, query_clinicaltrials, query_pubmed, synthesize_brief
from app.state import BriefingState

_builder = StateGraph(BriefingState)

_builder.add_node("query_pubmed", query_pubmed)
_builder.add_node("query_clinicaltrials", query_clinicaltrials)
_builder.add_node("synthesize_brief", synthesize_brief)
_builder.add_node("format_output", format_output)

# Parallel fan-out: both retrieval nodes start from START
_builder.add_edge(START, "query_pubmed")
_builder.add_edge(START, "query_clinicaltrials")

# Fan-in: both retrieval nodes converge on synthesis
_builder.add_edge("query_pubmed", "synthesize_brief")
_builder.add_edge("query_clinicaltrials", "synthesize_brief")

# Sequential continuation
_builder.add_edge("synthesize_brief", "format_output")
_builder.add_edge("format_output", END)

briefing_graph = _builder.compile()

if __name__ == "__main__":
    initial_state: BriefingState = {
        "condition": "asthma",
        "pubmed_results": [],
        "trial_results": [],
        "brief": {},
    }
    result = briefing_graph.invoke(initial_state)
    print(result)
