# Judge Node - Handles debate evaluation and winner selection
from state import DebateState
from agents import judge
from logger import logger
import json


def judge_debate(state: DebateState) -> DebateState:
    try:
        logger.log("judging_start", {"total_arguments": len(state["arguments"])})
        
        # Generate judgment
        try:
            judgment_text = judge.make_judgment(
                state["topic"],
                state["arguments"]
            )
        except Exception as e:
            judgment_text = f"[Error: Judge could not make a decision - {str(e)}]"
            logger.log("judge_error", {"error": str(e)})
        
        # Parse JSON output
        try:
            # Strip markdown code blocks if present
            judgment_clean = judgment_text.strip()
            if judgment_clean.startswith("```"):
                # Extract content between code blocks
                lines = judgment_clean.split('\n')
                json_lines = []
                in_code_block = False
                for line in lines:
                    if line.strip().startswith("```"):
                        in_code_block = not in_code_block
                        continue
                    if in_code_block:
                        json_lines.append(line)
                judgment_clean = '\n'.join(json_lines)
            
            # Try to parse as JSON
            parsed_judgment = json.loads(judgment_clean)
            
            # Validate required fields
            required_fields = ["winner", "reasoning", "summary"]
            if all(field in parsed_judgment for field in required_fields):
                state["judgment"] = parsed_judgment
                logger.log("judgment_parsed", {
                    "winner": parsed_judgment.get("winner"),
                    "status": "valid_json"
                })
            else:
                # Missing required fields
                missing = [f for f in required_fields if f not in parsed_judgment]
                error_msg = f"Judge JSON missing fields: {missing}"
                logger.log("judgment_parse_error", {"error": error_msg})
                state["errors"].append(error_msg)
                state["judgment"] = {
                    "raw": judgment_text,
                    "parse_error": error_msg
                }
                
        except json.JSONDecodeError as e:
            # Not valid JSON - store as raw with error
            error_msg = f"Judge output invalid JSON: {str(e)}"
            logger.log("judgment_parse_error", {"error": error_msg})
            state["errors"].append(error_msg)
            state["judgment"] = {
                "raw": judgment_text,
                "parse_error": error_msg
            }
        
        state["current_speaker"] = "Judge"
        logger.log("judging_complete", {"status": "success"})
        
        return state
        
    except Exception as e:
        error_msg = f"Judge node error: {str(e)}"
        logger.log("node_error", {"agent": "Judge", "error": error_msg})
        state["errors"].append(error_msg)
        state["judgment"] = {
            "raw": f"[Error in judgment: {str(e)}]",
            "parse_error": error_msg
        }
        return state
