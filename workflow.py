# Workflow using modular nodes
from langgraph.graph import StateGraph, END
from state import DebateState, create_initial_state
from nodes.rounds_controller import validate_round, should_continue, route_to_speaker
from nodes.agent_node import agent_a_turn, agent_b_turn
from nodes.judge_node import judge_debate
from nodes.logger_node import log_event


def create_debate_workflow():
    try:
        workflow = StateGraph(DebateState)
        
        # Add nodes using modular functions
        workflow.add_node("validate", validate_round)
        workflow.add_node("agent_a", agent_a_turn)
        workflow.add_node("agent_b", agent_b_turn)
        workflow.add_node("judge", judge_debate)
        
        # Set entry point
        workflow.set_entry_point("validate")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "validate",
            should_continue,
            {
                "continue": "route_speaker",
                "judge": "judge"
            }
        )
        
        # Add routing node
        workflow.add_node("route_speaker", lambda state: state)
        workflow.add_conditional_edges(
            "route_speaker",
            route_to_speaker,
            {
                "agent_a": "agent_a",
                "agent_b": "agent_b"
            }
        )
        
        # Add edges back to validation
        workflow.add_edge("agent_a", "validate")
        workflow.add_edge("agent_b", "validate")
        workflow.add_edge("judge", END)
        
        log_event("workflow_created", {"status": "success"})
        
        return workflow.compile()
        
    except Exception as e:
        log_event("workflow_creation_error", {"error": str(e)})
        raise


def run_debate(topic: str) -> DebateState:
    try:
        log_event("debate_start", {"topic": topic})
        
        app = create_debate_workflow()
        initial_state = create_initial_state(topic)
        
        # Invoke with increased recursion limit
        final_state = app.invoke(
            initial_state,
            config={"recursion_limit": 50}
        )
        
        log_event("debate_complete", {
            "rounds": final_state["current_round"],
            "errors": len(final_state["errors"])
        })
        
        return final_state
        
    except Exception as e:
        log_event("debate_execution_error", {"error": str(e)})
        raise