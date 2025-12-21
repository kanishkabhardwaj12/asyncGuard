from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User, UserRole
from app.schemas.auth import SignupRequest, SignupResponse
from app.helpers.hashing import hash_password

class AuthService:
    @staticmethod
    async def signup(data:SignupRequest , db :AsyncSession)->SignupResponse:
        result = await db.execute(select(User).where(User.email==data.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="user already exists")
        hashed_pass=hash_password(data.password)
        user = User(
            email=data.email,
            hashed_password=hashed_pass,
            role=UserRole.viewer,
            org_id=None
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return SignupResponse(
            id=user.id,
            email=user.email,
            role=user.role.value,
            org_id=user.org_id
            
        )
    
        