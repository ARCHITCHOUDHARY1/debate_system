# User Input Node - Handles CLI topic input and validation

def get_topic_input(topic: str = None) -> str:
    if topic:
        # Validate provided topic
        if len(topic.strip()) < 10:
            raise ValueError("Topic too short (minimum 10 characters)")
        if len(topic.strip()) > 500:
            raise ValueError("Topic too long (maximum 500 characters)")
        
        return topic.strip()
    
    # Interactive input
    print("Enter topic for debate:")
    user_topic = input("> ").strip()
    
    # Validate
    if len(user_topic) < 10:
        raise ValueError("Topic too short (minimum 10 characters)")
    if len(user_topic) > 500:
        raise ValueError("Topic too long (maximum 500 characters)")
    
    return user_topic


def sanitize_topic(topic: str) -> str:
    """Sanitize topic input"""
    return topic.strip()
