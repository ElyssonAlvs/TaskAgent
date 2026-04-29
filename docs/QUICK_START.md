# Quick Start

## Prerequisites

- Python 3.10+
- Ollama running (`ollama serve`)
- TaskManager API running on `http://localhost:8000`
- UV package manager

## Installation

```bash
# Clone/setup
cd TaskAgent
uv venv

# Activate the environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

## Start Ollama

**Terminal 1:**
```bash
ollama serve
```

**Terminal 2:**
```bash
ollama pull mistral
```

## Start TaskManager API

**Terminal 3:**
```bash
cd ../TaskManager
uv run python -m uvicorn main:app --reload
```

API available at: `http://localhost:8000`

## Run TaskAgent

**Terminal 4:**
```bash
cd ../TaskAgent
uv run python -m src.main
```

## First Commands

```
>>> list my tasks
>>> create task called "My first task"
>>> show task 1
```

See more examples in [docs/COMMANDS.md](COMMANDS.md)
