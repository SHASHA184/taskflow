from app.models.user import User
from app.services.base_service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.user import UserCreate
from fastapi import HTTPException
from app.utils import verify_password, get_password_hash


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
