# Memory Node - Manages debate memory and context
from typing import List, Dict
from state import DebateState


def update_memory(state: DebateState) -> DebateState:
    # Memory is maintained in state["arguments"]
    return state


def get_agent_memory(state: DebateState, agent_name: str, max_items: int = 3) -> List[Dict]:

    all_args = state.get("arguments", [])
    
    # Filter for opponent's arguments (last N)
    opponent_args = [arg for arg in all_args if arg.get("agent") != agent_name]
    relevant_opponent = opponent_args[-max_items:] if len(opponent_args) > max_items else opponent_args
    
    # Include agent's own last argument for context
    own_args = [arg for arg in all_args if arg.get("agent") == agent_name]
    relevant_own = own_args[-1:] if own_args else []
    
    # Combine and sort by round
    relevant = relevant_own + relevant_opponent
    relevant.sort(key=lambda x: x.get("round", 0))
    
    return relevant


def create_memory_summary(state: DebateState) -> str:
    summary = f"Topic: {state['topic']}\\n"
    summary += f"Current Round: {state['current_round']}\\n"
    summary += f"Total Arguments: {len(state['arguments'])}\\n"
    
    return summary
