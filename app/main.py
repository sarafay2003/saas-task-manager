from fastapi import FastAPI
app = FastAPI(title="SaaS Task Manager", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Task Manager API is running"}

@app.get("/health")
def health():
    return {"statur": "healthy"}
