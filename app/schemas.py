from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ─── Auth ───
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    role: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# ─── Projects ───
class ProjectCreate(BaseModel):
    name: str

class ProjectOut(BaseModel):
    id: int
    name: str
    owner_id: int
    created_at: datetime
    class Config:
        from_attributes = True

# ─── Tasks ───
class TaskCreate(BaseModel):
    title: str
    project_id: int
    assignee_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    assignee_id: Optional[int] = None

class TaskOut(BaseModel):
    id: int
    title: str
    status: str
    project_id: int
    assignee_id: Optional[int]
    created_at: datetime
    class Config:
        from_attributes = True

# ─── Activity ───
class ActivityOut(BaseModel):
    id: int
    user_id: int
    action: str
    entity_type: str
    entity_id: Optional[int]
    timestamp: datetime
    class Config:
        from_attributes = True