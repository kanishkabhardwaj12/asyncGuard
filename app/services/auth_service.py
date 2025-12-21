from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status, Response

from app.models.user import User, UserRole
from app.schemas.auth import SignupRequest, SignupResponse, LoginRequest
from app.helpers.jwt import create_access_token
from app.helpers.hashing import verify_password, hash_password
from app.config.settings import settings


class AuthService:
    @staticmethod
    async def signup(
        data: SignupRequest,
        db: AsyncSession
    ) -> SignupResponse:
        result = await db.execute(
            select(User).where(User.email == data.email)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            role=UserRole.viewer,
            org_id=None,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return SignupResponse(
            id=user.id,
            email=user.email,
            role=user.role.value,
            org_id=user.org_id,
        )

    @staticmethod
    async def login(
        data: LoginRequest,
        response: Response,
        db: AsyncSession
    ) -> dict:
        result = await db.execute(
            select(User).where(User.email == data.email)
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(
            data.password, user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        token = create_access_token(
            data={
                "sub": user.email,
                "user_id": user.id,
                "role": user.role.value,
            }
        )

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=False,
            secure=not settings.DEBUG,
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

        return {"message": "Logged in successfully"}

    @staticmethod
    async def logout(response: Response) -> dict:
        response.delete_cookie(
            key="access_token",
            httponly=False,
            secure=not settings.DEBUG,
            samesite="lax",
        )
        return {"message": "Logged out successfully"}
