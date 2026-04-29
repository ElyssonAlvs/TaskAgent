# TaskAgent 🤖

AI-powered task manager. Chat naturally, get things done.

---

## 📚 Documentation Guide

### First Time?
Start here: **[QUICK START](docs/QUICK_START.md)**
- Installation
- Running locally  
- First commands

### How It Works?
Read: **[ARCHITECTURE](docs/ARCHITECTURE.md)**
- System design
- Component overview
- Data flow

### Available Commands?
See: **[COMMANDS](docs/COMMANDS.md)**
- What you can ask
- Examples
- Supported operations

### Deep Dive on Parser?
Learn: **[PARSER](docs/PARSER.md)**
- How NLP → Functions
- Parsing strategies
- Technical details

### Something Broke?
Check: **[TROUBLESHOOTING](docs/TROUBLESHOOTING.md)**
- Common issues
- Debugging steps
- Solutions

---

## 🚀 Quick Start

```bash
# 1. Setup
cd TaskAgent
uv venv
source .venv/bin/activate  # Linux/Mac or .venv\Scripts\activate on Windows

# 2. Start Ollama (Terminal 1)
ollama serve
ollama pull mistral

# 3. Start TaskManager API (Terminal 2)  
cd ../TaskManager
uv run python -m uvicorn main:app --reload

# 4. Start Agent (Terminal 3)
cd ../TaskAgent
uv run python -m src.main

# 5. Chat!
>>> list my tasks
>>> create task: Study Python
>>> delete task 1
```

See [QUICK START](docs/QUICK_START.md) for detailed steps.

---

## 📦 Project Structure

```
TaskAgent/
├── src/                    # Source code
│   ├── agents/            # Agent logic
│   ├── tools/             # Task management tools
│   ├── utils/             # Utilities
│   └── main.py            # Entry point
├── docs/                  # Documentation
│   ├── QUICK_START.md     # Getting started
│   ├── ARCHITECTURE.md    # System design
│   ├── PARSER.md          # NLP → Functions
│   ├── COMMANDS.md        # Available commands
│   └── TROUBLESHOOTING.md # Problem solving
├── config/                # Configuration
│   ├── settings.yaml      # App settings
│   └── .env.example       # Environment template
└── data/                  # Data & examples
    ├── examples/          # Usage examples
    └── logs/              # Execution logs
```

---

## 🎯 What Can It Do?

| Task | Command | Tool |
|------|---------|------|
| **List tasks** | "show my tasks" | `list_tasks()` |
| **Create** | "create task: Study" | `create_task()` |
| **View** | "show task 1" | `get_task()` |
| **Update** | "mark task 2 as done" | `update_task()` |
| **Delete** | "remove task 3" | `delete_task()` |

Full list in [COMMANDS.md](docs/COMMANDS.md)

---

## 🧠 How It Works (Simplified)

1. **You talk** → "Create a task to study"
2. **LLM understands** → Mistral model decides to call `create_task()`
3. **Parser converts** → Extracts title and other parameters
4. **Tool executes** → Calls TaskManager API
5. **Result returns** → "Task created: ..."

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for full details.

---

## 🔧 Stack

- **Language:** Python 3.10+
- **LLM:** Ollama (Mistral)
- **LLM Client:** OpenAI SDK
- **Package Manager:** UV
- **API Client:** Requests

---

## 📋 Requirements

- Python 3.10+
- Ollama running locally
- TaskManager API (`http://localhost:8000`)
- UV package manager

---

## 🚨 Troubleshooting

### API won't connect?
```bash
cd ../TaskManager
uv run python -m uvicorn main:app --reload
```

### Ollama offline?
```bash
ollama serve
```

### Model missing?
```bash
ollama pull mistral
```

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for more.

---

## 📝 License

See LICENSE file

---

**Built with Python + Ollama + FastAPI**
