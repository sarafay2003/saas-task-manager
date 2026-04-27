from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, projects, tasks, activity

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SaaS Task Manager", version="1.0.0")

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(activity.router)

@app.get("/")
def root():
    return {"message": "Task Manager API is running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}