from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    max_tasks: int


class UserUpdate(BaseModel):
    max_tasks: int


class UserInDB(UserCreate):
    id: int

    class Config:
        from_attributes = True
