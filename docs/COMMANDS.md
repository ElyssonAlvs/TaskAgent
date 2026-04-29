# Commands Reference

## Available Commands

| Intent | Example | Tool Called |
|--------|---------|------------|
| **List all tasks** | "list my tasks" / "show all tasks" | `list_tasks()` |
| **Filter by status** | "show pending tasks" / "in progress tasks" | `list_tasks(status="pending")` |
| **Create task** | "create task: Study Python" / "new task called Test" | `create_task(title="...")` |
| **View specific** | "show task 1" / "get task with id 5" | `get_task(task_id=5)` |
| **Update task** | "update task 2 status to done" / "mark as in_progress" | `update_task(task_id=2, status="done")` |
| **Delete task** | "delete task 3" / "remove task 5" | `delete_task(task_id=3)` |

## Status Values

- `pending` - Tarefa não iniciada
- `in_progress` - Tarefa em andamento
- `done` - Tarefa concluída

## Examples

### Create
```
>>> create task: Morning workout
Tarefa criada: Morning workout (ID: 1)

>>> create a task called Review code with description "Check PR #42"
Tarefa criada: Review code (ID: 2)
```

### List
```
>>> list my tasks
Tarefas (3):
[1] Morning workout (pending)
[2] Review code (pending)
[3] Meeting (done)

>>> show in_progress tasks
Tarefas (1):
[2] Review code (in_progress)
```

### Get
```
>>> show task 2
[2] Review code
Status: in_progress
Descrição: Check PR #42
```

### Update
```
>>> update task 1 to done
Tarefa 1 atualizada: Morning workout (Status: done)
```

### Delete
```
>>> delete task 3
Tarefa 3 deletada
```

## Natural Language Support

O agente entende múltiplas variações de linguagem natural:
- Português e Inglês
- Formas diferentes de pedir a mesma coisa
- Abreviações (ex: "task" = "tarefa")

**Não funciona com:**
- Requisições muito vagas
- Múltiplas ações em um comando
- Idiomas diferentes dos suportados
