# Debate System Setup Guide

## Quick Start

### Option 1: PowerShell (Recommended)
```powershell
.\setup.ps1
```

### Option 2: Command Prompt
```cmd
.\setup.bat
```

## Common Issues & Solutions

### Issue 1: "setup.bat is not recognized"

**Error:**
```
setup.bat : The term 'setup.bat' is not recognized...
```

**Solution:**
PowerShell requires the `.\` prefix to run scripts in the current directory:
```powershell
.\setup.bat
```

### Issue 2: UV Not Installed

**Error:**
```
ERROR: UV is not installed or not in PATH
```

**Solution:**
1. Check if UV is installed:
   ```powershell
   uv --version
   ```

2. If not installed, install UV:
   - Windows: Download from https://github.com/astral-sh/uv
   - Or use PowerShell:
     ```powershell
     irm https://astral.sh/uv/install.ps1 | iex
     ```

### Issue 3: Missing API Key

**Error:**
```
ERROR: MISTRAL_API_KEY not found in .env file
```

**Solution:**
1. Open `.env` file
2. Add your Mistral API key:
   ```
   MISTRAL_API_KEY="your-api-key-here"
   ```

## Running the Debate System

After setup is complete:

```powershell
# Activate virtual environment (if not already activated)
.\.venv\Scripts\Activate.ps1

# Run the debate system
python main.py
```

## Project Structure

```
debate_system/
├── .env                # API configuration
├── setup.bat           # Windows CMD setup script
├── setup.ps1           # PowerShell setup script
├── requirements.txt    # Python dependencies
├── main.py            # Entry point
├── config.py          # Configuration settings
├── agents.py          # AI agent definitions
├── nodes.py           # Graph nodes
├── workflow.py        # Debate workflow
├── state.py           # State management
└── logger.py          # Logging utilities
```

## Manual Setup (Alternative)

If automated setup fails, follow these steps:

```powershell
# 1. Initialize UV project
uv init

# 2. Create virtual environment
uv venv

# 3. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 4. Install dependencies
uv pip install -r requirements.txt

# 5. Verify installation
python -c "import langgraph; import langchain_mistralai; print('Success')"

# 6. Run the system
python main.py
```

## Dependencies

- Python 3.10+
- UV package manager
- langgraph >= 0.0.20
- langchain-mistralai >= 0.0.5
- langchain-core >= 0.1.0
- python-dotenv >= 1.0.0

## Error Handling

All error messages are in plain ASCII text (no unicode characters) to prevent Windows encoding issues.

## Support

If you encounter issues:
1. Check that UV is installed: `uv --version`
2. Verify Python version: `python --version`
3. Ensure .env file has valid API key
4. Check error messages for specific guidance
