from models.task import Task
from utils.db_connection import SessionLocal as get_db
from utils.crud import CRUDBase
from schemas.task import CreateTaskInput, UpdateTaskInput, DeleteTaskInput, FilterTasksInput
from datetime import datetime

crud_task = CRUDBase(Task)

# --- CREATE TASK ---
def create_task(title: str, description: str, priority: str = "medium", due_date: str | None = None):
    db = get_db()

    # Parse due_date safely
    parsed_due_date = None
    if due_date:
        try:
            parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return {"error": f"❌ Invalid date format '{due_date}'. Use YYYY-MM-DD."}

    # Create ORM object
    task_dict = {
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": parsed_due_date,
    }

    # Use CRUDBase create
    db_obj = crud_task.create(db, obj_in=CreateTaskInput(**{
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
    }))

    # After insert, update due_date (since schema takes string)
    db_obj.due_date = parsed_due_date
    db.commit()
    db.refresh(db_obj)

    return {"message": f"✅ Task '{db_obj.title}' created.", "task_id": db_obj.id}


# --- LIST TASKS ---
def list_tasks():
    db = get_db()
    tasks = crud_task.get_all(db)
    return [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "priority": t.priority,
            "status": t.status,
            "due_date": t.due_date,
        }
        for t in tasks
    ]


# --- UPDATE TASK ---
def update_task(task_id: int, title: str | None = None, description: str | None = None,
                priority: str | None = None, due_date: str | None = None, status: str | None = None):
    db = get_db()

    update_data = {}
    if title is not None:
        update_data["title"] = title
    if description is not None:
        update_data["description"] = description
    if priority is not None:
        update_data["priority"] = priority
    if status is not None:
        update_data["status"] = status
    if due_date:
        try:
            update_data["due_date"] = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return {"error": f"❌ Invalid date format '{due_date}'. Use YYYY-MM-DD."}

    updated_task = crud_task.update(db, id=task_id, obj_in=UpdateTaskInput(**{
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "task_id": task_id,
        "status": status
    }))

    if not updated_task:
        return {"error": "❌ Task not found."}

    return {"message": f"✅ Task '{updated_task.title}' updated."}


# --- DELETE TASK ---
def delete_task(task_id: int):
    db = get_db()
    deleted_task = crud_task.delete(db, id=task_id)
    if not deleted_task:
        return {"error": "❌ Task not found."}
    return {"message": f"🗑️ Task '{deleted_task.title}' deleted."}


# --- FILTER TASKS ---
def filter_tasks(status: str | None = None, priority: str | None = None, due_date: str | None = None):
    db = get_db()
    filters = FilterTasksInput(status=status, priority=priority, due_date=due_date)
    # Reuse CRUD directly for tools to keep symmetry with API
    filter_dict = {}
    if filters.status:
        filter_dict["status"] = filters.status
    if filters.priority:
        filter_dict["priority"] = filters.priority
    if filters.due_date:
        try:
            datetime.strptime(filters.due_date, "%Y-%m-%d")
            filter_dict["due_date"] = filters.due_date
        except ValueError:
            return {"error": f"❌ Invalid date format '{filters.due_date}'. Use YYYY-MM-DD."}
    tasks = crud_task.get_all(db, filters=filter_dict or None)
    return [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "priority": t.priority,
            "status": t.status,
            "due_date": t.due_date,
        }
        for t in tasks
    ]
