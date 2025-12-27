# All agents
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import List, Dict
import time
from config import MODEL_NAME, TEMPERATURE, AGENT_A_NAME, AGENT_B_NAME, JUDGE_NAME
from logger import logger

# API retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


class DebaterAgent:
    def __init__(self, agent_name: str, position: str):
        self.agent_name = agent_name
        self.position = position
        try:
            self.llm = ChatMistralAI(
                model=MODEL_NAME,
                temperature=TEMPERATURE
            )
            logger.log("agent_initialized", {
                "agent": agent_name,
                "position": position
            })
        except Exception as e:
            logger.log("agent_init_error", {
                "agent": agent_name,
                "error": str(e)
            })
            raise
    
    def generate_argument(
        self,
        topic: str,
        previous_arguments: List[Dict],
        round_number: int
    ) -> str:
        try:
            context = "\n".join([
                f"Round {arg['round']} - {arg['agent']}: {arg['text']}"
                for arg in previous_arguments
            ]) if previous_arguments else "No previous arguments yet."
            
            turn_number = (round_number + 1) // 2
            
            system_prompt = f"""You are {self.agent_name}, debating {self.position} the topic.

Rules:
- You have exactly 4 turns total (this is turn {turn_number})
- Make strong, logical arguments
- Respond to opponent points
- Keep arguments concise (2-3 sentences)
- Do NOT mention whose turn it is next"""

            human_prompt = f"""Topic: {topic}

Previous arguments:
{context}

Your argument:"""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            # Retry logic for API calls
            for attempt in range(MAX_RETRIES):
                try:
                    response = self.llm.invoke(messages)
                    argument = response.content.strip()
                    
                    logger.log("argument_generated", {
                        "agent": self.agent_name,
                        "round": round_number,
                        "length": len(argument),
                        "attempt": attempt + 1
                    })
                    
                    return argument
                except Exception as api_error:
                    if attempt < MAX_RETRIES - 1:
                        logger.log("api_retry", {
                            "agent": self.agent_name,
                            "attempt": attempt + 1,
                            "error": str(api_error)
                        })
                        time.sleep(RETRY_DELAY)
                    else:
                        raise api_error
            
        except Exception as e:
            error_msg = f"Error generating argument for {self.agent_name}: {str(e)}"
            logger.log("argument_error", {
                "agent": self.agent_name,
                "error": error_msg
            })
            return f"[Error generating argument: {str(e)}]"


class JudgeAgent:
    def __init__(self):
        try:
            self.llm = ChatMistralAI(
                model=MODEL_NAME,
                temperature=0.3
            )
            logger.log("judge_initialized", {"status": "success"})
        except Exception as e:
            logger.log("judge_init_error", {"error": str(e)})
            raise
    
    def make_judgment(self, topic: str, arguments: List[Dict]) -> str:
        try:
            debate_transcript = "\n\n".join([
                f"Round {arg['round']} - {arg['agent']}:\n{arg['text']}"
                for arg in arguments
            ])
            
            system_prompt = f"""You are {JUDGE_NAME}, an impartial debate judge.

Evaluate both debaters on:
1. Strength of arguments
2. Logic and evidence
3. Rebuttals
4. Coherence

Declare a winner and explain in 3-4 sentences."""

            human_prompt = f"""Topic: {topic}

Debate Transcript:
{debate_transcript}

Your judgment:"""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            # Retry logic for API calls
            for attempt in range(MAX_RETRIES):
                try:
                    response = self.llm.invoke(messages)
                    judgment = response.content.strip()
                    
                    logger.log("judgment_generated", {
                        "length": len(judgment),
                        "attempt": attempt + 1
                    })
                    
                    return judgment
                except Exception as api_error:
                    if attempt < MAX_RETRIES - 1:
                        logger.log("api_retry", {
                            "agent": "Judge",
                            "attempt": attempt + 1,
                            "error": str(api_error)
                        })
                        time.sleep(RETRY_DELAY)
                    else:
                        raise api_error
            
        except Exception as e:
            error_msg = f"Error making judgment: {str(e)}"
            logger.log("judgment_error", {"error": error_msg})
            return f"[Error making judgment: {str(e)}]"


agent_a = DebaterAgent(AGENT_A_NAME, "for")
agent_b = DebaterAgent(AGENT_B_NAME, "against")
judge = JudgeAgent()