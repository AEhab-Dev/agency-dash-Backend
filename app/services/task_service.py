from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks_by_project(db: Session, project_id: int) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .order_by(Task.created_at.asc())
        .all()
    )


def get_task_by_id(db: Session, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


def create_task(db: Session, project_id: int, data: TaskCreate) -> Task:
    task = Task(
        project_id=project_id,
        title=data.title,
        assignee=data.assignee,
        due_date=data.due_date,
        status=data.status,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: int, data: TaskUpdate) -> Task:
    task = get_task_by_id(db, task_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def complete_task(db: Session, task_id: int) -> Task:
    task = get_task_by_id(db, task_id)
    task.status = "Done"
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> None:
    task = get_task_by_id(db, task_id)
    db.delete(task)
    db.commit()