import requests

BASE_URL = "http://localhost:8000/v1"
REQUEST_TIMEOUT = 5


def get_task(task_id: int):
    """Get details of a specific task"""
    try:
        response = requests.get(
            f"{BASE_URL}/tasks/{task_id}", timeout=REQUEST_TIMEOUT)
        task = response.json()

        if "detail" in task:
            return f"Task {task_id} not found"

        return f"[{task['id']}] {task['title']}\nStatus: {task['status']}\nDescription: {task.get('description', 'N/A')}"
    except Exception as e:
        return f"Error: {str(e)}"


def create_task(title: str, description: str = "", status: str = "pending"):
    try:
        response = requests.post(
            f"{BASE_URL}/tasks/",
            json={"title": title, "description": description, "status": status},
            timeout=REQUEST_TIMEOUT
        )
        task = response.json()
        return f"Task created: {task['title']} (ID: {task['id']})"
    except Exception as e:
        return f"Error: {str(e)}"


def list_tasks(status: str = None, skip: int = 0, limit: int = 10):
    try:
        params = {"skip": skip, "limit": limit}
        if status:
            params["status"] = status

        response = requests.get(
            f"{BASE_URL}/tasks/", params=params, timeout=REQUEST_TIMEOUT)
        tasks = response.json()

        if not tasks:
            return "No tasks"

        result = f"Tasks ({len(tasks)}):\n"
        for task in tasks:
            result += f"[{task['id']}] {task['title']} ({task['status']})\n"

        return result.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def update_task(task_id: int, title: str = None, description: str = None, status: str = None):
    """Update an existing task"""
    try:
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if status is not None:
            update_data["status"] = status

        if not update_data:
            return "No fields to update"

        response = requests.put(
            f"{BASE_URL}/tasks/{task_id}",
            json=update_data,
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code == 200:
            task = response.json()
            return f"Task {task_id} updated: {task['title']} (Status: {task['status']})"
        else:
            return f"Error updating: {response.json().get('detail', 'Unknown error')}"
    except Exception as e:
        return f"Error: {str(e)}"


def delete_task(task_id: int):
    try:
        response = requests.delete(
            f"{BASE_URL}/tasks/{task_id}", timeout=REQUEST_TIMEOUT)
        if response.status_code == 204:
            return f"Task {task_id} deleted"
        else:
            return "Error deleting"
    except Exception as e:
        return f"Error: {str(e)}"
