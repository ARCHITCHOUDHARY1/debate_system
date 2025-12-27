# State management
from typing import TypedDict, List, Literal, Union, Dict


class DebateState(TypedDict):
    topic: str
    current_round: int  # Number of completed agent turns (0 to TOTAL_ROUNDS)
    current_speaker: Literal["AgentA", "AgentB", "Judge"]
    arguments: List[dict]
    debate_complete: bool
    judgment: Union[str, Dict]  # Can be string or structured dict with winner/reasoning/summary
    errors: List[str]


def create_initial_state(topic: str) -> DebateState:
    return {
        "topic": topic,
        "current_round": 0,
        "current_speaker": "AgentA",
        "arguments": [],
        "debate_complete": False,
        "judgment": "",
        "errors": []
    }