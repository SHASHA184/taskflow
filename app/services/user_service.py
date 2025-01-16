from app.models.user import User
from app.services.base_service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.user import UserCreate
from fastapi import HTTPException
from app.utils import verify_password, get_password_hash
from sqlalchemy.orm import selectinload


class UserService(BaseService):
    def __init__(self, db):
        super().__init__(db, User)

    def create(self, user_create: UserCreate):
        """Create a new user."""
        user_create.password = get_password_hash(user_create.password)
        return super().create(user_create)

    async def authenticate_user(self, db: AsyncSession, username: str, password: str):
        """Authenticate a user by username and password."""
        query = select(User).filter(User.name == username)
        user = await db.execute(query)
        user = user.scalars().first()
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )
        return user

    async def get_user_with_tasks(self, db: AsyncSession, user_id: int):
        """Get user details along with their tasks."""
        query = select(User).filter(User.id == user_id).options(selectinload(User.tasks))
        result = await db.execute(query)
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
