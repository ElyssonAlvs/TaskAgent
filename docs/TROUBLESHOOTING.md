# Troubleshooting

## "Connection refused" / API offline

**Problem:** Error connecting to TaskManager

**Solution:**
```bash
cd ../TaskManager
uv run python -m uvicorn main:app --reload
```

API should be at `http://localhost:8000`

---

## "Connection refused" / Ollama offline

**Problem:** Error connecting to Ollama

**Solution:**
```bash
ollama serve
```

Ollama should be at `http://localhost:11434`

---

## "Model not found"

**Problem:** Mistral model not available

**Solution:**
```bash
ollama pull mistral
```

Wait for download to complete.

---

## Request timeout

**Problem:** Agent takes too long to respond

**Causes:**
- Slow LLM (machine overloaded)
- Slow network
- Overloaded TaskManager

**Solutions:**
1. Increase timeout in `config/settings.yaml`:
   ```yaml
   agent:
     timeout: 10  # From 5 to 10 seconds
   ```

2. Close tabs/programs to free up resources

3. Use smaller model (ex: `neural-chat`)

---

## ImportError: No module named 'openai'

**Problem:** openai library not installed

**Solution:**
```bash
uv sync
```

Or:
```bash
uv pip install openai requests
```

---

## "Unknown tool" error

**Problem:** Agent did not recognize the command

**Cause:** Command too vague or ambiguous

**Solution:** Be more specific:
```
❌ "do something with task"
✅ "create a task called Study"
```

---

## Task is not created

**Problem:** Command was understood but task was not created

**Causes:**
1. TaskManager API offline
2. Banco de dados full
3. Erro na API

**Solução:**
1. Verificar logs em `data/logs/`
2. Checar status da API:
   ```bash
   curl http://localhost:8000/v1/tasks/
   ```

---

## Ollama muito lento

**Problema:** Respostas demorando muito

**Soluções:**
1. Usar modelo mais leve:
   ```bash
   ollama pull neural-chat
   # Depois alterar em config/settings.yaml:
   # model: neural-chat
   ```

2. Aumentar RAM alocada para Ollama

3. Usar GPU se disponível

---

## Módulo não encontrado

**Problema:** `ModuleNotFoundError: No module named 'src'`

**Solução:**
Executar sempre da raiz do projeto:
```bash
cd c:\Users\elyss\Desktop\Projects\1_agent\TaskAgent
uv run python -m src.main
```

Nunca:
```bash
cd src
python main.py  # ❌ Errado
```

---

## Como debug?

1. **Ativar verbose logging:**
   ```bash
   export LOG_LEVEL=DEBUG  # Linux
   set LOG_LEVEL=DEBUG     # Windows
   uv run python -m src.main
   ```

2. **Checar logs:**
   ```bash
   tail -f data/logs/agent.log
   ```

3. **Testar API manualmente:**
   ```bash
   curl http://localhost:8000/v1/tasks/
   ```

---

## Mais ajuda?

1. Verificar [QUICK_START.md](QUICK_START.md)
2. Ver exemplos em `data/examples/usage.md`
3. Ler [ARCHITECTURE.md](ARCHITECTURE.md)
