from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate


FREE_PLAN_LIMIT = 3


def enforce_project_limit(db: Session, user: User) -> None:
    if user.plan == "paid":
        return
    count = db.query(Project).count()
    if count >= FREE_PLAN_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="FREE_LIMIT_REACHED",
        )


def get_all_projects(db: Session) -> list[Project]:
    return (
        db.query(Project)
        .order_by(Project.created_at.desc())
        .all()
    )


def get_project_by_id(db: Session, project_id: int) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project


def create_project(db: Session, data: ProjectCreate, user: User) -> Project:
    enforce_project_limit(db, user)
    project = Project(
        name=data.name,
        client_name=data.client_name,
        deadline=data.deadline,
        status=data.status,
        created_by=user.id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(db: Session, project_id: int, data: ProjectUpdate) -> Project:
    project = get_project_by_id(db, project_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: int) -> None:
    project = get_project_by_id(db, project_id)
    db.delete(project)
    db.commit()