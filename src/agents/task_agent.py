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
            "description": "Obtem detalhes completos de uma tarefa especifica pelo ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "ID da tarefa"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Cria uma nova tarefa",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Titulo da tarefa"},
                    "description": {"type": "string", "description": "Descricao opcinal"},
                    "status": {"type": "string", "description": "Status: pending, in_progress ou done"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Lista todas as tarefas com filtros opcionais",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "Filtrar por status: pending, in_progress ou done"},
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
            "description": "Atualiza uma tarefa existente (titulo, descricao ou status)",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "ID da tarefa a atualizar"},
                    "title": {"type": "string", "description": "Novo titulo da tarefa"},
                    "description": {"type": "string", "description": "Nova descricao da tarefa"},
                    "status": {"type": "string", "description": "Novo status: pending, in_progress ou done"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Deleta uma tarefa pelo ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "ID da tarefa a deletar"}
                },
                "required": ["task_id"]
            }
        }
    }
]

SYSTEM_PROMPT = """Você é um assistente que OBRIGATORIAMENTE deve chamar funções.
Seu trabalho é interpretar o comando do usuário e chamar a função correta.

REGRAS:
1. O usuário quer ver UMA tarefa específica? Chame: get_task(task_id=...)
2. O usuário quer listar tarefas? Chame: list_tasks() ou list_tasks(status="pending")
3. O usuário quer criar tarefa? Chame: create_task(title="...", description="...", status="pending")
4. O usuário quer deletar tarefa? Chame: delete_task(task_id=...)

NUNCA responda com texto. SEMPRE use uma função.
NUNCA explique o que vai fazer.
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
    """Processa uma chamada de ferramenta estruturada."""
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    return execute_tool(name, args)


def _parse_named_args(args_str: str) -> Dict:
    """Parseia argumentos nomeados: task_id=1, title="foo" """
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
    """Mapeia argumentos posicionais para nomeados baseado no nome da função."""
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
    """Processa string com chamada de função: get_task(1) ou get_task(task_id=1)"""
    match = re.match(r'(\w+)\((.*)\)', func_str.strip())
    if not match:
        return None

    name, args_str = match.group(1), match.group(2).strip()

    if not args_str:
        return execute_tool(name, {})

    # Argumentos nomeados vs posicionais
    if '=' in args_str:
        args = _parse_named_args(args_str)
    else:
        positional = [arg.strip() for arg in args_str.split(',')]
        args = _parse_positional_args(name, positional)

    return execute_tool(name, args)


def handle_json_fallback(message_content: str) -> str:
    """Processa fallback quando modelo retorna JSON ou função Python como texto."""
    content_str = message_content.strip()

    # Tenta parsear como JSON
    parsed = parse_json_response(content_str)
    if parsed and "name" in parsed:
        name = parsed["name"]
        args = parsed.get("arguments", {})
        return execute_tool(name, args)

    # Tenta parsear como função Python
    result = _handle_function_call(content_str)
    if result is not None:
        return result

    return f"Erro ao processar: {message_content}"


def run_agent(user_input: str) -> str:
    """Executa o agente com entrada do usuário."""
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

    return "Erro: Sem resposta do modelo"


if __name__ == "__main__":
    while True:
        user_input = input(">>> ")
        result = run_agent(user_input)
        print(result)
