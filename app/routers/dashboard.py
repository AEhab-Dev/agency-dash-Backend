from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.task import Task

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()
    week_end = today + timedelta(days=7)

    total_projects = db.query(Project).count()

    due_this_week = (
        db.query(Task)
        .filter(Task.due_date >= today, Task.due_date <= week_end)
        .filter(Task.status != "Done")
        .count()
    )

    overdue = (
        db.query(Task)
        .filter(Task.due_date < today)
        .filter(Task.status != "Done")
        .count()
    )

    recent_projects = (
        db.query(Project)
        .order_by(Project.created_at.desc())
        .limit(5)
        .all()
    )

    return {
        "total_projects": total_projects,
        "due_this_week": due_this_week,
        "overdue": overdue,
        "recent_projects": [
            {
                "id": p.id,
                "name": p.name,
                "client_name": p.client_name,
                "deadline": p.deadline.isoformat(),
                "status": p.status,
                "created_at": p.created_at.isoformat(),
            }
            for p in recent_projects
        ],
    }