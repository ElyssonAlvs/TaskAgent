from openai import OpenAI
import json
import re
from typing import Optional, Dict, Any
from src.tools.task_tools import create_task, list_tasks, delete_task, get_task, update_task

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_task",
            "description": "Get complete details of a specific task by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "Task ID"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Create a new task",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Optional description"},
                    "status": {"type": "string", "description": "Status: pending, in_progress or done"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks with optional filters",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "Filter by status: pending, in_progress or done"},
                    "skip": {"type": "integer"},
                    "limit": {"type": "integer"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update an existing task (title, description or status)",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "Task ID to update"},
                    "title": {"type": "string", "description": "New task title"},
                    "description": {"type": "string", "description": "New task description"},
                    "status": {"type": "string", "description": "New status: pending, in_progress or done"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "Task ID to delete"}
                },
                "required": ["task_id"]
            }
        }
    }
]

SYSTEM_PROMPT = """You are an assistant that MUST call functions.
Your job is to interpret the user's command and call the correct function.

RULES:
1. User wants to see ONE specific task? Call: get_task(task_id=...)
2. User wants to list tasks? Call: list_tasks() or list_tasks(status="pending")
3. User wants to create task? Call: create_task(title="...", description="...", status="pending")
4. User wants to delete task? Call: delete_task(task_id=...)
5. User wants to update task? Call: update_task(task_id=..., status="...")

NEVER respond with text. ALWAYS use a function.
NEVER explain what you will do.
"""

# Mapa de ferramentas disponíveis
TOOL_FUNCTIONS = {
    "get_task": get_task,
    "create_task": create_task,
    "update_task": update_task,
    "list_tasks": list_tasks,
    "delete_task": delete_task,
}


def execute_tool(name: str, args: dict) -> str:
    """Executa uma ferramenta pelo nome com os argumentos fornecidos."""
    tool_func = TOOL_FUNCTIONS.get(name)
    if not tool_func:
        return "Unknown tool"
    try:
        return tool_func(**args)
    except Exception as e:
        return f"Erro ao executar {name}: {str(e)}"


def parse_json_response(content_str: str) -> Optional[Dict]:
    """Parseia JSON de resposta como texto."""
    try:
        content_str = content_str.strip()
        if not content_str:
            return None

        if content_str.startswith('['):
            parsed_list = json.loads(content_str)
            if parsed_list and isinstance(parsed_list, list):
                return parsed_list[0]
            return None

        return json.loads(content_str)
    except (json.JSONDecodeError, IndexError, TypeError):
        return None


def handle_tool_call(tool_call: Any) -> str:
    """Process a structured tool call."""
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    return execute_tool(name, args)


def _parse_named_args(args_str: str) -> Dict:
    """Parse named arguments: task_id=1, title="foo" """
    args = {}
    for pair in args_str.split(','):
        if '=' not in pair:
            continue
        parts = pair.strip().split('=', 1)
        key, value = parts[0].strip(), parts[1].strip()
        try:
            args[key] = int(value)
        except ValueError:
            args[key] = value.strip('"\'')
    return args


def _parse_positional_args(func_name: str, positional_args: list) -> Dict:
    """Map positional arguments to named based on function name."""
    args = {}

    if func_name in ("get_task", "delete_task"):
        try:
            args["task_id"] = int(positional_args[0])
        except (ValueError, IndexError):
            args["task_id"] = positional_args[0] if positional_args else 0

    elif func_name == "create_task":
        if len(positional_args) > 0:
            args["title"] = positional_args[0].strip('"\'')
            if len(positional_args) > 1:
                args["description"] = positional_args[1].strip('"\'')

    elif func_name == "list_tasks" and len(positional_args) > 0:
        args["status"] = positional_args[0].strip('"\'')

    return args


def _handle_function_call(func_str: str) -> Optional[str]:
    """Process string with function call: get_task(1) or get_task(task_id=1)"""
    match = re.match(r'(\w+)\((.*)\)', func_str.strip())
    if not match:
        return None

    name, args_str = match.group(1), match.group(2).strip()

    if not args_str:
        return execute_tool(name, {})

    # Named vs positional arguments
    if '=' in args_str:
        args = _parse_named_args(args_str)
    else:
        positional = [arg.strip() for arg in args_str.split(',')]
        args = _parse_positional_args(name, positional)

    return execute_tool(name, args)


def handle_json_fallback(message_content: str) -> str:
    """Process fallback when model returns JSON or Python function as text."""
    content_str = message_content.strip()

    # Try to parse as JSON
    parsed = parse_json_response(content_str)
    if parsed and "name" in parsed:
        name = parsed["name"]
        args = parsed.get("arguments", {})
        return execute_tool(name, args)

    # Try to parse as Python function
    result = _handle_function_call(content_str)
    if result is not None:
        return result

    return f"Error processing: {message_content}"


def run_agent(user_input: str) -> str:
    """Run the agent with user input."""
    response = client.chat.completions.create(
        model="mistral",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        tools=tools,
        tool_choice="required"
    )

    message = response.choices[0].message

    if message.tool_calls:
        return handle_tool_call(message.tool_calls[0])

    if message.content:
        return handle_json_fallback(message.content)

    return "Error: No response from model"


if __name__ == "__main__":
    while True:
        user_input = input(">>> ")
        result = run_agent(user_input)
        print(result)
