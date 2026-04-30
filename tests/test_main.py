import os
os.environ["DATABASE_URL"] = "postgresql://postgres:2003@localhost:5432/taskmanager"
os.environ["SECRET_KEY"] = "testsecretkey123"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

from fastapi.testclient import TestClient

def test_health_check():
    from app.main import app
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root():
    from app.main import app
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200