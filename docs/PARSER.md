# Parser Mechanism

## O que é o Parser?

O **parser** é o mecanismo que traduz a resposta do LLM em comandos executáveis. Ele é o coração que converte linguagem natural em ações.

## Fluxo Simplificado

```
Input: "crie uma tarefa chamada Estudar"
  ↓
LLM Decision: Chamar create_task(title="Estudar")
  ↓
Parser processa resposta
  ↓
Execute: Chamada API ao TaskManager
  ↓
Output: "Tarefa criada: Estudar (ID: 1)"
```

## 5 Estratégias de Parsing

### 1. **Structured Tool Calls (Ideal)**
LLM retorna resposta estruturada do OpenAI:
```json
{
  "name": "create_task",
  "arguments": {"title": "Estudar"}
}
```
→ Direto para execução

### 2. **JSON Text Response**
LLM retorna JSON como texto:
```
[{"name": "create_task", "arguments": {"title": "Estudar"}}]
```
→ `parse_json_response()` converte

### 3. **Function Call String**
LLM retorna chamada de função:
```
create_task(title="Estudar")
```
→ `_handle_function_call()` com REGEX

### 4. **Named Arguments**
Argumentos com chave=valor:
```
title="Estudar", status="pending"
```
→ `_parse_named_args()` extrai

### 5. **Positional Arguments**
Apenas valores em ordem:
```
"Estudar"
```
→ `_parse_positional_args()` mapeia

## Fallback Chain

Se uma estratégia falhar, tenta a próxima:

```
Resposta da IA
    │
    ├─→ Tem tool_calls estruturado?
    │   └─→ SIM: Executa direto
    │   └─→ NÃO: Próximo passo
    │
    ├─→ É JSON válido?
    │   └─→ SIM: Parse JSON → Executa
    │   └─→ NÃO: Próximo passo
    │
    ├─→ É função Python?
    │   └─→ SIM: Parse função → Executa
    │   └─→ NÃO: Próximo passo
    │
    └─→ Erro: "Não consegui processar"
```

## Funções-Chave

**`execute_tool(name, args)`**  
Executa a função com argumentos. Faz o mapeamento:
```python
TOOL_FUNCTIONS = {
    "get_task": get_task,
    "create_task": create_task,
    ...
}
```

**`parse_json_response(content_str)`**  
Converte string JSON em dicionário

**`_handle_function_call(func_str)`**  
Usa REGEX para extrair: `(\w+)\((.*)\)`
- Grupo 1: Nome da função
- Grupo 2: Argumentos

**`handle_json_fallback(message_content)`**  
Orquestra a cadeia de fallbacks

## Por que múltiplas estratégias?

Ollama (Mistral local) não é 100% confiável:
- Às vezes retorna JSON
- Às vezes retorna Python code
- Às vezes retorna estruturado

Múltiplas estratégias garantem robustez.

## Detalhes Técnicos

Arquivo: `src/agents/task_agent.py`

Funções principais:
- `run_agent()` - Entrada
- `handle_tool_call()` - Processa tool_calls estruturados
- `handle_json_fallback()` - Processa fallbacks
- `_parse_named_args()` - Parser para key=value
- `_parse_positional_args()` - Parser para argumentos posicionais
- `_handle_function_call()` - Parser REGEX para function strings
- `execute_tool()` - Executa função mapeada

Ver [docs/ARCHITECTURE.md](ARCHITECTURE.md) para contexto completo.
