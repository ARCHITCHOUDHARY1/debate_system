# State management
from typing import TypedDict, List, Literal


class DebateState(TypedDict):
    topic: str
    current_round: int
    current_speaker: Literal["AgentA", "AgentB", "Judge"]
    arguments: List[dict]
    debate_complete: bool
    judgment: str
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