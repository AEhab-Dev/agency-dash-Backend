from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.services.task_service import (
    get_tasks_by_project,
    create_task,
    update_task,
    complete_task,
    delete_task,
)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/project/{project_id}", response_model=list[TaskOut])
def list_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_tasks_by_project(db, project_id)


@router.post("/project/{project_id}", response_model=TaskOut, status_code=201)
def create(
    project_id: int,
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_task(db, project_id, data)


@router.put("/{task_id}", response_model=TaskOut)
def update(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_task(db, task_id, data)


@router.patch("/{task_id}/complete", response_model=TaskOut)
def complete(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return complete_task(db, task_id)


@router.delete("/{task_id}", status_code=204)
def delete(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_task(db, task_id)