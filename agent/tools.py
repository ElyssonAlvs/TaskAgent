import requests

BASE_URL = "http://localhost:8000/v1"
REQUEST_TIMEOUT = 5


def get_task(task_id: int):
    """Obter detalhes de uma tarefa específica"""
    try:
        response = requests.get(
            f"{BASE_URL}/tasks/{task_id}", timeout=REQUEST_TIMEOUT)
        task = response.json()

        if "detail" in task:
            return f"Tarefa {task_id} nao encontrada"

        return f"[{task['id']}] {task['title']}\nStatus: {task['status']}\nDescricao: {task.get('description', 'N/A')}"
    except Exception as e:
        return f"Erro: {str(e)}"


def create_task(title: str, description: str = "", status: str = "pending"):
    try:
        response = requests.post(
            f"{BASE_URL}/tasks/",
            json={"title": title, "description": description, "status": status},
            timeout=REQUEST_TIMEOUT
        )
        task = response.json()
        return f"Tarefa criada: {task['title']} (ID: {task['id']})"
    except Exception as e:
        return f"Erro: {str(e)}"


def list_tasks(status: str = None, skip: int = 0, limit: int = 10):
    try:
        params = {"skip": skip, "limit": limit}
        if status:
            params["status"] = status

        response = requests.get(
            f"{BASE_URL}/tasks/", params=params, timeout=REQUEST_TIMEOUT)
        tasks = response.json()

        if not tasks:
            return "Sem tarefas"

        result = f"Tarefas ({len(tasks)}):\n"
        for task in tasks:
            result += f"[{task['id']}] {task['title']} ({task['status']})\n"

        return result.strip()
    except Exception as e:
        return f"Erro: {str(e)}"


def delete_task(task_id: int):
    try:
        response = requests.delete(
            f"{BASE_URL}/tasks/{task_id}", timeout=REQUEST_TIMEOUT)
        if response.status_code == 204:
            return f"Tarefa {task_id} deletada"
        else:
            return "Erro ao deletar"
    except Exception as e:
        return f"Erro: {str(e)}"
