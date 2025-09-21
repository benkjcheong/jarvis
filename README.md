# Jarvis Desktop Automation

AI-powered desktop automation system that understands natural language commands.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Usage
```bash
# Run the main application
python3 main.py

# Run tests
python3 run_tests.py
```

## Project Structure
```
src/
├── ai/           # AI models and processing
│   ├── vision.py    # Computer vision for UI detection
│   └── language.py  # NLP for prompt parsing
├── core/         # Core automation components
│   ├── types.py     # Data structures
│   ├── automation.py # UI analysis and actions
│   └── engine.py    # Main automation engine
└── workflows/    # Pre-defined workflows
    └── library.py   # Common task workflows
tests/           # Test files
```
