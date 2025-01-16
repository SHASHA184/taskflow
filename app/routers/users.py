from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserUpdate, UserInDB, UserWithTasks
from app.services.user_service import UserService
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/{id}", response_model=UserInDB)
async def read_user(id: int, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = await user_service.get(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{id}/details", response_model=UserWithTasks)
async def read_user_with_tasks(id: int, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return await user_service.get_user_with_tasks(db, id)


@router.post("/", response_model=UserInDB)
async def create_user(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return await user_service.create(user_create)


@router.patch("/{id}", response_model=UserInDB)
async def update_user(
    id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    return await user_service.update(id, user_update)
