# Parser Mechanism

## What is the Parser?

The **parser** is the mechanism that translates the LLM response into executable commands. It is the heart that converts natural language into actions.

## Simplified Flow

```
Input: "Create a task called Study"
  ↓
LLM Decision: Call create_task(title="Study")
  ↓
Parser processes response
  ↓
Execute: API call to TaskManager
  ↓
Output: "Task created: Study (ID: 1)"
```

## 5 Parsing Strategies

### 1. **Structured Tool Calls (Ideal)**
LLM returns structured OpenAI response:
```json
{
  "name": "create_task",
  "arguments": {"title": "Study"}
}
```
→ Direct execution

### 2. **JSON Text Response**
LLM returns JSON as text:
```
[{"name": "create_task", "arguments": {"title": "Study"}}]
```
→ `parse_json_response()` converts

### 3. **Function Call String**
LLM returns function call:
```
create_task(title="Study")
```
→ `_handle_function_call()` with REGEX

### 4. **Named Arguments**
Arguments with key=value:
```
title="Study", status="pending"
```
→ `_parse_named_args()` extracts

### 5. **Positional Arguments**
Values only in order:
```
"Study"
```
→ `_parse_positional_args()` maps

## Fallback Chain

If one strategy fails, it tries the next:

```
AI Response
    │
    ├─→ Has structured tool_calls?
    │   └─→ YES: Execute directly
    │   └─→ NO: Next step
    │
    ├─→ Valid JSON?
    │   └─→ YES: Parse JSON → Execute
    │   └─→ NO: Next step
    │
    ├─→ Is Python function?
    │   └─→ YES: Parse function → Execute
    │   └─→ NO: Next step
    │
    └─→ Error: "Could not process"
```

## Key Functions

**`execute_tool(name, args)`**  
Executes function with arguments. Does the mapping:
```python
TOOL_FUNCTIONS = {
    "get_task": get_task,
    "create_task": create_task,
    ...
}
```

**`parse_json_response(content_str)`**  
Converts JSON string to dictionary

**`_handle_function_call(func_str)`**  
Uses REGEX to extract: `(\w+)\((.*)\)`
- Group 1: Function name
- Group 2: Arguments

**`handle_json_fallback(message_content)`**  
Orchestrates the fallback chain

## Why Multiple Strategies?

Ollama (local Mistral) is not 100% reliable:
- Sometimes returns JSON
- Sometimes returns Python code
- Sometimes returns structured format

Multiple strategies ensure robustness.

## Technical Details

File: `src/agents/task_agent.py`

Main functions:
- `run_agent()` - Entry point
- `handle_tool_call()` - Processes structured tool_calls
- `handle_json_fallback()` - Processes fallbacks
- `_parse_named_args()` - Parser for key=value
- `_parse_positional_args()` - Parser for positional arguments
- `_handle_function_call()` - REGEX parser for function strings
- `execute_tool()` - Executes mapped function

See [docs/ARCHITECTURE.md](ARCHITECTURE.md) for full context.
