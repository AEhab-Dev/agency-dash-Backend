from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.models import user, project, task
from app.routers import auth, projects, tasks, payments, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AgencyDash API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(payments.router)
app.include_router(dashboard.router)


@app.get("/health")
def health():
    return {"status": "ok"}