#settings
import os
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("ERROR: MISTRAL_API_KEY not found in .env file")

TOTAL_ROUNDS = 8
TURNS_PER_AGENT = 4
AGENT_A_NAME = "AgentA"
AGENT_B_NAME = "AgentB"
JUDGE_NAME = "Judge"

MODEL_NAME = "mistral-small-latest"
TEMPERATURE = 0.7

DEFAULT_TOPIC = "Should artificial intelligence be regulated by governments?"

LOG_FILE = "debate_log.txt"
ENABLE_CONSOLE_LOGGING = True