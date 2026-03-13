from datetime import datetime

from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str
    project_id: int | None = None


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    project_id: int | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotePatch(BaseModel):
    title: str | None = None
    content: str | None = None
    project_id: int | None = None


class ActionItemCreate(BaseModel):
    description: str
    project_id: int | None = None


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool
    project_id: int | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActionItemPatch(BaseModel):
    description: str | None = None
    completed: bool | None = None
    project_id: int | None = None


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class ProjectRead(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectPatch(BaseModel):
    name: str | None = None
    description: str | None = None


