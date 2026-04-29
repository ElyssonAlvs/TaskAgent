# Quick Start

## Pré-requisitos

- Python 3.10+
- Ollama rodando (`ollama serve`)
- TaskManager API rodando em `http://localhost:8000`
- UV package manager

## Instalação

```bash
# Clone/setup
cd TaskAgent
uv venv

# Ative o ambiente
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

## Iniciar Ollama

**Terminal 1:**
```bash
ollama serve
```

**Terminal 2:**
```bash
ollama pull mistral
```

## Iniciar TaskManager API

**Terminal 3:**
```bash
cd ../TaskManager
uv run python -m uvicorn main:app --reload
```

API disponível em: `http://localhost:8000`

## Rodar TaskAgent

**Terminal 4:**
```bash
cd ../TaskAgent
uv run python -m src.main
```

## Primeiros Comandos

```
>>> list my tasks
>>> create task called "My first task"
>>> show task 1
```

Ver mais exemplos em [docs/COMMANDS.md](COMMANDS.md)
