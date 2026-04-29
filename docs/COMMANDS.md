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

- `pending` - Task not started
- `in_progress` - Task in progress
- `done` - Task completed

## Examples

### Create
```
>>> create task: Morning workout
Task created: Morning workout (ID: 1)

>>> create a task called Review code with description "Check PR #42"
Task created: Review code (ID: 2)
```

### List
```
>>> list my tasks
Tasks (3):
[1] Morning workout (pending)
[2] Review code (pending)
[3] Meeting (done)

>>> show in_progress tasks
Tasks (1):
[2] Review code (in_progress)
```

### Get
```
>>> show task 2
[2] Review code
Status: in_progress
Description: Check PR #42
```

### Update
```
>>> update task 1 to done
Task 1 updated: Morning workout (Status: done)
```

### Delete
```
>>> delete task 3
Task 3 deleted
```

## Natural Language Support

The agent understands multiple variations of natural language:
- Portuguese and English
- Different ways to ask for the same thing
- Abbreviations (ex: "task" = "tarefa")

**Does not work with:**
- Very vague requests
- Multiple actions in one command
- Unsupported languages
