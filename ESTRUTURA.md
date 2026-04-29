# 📁 Estrutura Completa do Projeto

Novo layout profissional do TaskAgent:

```
TaskAgent/
│
├── 📄 .gitignore              # Ignorar arquivos do git
│
├── 📂 config/                  # CONFIGURAÇÃO
│   ├── .env.example            # Template de variáveis
│   └── settings.yaml           # Configurações YAML
│
├── 📂 data/                    # DADOS
│   ├── examples/
│   │   └── usage.md            # Exemplos de uso
│   └── logs/                   # Logs de execução
│
├── 📂 docs/                    # DOCUMENTAÇÃO
│   ├── QUICK_START.md          # Como começar
│   ├── ARCHITECTURE.md         # Design do sistema
│   ├── PARSER.md               # Como funciona o parser
│   ├── COMMANDS.md             # Comandos disponíveis
│   └── TROUBLESHOOTING.md      # Resolução de problemas
│
├── 📂 src/                     # CÓDIGO-FONTE
│   ├── agents/
│   │   ├── __init__.py
│   │   └── task_agent.py       # Lógica principal do agente
│   ├── tools/
│   │   ├── __init__.py
│   │   └── task_tools.py       # Ferramentas (chamadas API)
│   ├── utils/
│   │   └── __init__.py         # Utilitários (vazio)
│   ├── __init__.py
│   └── main.py                 # Entry point
│
├── 📄 LICENSE
├── 📄 README.md                # Documentação principal (ÍNDICE)
└── 📄 pyproject.toml           # Configuração do projeto (uv)
```

---

## 🔍 Explicação por Pasta

### `config/`
- `settings.yaml` - Configurações centralizadas (timeout, endpoints, etc)
- `.env.example` - Template para variáveis de ambiente

### `data/`
- `examples/` - Exemplos de comandos que podem ser usados
- `logs/` - Onde os logs de execução são salvos

### `docs/`
- `QUICK_START.md` - Guia de instalação e primeiros passos
- `ARCHITECTURE.md` - Descrição do design e componentes
- `PARSER.md` - Explicação técnica de como funciona conversão NLP → Functions
- `COMMANDS.md` - Lista de comandos disponíveis com exemplos
- `TROUBLESHOOTING.md` - Problemas comuns e soluções

### `src/`
- `agents/task_agent.py` - Núcleo do agente (LLM + parser)
- `tools/task_tools.py` - Implementação das ferramentas (get_task, create_task, etc)
- `utils/` - Lugar para funções utilitárias no futuro
- `main.py` - Ponto de entrada do programa

---

## 🚀 Como Usar

### Rodar o agente
```bash
uv run python -m src.main
```

### Ou via script instalado
```bash
uv sync
taskagent
```

---

## 📚 Onde Procurar Informações

| Pergunta | Arquivo |
|----------|---------|
| Como começo? | [QUICK_START.md](docs/QUICK_START.md) |
| Como funciona? | [ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Que comandos posso usar? | [COMMANDS.md](docs/COMMANDS.md) |
| Como o parser funciona? | [PARSER.md](docs/PARSER.md) |
| Algo deu erro! | [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) |
| Visão geral | [README.md](README.md) |

---

## ✅ Benefícios da Nova Estrutura

- ✅ **Padrão Python** - Segue PEP 517
- ✅ **Escalável** - Fácil adicionar novos módulos
- ✅ **Profissional** - Estrutura usada em projetos reais
- ✅ **Organizado** - Separação clara de responsabilidades
- ✅ **Documentado** - Docs estruturadas por tema
- ✅ **Configurável** - Settings em arquivo separado
- ✅ **Maintível** - Código mais fácil de manter
