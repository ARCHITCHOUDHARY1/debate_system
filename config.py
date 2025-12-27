#settings
import os
from dotenv import load_dotenv

load_dotenv()

# Check if running in test/CI environment
IS_TEST_ENV = os.getenv("TESTING", "false").lower() in ("true", "1", "yes")

# Get API key but don't raise on missing (let agents validate when instantiated)
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

TOTAL_ROUNDS = 8
TURNS_PER_AGENT = 4
AGENT_A_NAME = "AgentA"
AGENT_B_NAME = "AgentB"
JUDGE_NAME = "Judge"

MODEL_NAME = "mistral-small-latest"
TEMPERATURE = 0.7

DEFAULT_TOPIC = "Should artificial intelligence be regulated by governments?"

LOG_FILE = "debate_log.jsonl"
ENABLE_CONSOLE_LOGGING = True