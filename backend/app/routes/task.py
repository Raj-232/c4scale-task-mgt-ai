from fastapi import APIRouter
from schemas.task import CreateTaskInput, UpdateTaskInput, DeleteTaskInput, FilterTasksInput
from services.task.task_crud import create_task, list_tasks, update_task, delete_task, filter_tasks

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/create")
def create_task_api(task: CreateTaskInput):
    return create_task(task)

@router.get("/list")
def list_tasks_api(page: int = 1, page_size: int = 100):
    return list_tasks(page, page_size)

@router.put("/update")
def update_task_api(task: UpdateTaskInput):
    return update_task(task)

@router.delete("/delete")
def delete_task_api(task: DeleteTaskInput):
    return delete_task(task)

@router.post("/filter")
def filter_tasks_api(filters: FilterTasksInput, page: int = 1, page_size: int = 100):
    return filter_tasks(filters, page, page_size)
