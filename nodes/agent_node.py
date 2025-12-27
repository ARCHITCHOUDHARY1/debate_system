# Agent Node - Handles agent turn logic
from typing import Dict, List
from state import DebateState
from agents import agent_a, agent_b
from config import AGENT_A_NAME, AGENT_B_NAME
from logger import logger
from nodes.memory_node import get_agent_memory
from validation import validate_argument


def agent_a_turn(state: DebateState) -> DebateState:
    return _agent_turn(state, AGENT_A_NAME, agent_a)


def agent_b_turn(state: DebateState) -> DebateState:
    return _agent_turn(state, AGENT_B_NAME, agent_b)


def _agent_turn(state: DebateState, agent_name: str, agent) -> DebateState:
    try:
        # Validate it's the correct agent's turn
        if state["current_speaker"] != agent_name:
            error_msg = f"Turn violation: {agent_name} attempted to speak during {state['current_speaker']}'s turn"
            logger.log("turn_violation", {"error": error_msg})
            state["errors"].append(error_msg)
            return state
        
        # Increment round
        state["current_round"] += 1
        
        logger.log("agent_turn_start", {
            "agent": agent_name,
            "round": state["current_round"]
        })
        
        # Get memory slice (relevant context only)
        memory_slice = get_agent_memory(state, agent_name, max_items=3)
        
        # Generate and validate argument with retry logic
        MAX_RETRIES = 3
        argument = None
        validation_error = None
        
        for attempt in range(MAX_RETRIES):
            try:
                # Generate argument using memory slice
                candidate_argument = agent.generate_argument(
                    state["topic"],
                    memory_slice,
                    state["current_round"]
                )
                
                # Validate argument BEFORE accepting
                is_valid, error_msg = validate_argument(
                    candidate_argument,
                    state["arguments"],
                    state["topic"],
                    agent_name
                )
                
                if is_valid:
                    argument = candidate_argument
                    logger.log("argument_validated", {
                        "agent": agent_name,
                        "round": state["current_round"],
                        "attempt": attempt + 1
                    })
                    break
                else:
                    # Validation failed - log and retry
                    logger.log("validation_failed", {
                        "agent": agent_name,
                        "round": state["current_round"],
                        "attempt": attempt + 1,
                        "error": error_msg
                    })
                    validation_error = error_msg
                    
            except Exception as e:
                logger.log("agent_error", {
                    "agent": agent_name,
                    "attempt": attempt + 1,
                    "error": str(e)
                })
                validation_error = str(e)
        
        # If all retries failed, use error message
        if argument is None:
            argument = f"[Failed to generate valid argument after {MAX_RETRIES} attempts: {validation_error}]"
            state["errors"].append(f"{agent_name} validation error: {validation_error}")
            logger.log("argument_generation_failed", {
                "agent": agent_name,
                "round": state["current_round"],
                "error": validation_error
            })
        
        # Add validated argument to state
        state["arguments"].append({
            "round": state["current_round"],
            "agent": agent_name,
            "text": argument
        })
        
        logger.log("agent_turn_complete", {
            "agent": agent_name,
            "round": state["current_round"]
        })
        
        # Switch speaker
        state["current_speaker"] = AGENT_B_NAME if agent_name == AGENT_A_NAME else AGENT_A_NAME
        
        return state
        
    except Exception as e:
        error_msg = f"{agent_name} node error: {str(e)}"
        logger.log("node_error", {"agent": agent_name, "error": error_msg})
        state["errors"].append(error_msg)
        return state
