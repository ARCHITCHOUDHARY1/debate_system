# Argument validation utilities
from typing import List, Dict, Tuple
from difflib import SequenceMatcher


def calculate_similarity(text1: str, text2: str) -> float:
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def extract_keywords(text: str, min_length: int = 4) -> set:
    words = text.lower().split()
    return {word.strip('.,!?;:') for word in words if len(word) >= min_length}


def check_repetition(new_argument: str, previous_arguments: List[Dict], 
                     similarity_threshold: float = 0.7,
                     keyword_threshold: float = 0.8) -> Tuple[bool, str]:

    if not previous_arguments:
        return False, ""
    
    new_keywords = extract_keywords(new_argument)
    
    for prev_arg in previous_arguments:
        prev_text = prev_arg.get('text', '')
        
        # Check string similarity
        similarity = calculate_similarity(new_argument, prev_text)
        if similarity >= similarity_threshold:
            return True, f"Argument too similar to Round {prev_arg['round']} ({similarity:.0%} match)"
        
        # Check keyword overlap
        prev_keywords = extract_keywords(prev_text)
        if prev_keywords and new_keywords:
            overlap = len(new_keywords & prev_keywords) / len(new_keywords | prev_keywords)
            if overlap >= keyword_threshold:
                return True, f"Argument repeats keywords from Round {prev_arg['round']} ({overlap:.0%} overlap)"
    
    return False, ""


def check_topic_relevance(argument: str, topic: str, min_relevance: float = 0.3) -> Tuple[bool, float]:
    # Extract keywords from topic (use min_length=2 to capture "AI")
    topic_keywords = extract_keywords(topic, min_length=2)
    
    # Extract keywords from argument
    arg_keywords = extract_keywords(argument, min_length=2)
    
    if not topic_keywords:
        return True, 1.0  # Can't judge, assume relevant
    
    # Calculate overlap
    overlap = len(topic_keywords & arg_keywords)
    relevance = overlap / len(topic_keywords) if topic_keywords else 0.0
    
    return relevance >= min_relevance, relevance


def validate_argument(argument: str, previous_arguments: List[Dict], 
                      topic: str, agent_name: str) -> Tuple[bool, str]:
    # Check minimum length
    if len(argument.strip()) < 20:
        return False, "Argument too short (minimum 20 characters)"
    
    # Check repetition against agent's own previous arguments
    agent_previous = [arg for arg in previous_arguments if arg.get('agent') == agent_name]
    is_repetition, repetition_reason = check_repetition(
        argument, agent_previous, 
        similarity_threshold=0.7,
        keyword_threshold=0.8
    )
    
    if is_repetition:
        return False, f"Repetition detected: {repetition_reason}"
    
    # Check topic relevance
    is_relevant, relevance_score = check_topic_relevance(argument, topic, min_relevance=0.2)
    
    if not is_relevant:
        return False, f"Argument not relevant to topic (relevance: {relevance_score:.0%})"
    
    return True, ""
