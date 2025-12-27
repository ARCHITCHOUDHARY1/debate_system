# Main CLI launcher for Multi-Agent Debate System
import argparse
import os
import random
from workflow import run_debate
from logger import logger
from config import DEFAULT_TOPIC
import json
from datetime import datetime


def print_separator(char="=", length=70):
    print(char * length)


def print_debate_results(final_state):
    print_separator()
    print(f"DEBATE TOPIC: {final_state['topic']}")
    print_separator()
    
    print("\nDEBATE TRANSCRIPT:")
    print_separator("-")
    
    for arg in final_state['arguments']:
        print(f"\n[Round {arg['round']} - {arg['agent']}]")
        print(arg['text'])
    
    print("\n")
    print_separator()
    print("JUDGE'S DECISION:")
    print_separator()
    
    # Handle both string and dict judgment
    judgment = final_state['judgment']
    if isinstance(judgment, dict):
        if 'winner' in judgment:
            print(f"Winner: {judgment['winner']}")
            print(f"\nReasoning: {judgment.get('reasoning', 'N/A')}")
            print(f"\nSummary: {judgment.get('summary', 'N/A')}")
        else:
            print(judgment.get('raw', str(judgment)))
    else:
        print(judgment)
    
    if final_state['errors']:
        print("\n")
        print_separator()
        print("ERRORS DETECTED:")
        print_separator()
        for idx, error in enumerate(final_state['errors'], 1):
            print(f"{idx}. {error}")
    
    print("\n")
    print_separator()
    print(f"Debate completed: {final_state['current_round']} rounds")
    print_separator()


def export_results(final_state, format_type):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    try:
        if format_type in ['json', 'both']:
            json_file = f"logs/debate_export_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(final_state, f, indent=2, ensure_ascii=False)
            print(f"\nExported to JSON: {json_file}")
        
        if format_type in ['txt', 'both']:
            txt_file = f"logs/debate_export_{timestamp}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"DEBATE TOPIC: {final_state['topic']}\n")
                f.write("=" * 70 + "\n\n")
                f.write("DEBATE TRANSCRIPT:\n")
                f.write("-" * 70 + "\n\n")
                
                for arg in final_state['arguments']:
                    f.write(f"[Round {arg['round']} - {arg['agent']}]\n")
                    f.write(f"{arg['text']}\n\n")
                
                f.write("=" * 70 + "\n")
                f.write("JUDGE'S DECISION:\n")
                f.write("=" * 70 + "\n")
                
                # Handle dict or string judgment
                judgment = final_state['judgment']
                if isinstance(judgment, dict):
                    f.write(json.dumps(judgment, indent=2))
                else:
                    f.write(str(judgment))
                f.write("\n")
            
            print(f"\nExported to TXT: {txt_file}")
    except Exception as e:
        print(f"\nExport error: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description='Multi-Agent Debate System - ATG Technical Assignment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_debate.py
  python run_debate.py --topic "Is democracy the best form of government?"
  python run_debate.py --topic "Should AI be regulated?" --export json
  python run_debate.py --log-path logs/debate.jsonl --seed 42
  python run_debate.py --persona-config persona_templates
        """
    )
    
    parser.add_argument(
        '--topic',
        type=str,
        default=DEFAULT_TOPIC,
        help='Custom debate topic (default: from config.py)'
    )
    
    parser.add_argument(
        '--export',
        type=str,
        choices=['json', 'txt', 'both'],
        help='Export debate results to logs/ directory'
    )
    
    parser.add_argument(
        '--log-path',
        type=str,
        help='Custom path for debate log file (default: debate_log.jsonl)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        help='Random seed for deterministic runs'
    )
    
    parser.add_argument(
        '--persona-config',
        type=str,
        help='Path to persona templates directory (experimental)'
    )
    
    args = parser.parse_args()
    
    # Set random seed if provided
    if args.seed:
        random.seed(args.seed)
        print(f"Random seed set to: {args.seed}")
    
    # Set custom log path if provided
    if args.log_path:
        logger.set_log_file(args.log_path)
        print(f"Logging to: {args.log_path}")
    
    # TODO: Implement persona config loading when persona templates are ready
    if args.persona_config:
        print(f"Note: Persona config from {args.persona_config} (feature in development)")
    
    try:
        print("=" * 70)
        print("Multi-Agent Debate System - ATG Technical Assignment")
        print("=" * 70)
        print(f"\nTopic: {args.topic}\n")
        
        # Run the debate
        final_state = run_debate(args.topic)
        
        # Print results
        print_debate_results(final_state)
        
        # Save logs (now just prints summary)
        logger.save()
        
        # Export results if requested
        if args.export:
            export_results(final_state, args.export)
        
        print("\nDebate session complete!")
        
    except KeyboardInterrupt:
        print("\n\nDebate interrupted by user.")
        logger.save()
    except Exception as e:
        print(f"\nCRITICAL ERROR: {str(e)}")
        logger.log("critical_error", {"error": str(e)})
        logger.save()
        raise


if __name__ == "__main__":
    main()
