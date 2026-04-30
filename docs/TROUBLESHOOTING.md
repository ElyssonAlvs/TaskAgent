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
2. Database full
3. API error

**Solution:**
1. Check logs in `data/logs/`
2. Check API status:
   ```bash
   curl http://localhost:8000/v1/tasks/
   ```

---

## Ollama Too Slow

**Problem:** Responses taking too long

**Solutions:**
1. Use lighter model:
   ```bash
   ollama pull neural-chat
   # Then change in config/settings.yaml:
   # model: neural-chat
   ```

2. Increase RAM allocated to Ollama

3. Use GPU if available

---

## Module Not Found

**Problem:** `ModuleNotFoundError: No module named 'src'`

**Solution:**
Always run from project root:
```bash
cd c:\Users\elyss\Desktop\Projects\1_agent\TaskAgent
uv run python -m src.main
```

Never:
```bash
cd src
python main.py  # ❌ Wrong
```

---

## How to Debug?

1. **Enable verbose logging:**
   ```bash
   export LOG_LEVEL=DEBUG  # Linux
   set LOG_LEVEL=DEBUG     # Windows
   uv run python -m src.main
   ```

2. **Check logs:**
   ```bash
   tail -f data/logs/agent.log
   ```

3. **Test API manually:**
   ```bash
   curl http://localhost:8000/v1/tasks/
   ```

---

## Need More Help?

1. Check [QUICK_START.md](QUICK_START.md)
2. See examples in `data/examples/usage.md`
3. Read [ARCHITECTURE.md](ARCHITECTURE.md)
