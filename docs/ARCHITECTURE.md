# Architecture

## Componentes Principais

```
┌─────────────────────────────────────────────────────┐
│                    USER INPUT                        │
│            (Linguagem Natural)                       │
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

## Fluxo de Dados

**Entrada:** `"crie uma tarefa chamada Estudar"`

1. **Agent recebe** → `run_agent()` em `task_agent.py`
2. **LLM processa** → Mistral escolhe função `create_task()`
3. **Parser processa** → Extrai argumentos
4. **Ferramenta executa** → Chamada API ao TaskManager
5. **Resultado retorna** → Mensagem formatada ao usuário

## Estrutura de Diretórios

```
src/
├── agents/          # Lógica do agente
│   └── task_agent.py   # Run agent, parser, tool dispatcher
├── tools/           # Ferramentas (API calls)
│   └── task_tools.py   # CRUD: get, create, list, update, delete
├── utils/           # Utilitários (vazio por enquanto)
└── main.py         # Entry point

config/
├── settings.yaml    # Configurações
└── .env.example     # Template de variáveis

docs/
├── QUICK_START.md   # Como começar
├── ARCHITECTURE.md  # Este arquivo
├── PARSER.md        # Como o parser funciona
├── COMMANDS.md      # Comandos disponíveis
└── TROUBLESHOOTING.md # Resolvendo problemas

data/
├── examples/        # Exemplos de uso
└── logs/           # Logs da execução
```

## Tecnologias

| Componente | Tecnologia |
|-----------|-----------|
| LLM | Ollama (Mistral) |
| API Client | OpenAI Python |
| HTTP Client | Requests |
| Config | YAML |
