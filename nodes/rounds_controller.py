# Rounds Controller Node - Manages round count and debate completion
from state import DebateState
from config import TOTAL_ROUNDS, AGENT_A_NAME, AGENT_B_NAME
from logger import logger


def validate_round(state: DebateState) -> DebateState:

    try:
        logger.log("validation_start", {
            "round": state["current_round"],
            "speaker": state["current_speaker"]
        })
        
        # Check if we've reached the round limit
        if state["current_round"] >= TOTAL_ROUNDS:
            state["debate_complete"] = True
            logger.log("validation_complete", {"status": "debate_complete"})
        else:
            logger.log("validation_complete", {"status": "continue"})
        
        return state
        
    except Exception as e:
        error_msg = f"Round validation error: {str(e)}"
        logger.log("validation_error", {"error": error_msg})
        state["errors"].append(error_msg)
        return state


def should_continue(state: DebateState) -> str:
    if state.get("debate_complete") or state["current_round"] >= TOTAL_ROUNDS:
        return "judge"
    else:
        return "continue"


def route_to_speaker(state: DebateState) -> str:
    next_speaker = state["current_speaker"]
    
    if next_speaker == AGENT_A_NAME:
        return "agent_a"
    else:
        return "agent_b"
