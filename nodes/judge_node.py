# Judge Node - Handles debate evaluation and winner selection
from state import DebateState
from agents import judge
from logger import logger


def judge_debate(state: DebateState) -> DebateState:

    try:
        logger.log("judging_start", {"total_arguments": len(state["arguments"])})
        
        # Generate judgment
        try:
            judgment = judge.make_judgment(
                state["topic"],
                state["arguments"]
            )
        except Exception as e:
            judgment = f"[Error: Judge could not make a decision - {str(e)}]"
            logger.log("judge_error", {"error": str(e)})
        
        state["judgment"] = judgment
        state["current_speaker"] = "Judge"
        
        logger.log("judging_complete", {"status": "success"})
        
        return state
        
    except Exception as e:
        error_msg = f"Judge node error: {str(e)}"
        logger.log("node_error", {"agent": "Judge", "error": error_msg})
        state["errors"].append(error_msg)
        state["judgment"] = f"[Error in judgment: {str(e)}]"
        return state
