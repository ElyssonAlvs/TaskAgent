# Architecture

## Main Components

```
┌─────────────────────────────────────────────────────┐
│                    USER INPUT                        │
│            (Natural Language)                        │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│         src/agents/task_agent.py                     │
│  - Runs LLM (Mistral via Ollama)                    │
│  - Selects function to call                         │
│  - Returns response                                 │
└────────────────────┬────────────────────────────────┘
                     │
              ┌──────┴──────┐
              │             │
    ┌─────────▼──────┐  ┌──▼──────────────┐
    │ Tool Calls OK  │  │ JSON/Text Response
    │ (Structured)   │  │ (Fallback)
    └─────────┬──────┘  └──┬───────────────┘
              │            │
    ┌─────────▼────────────▼──────────┐
    │ src/tools/task_tools.py         │
    │ - Parser Functions              │
    │ - API Calls                     │
    │ - Result Formatting             │
    └─────────┬──────────────────────┘
              │
    ┌─────────▼──────────────────────┐
    │  TaskManager API                │
    │  (CRUD operations)              │
    └──────────────────────────────────┘
```

## Data Flow

**Input:** `"Create a task called Study"`

1. **Agent receives** → `run_agent()` in `task_agent.py`
2. **LLM processes** → Mistral chooses function `create_task()`
3. **Parser processes** → Extracts arguments
4. **Tool executes** → API call to TaskManager
5. **Result returns** → Formatted message to user

## Directory Structure

```
src/
├── agents/          # Agent logic
│   └── task_agent.py   # Run agent, parser, tool dispatcher
├── tools/           # Tools (API calls)
│   └── task_tools.py   # CRUD: get, create, list, update, delete
├── utils/           # Utilities (empty for now)
└── main.py         # Entry point

config/
├── settings.yaml    # Configuration
└── .env.example     # Environment template

docs/
├── QUICK_START.md   # Getting started
├── ARCHITECTURE.md  # This file
├── PARSER.md        # How the parser works
├── COMMANDS.md      # Available commands
└── TROUBLESHOOTING.md # Troubleshooting issues

data/
├── examples/        # Usage examples
└── logs/           # Execution logs
```

## Technologies

| Component | Technology |
|-----------|-----------|
| LLM | Ollama (Mistral) |
| API Client | OpenAI Python |
| HTTP Client | Requests |
| Config | YAML |
