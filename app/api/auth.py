from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_db
from app.schemas.auth import SignupRequest, SignupResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup",response_model=SignupResponse)
async def signup(data:SignupRequest , db : AsyncSession=Depends(get_db)):
    return await AuthService.signup(data,db)
