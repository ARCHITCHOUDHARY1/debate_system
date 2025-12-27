# Agent Node - Handles agent turn logic
from typing import Dict, List
from state import DebateState
from agents import agent_a, agent_b
from config import AGENT_A_NAME, AGENT_B_NAME
from logger import logger


def agent_a_turn(state: DebateState) -> DebateState:
    """AgentA's turn in the debate"""
    return _agent_turn(state, AGENT_A_NAME, agent_a)


def agent_b_turn(state: DebateState) -> DebateState:
    """AgentB's turn in the debate"""
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
        
        # Generate argument
        try:
            argument = agent.generate_argument(
                state["topic"],
                state["arguments"],
                state["current_round"]
            )
        except Exception as e:
            argument = f"[Error generating argument: {str(e)}]"
            logger.log("agent_error", {"agent": agent_name, "error": str(e)})
        
        # Add argument to state
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
