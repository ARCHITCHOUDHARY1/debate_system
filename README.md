# Multi-Agent Debate System - ATG Technical Assignment

## Overview

A multi-agent debate system using LangGraph where two AI agents engage in structured debates, judged by a third AI agent. Fully compliant with ATG technical assignment requirements.

## Features

- ✅ **Strict Alternation**: Exactly 8 agent turns (4 per agent) with enforced alternation
- ✅ **Memory Slicing**: Agents see only relevant context, not full transcript
- ✅ **Repetition Detection**: Arguments validated for uniqueness with retry logic
- ✅ **Structured Output**: Judge returns JSON with winner, reasoning, and summary
- ✅ **Persistent Logging**: JSON-lines format with immediate writes
- ✅ **CLI Flags**: Seed, log path, export options, persona templates
- ✅ **Test-Friendly**: Config safe for CI/tests, LLM dependency injection

## Quick Start

### 1. Setup Environment

```powershell
# Option 1: PowerShell (Recommended)
.\setup.ps1

# Option 2: Command Prompt
.\setup.bat
```

### 2. Configure API Key

Create/edit `.env` file:
```
MISTRAL_API_KEY=your-api-key-here
```

### 3. Run a Debate

```bash
# Basic usage
python run_debate.py

# Custom topic
python run_debate.py --topic "Is democracy the best form of government?"

# With seed for reproducibility
python run_debate.py --seed 42

# Custom log path
python run_debate.py --log-path logs/my_debate.jsonl

# Export results
python run_debate.py --export json

# All options combined
python run_debate.py --topic "Should AI be regulated?" --seed 123 --log-path logs/debate.jsonl --export both
```

## CLI Options

| Flag | Description | Example |
|------|-------------|---------|
| `--topic` | Custom debate topic | `--topic "Climate change policy"` |
| `--seed` | Random seed for deterministic runs | `--seed 42` |
| `--log-path` | Custom log file path | `--log-path logs/debate.jsonl` |
| `--export` | Export results (json/txt/both) | `--export json` |
| `--persona-config` | Persona templates directory | `--persona-config persona_templates` |

## Project Structure

```
debate_system/
├── .env                    # API configuration
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── setup.ps1               # PowerShell setup script
├── setup.bat               # Windows CMD setup script
│
├── run_debate.py           # Main entry point ← START HERE
├── config.py               # Configuration settings
├── state.py                # State management
├── agents.py               # AI agent definitions
├── workflow.py             # Debate workflow graph
├── logger.py               # JSON-lines logging
├── validation.py           # Argument validation
├── generate_dag.py         # DAG visualization
│
├── nodes/                  # LangGraph nodes
│   ├── __init__.py
│   ├── agent_node.py       # Agent turn logic
│   ├── judge_node.py       # Judge evaluation
│   ├── rounds_controller.py # Round validation
│   ├── memory_node.py      # Memory management
│   ├── logger_node.py      # Logging utilities
│   └── user_input_node.py  # Input handling
│
├── persona_templates/      # Agent persona templates
│   ├── scientist.txt
│   └── philosopher.txt
│
├── tests/                  # Automated tests
│   ├── __init__.py
│   └── test_debate.py
│
└── logs/                   # Generated logs (gitignored)
    └── *.jsonl
```

## Testing

### Run Tests (CI Mode)

```bash
# Set TESTING environment variable
set TESTING=1

# Run pytest
pytest tests/

# Or Windows PowerShell
$env:TESTING="1"
pytest tests/
```

### Manual Smoke Test

```bash
python run_debate.py --seed 42 --log-path logs/test.jsonl
```

Verify:
- 8 rounds completed
- Log file created at `logs/test.jsonl`
- Each line is valid JSON
- Judge output is structured JSON

## Output Format

### Judge JSON Schema

```json
{
  "winner": "AgentA" | "AgentB" | "Tie",
  "reasoning": "Detailed 3-4 sentence explanation...",
  "summary": "Brief 1-2 sentence summary..."
}
```

### Log File Format (JSON-Lines)

Each line in `*.jsonl` is a JSON object:
```json
{"timestamp": "2025-12-27T18:30:00", "event_type": "debate_start", "data": {...}}
{"timestamp": "2025-12-27T18:30:01", "event_type": "agent_turn_start", "data": {...}}
```

## Configuration

### Environment Variables

- `MISTRAL_API_KEY`: Mistral AI API key (required for production)
- `TESTING`: Set to `1` or `true` for test/CI mode (optional)

### Config File (`config.py`)

```python
TOTAL_ROUNDS = 8              # Total agent turns
TURNS_PER_AGENT = 4           # Turns per agent
AGENT_A_NAME = "AgentA"       # First agent name
AGENT_B_NAME = "AgentB"       # Second agent name
MODEL_NAME = "mistral-small-latest"
TEMPERATURE = 0.7
LOG_FILE = "debate_log.jsonl"
```

## Compliance Features

### A1: Config Safety ✅
- No import-time errors if API key missing
- `TESTING` environment variable support
- Safe for CI/test environments

### A2: Memory Slicing ✅
- Agents receive only relevant context (last 3 opponent + own last)
- Full transcript not exposed to agents
- Prevents memory leakage

### A3: Repetition Enforcement ✅
- Arguments validated for similarity and keyword overlap
- Automatic retry (up to 3 attempts) on repetition
- Comprehensive logging of validation failures

### A4: Structured Judge Output ✅
- JSON schema with winner, reasoning, summary
- Markdown code block extraction
- Error handling for malformed output

### A5: Persistent Logging ✅
- JSON-lines format (one object per line)
- Immediate writes (crash-safe)
- Custom log path via `--log-path`
- Auto-creates directories

## Dependencies

- Python 3.10+
- langgraph >= 0.0.20
- langchain-mistralai >= 0.0.5
- langchain-core >= 0.1.0
- python-dotenv >= 1.0.0

## Troubleshooting

### Issue: Missing API Key
```
ERROR: MISTRAL_API_KEY required to initialize AgentA
```
**Solution:** Add API key to `.env` file or set `TESTING=1` for test mode

### Issue: Import Errors
```
ModuleNotFoundError: No module named 'langgraph'
```
**Solution:** Run setup script or manually install: `pip install -r requirements.txt`

### Issue: UV Not Found
```
ERROR: UV is not installed
```
**Solution:** Install UV from https://github.com/astral-sh/uv or use pip directly

### Issue: Log Directory Missing
The logger automatically creates directories. If you get permission errors, ensure write access to the project directory.

## Examples

### Example 1: Basic Debate
```bash
python run_debate.py
```

### Example 2: Reproducible Run
```bash
python run_debate.py --seed 42 --topic "Is AI beneficial?"
```

### Example 3: Custom Logging
```bash
python run_debate.py --log-path experiments/debate_001.jsonl --export json
```

### Example 4: Full Featured
```bash
python run_debate.py \
  --topic "Should universal basic income be implemented?" \
  --seed 123 \
  --log-path logs/ubi_debate.jsonl \
  --export both
```

## Development

### Running in Test Mode
```bash
# Set environment variable
export TESTING=1  # Linux/Mac
set TESTING=1     # Windows CMD
$env:TESTING="1"  # PowerShell

# Run without API key
python run_debate.py
```

### Generate DAG Visualization
```bash
python generate_dag.py
```

## License

ATG Technical Assignment - Educational Use

## Support

For issues or questions:
1. Check that UV/pip is installed
2. Verify Python version: `python --version`
3. Ensure `.env` has valid API key (or `TESTING=1`)
4. Check log files for detailed error information
