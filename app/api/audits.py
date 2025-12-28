from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.auth import get_current_user
from app.models.user import User
from app.services.audit_service import AuditService
from app.config.db import get_db
from app.workers.audit_tasks import run_audit_task
from fastapi import HTTPException
from app.models.user import UserRole

router = APIRouter(prefix="/audits", tags=["Audits"])

@router.post("/run/{api_id}", status_code=status.HTTP_202_ACCEPTED)
async def run_audit(api_id: int, user: User = Depends(get_current_user)):
    if user.role != UserRole.admin:
        raise HTTPException(403, "Only admins can run audits")
    
    run_audit_task.delay(api_id)
    return {"message": "Audit scheduled"}

@router.get("/results/{api_id}", status_code=status.HTTP_200_OK)
async def get_audit_results(api_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await AuditService.get_audit_results(api_id, user, db)

@router.get("/results", status_code=status.HTTP_200_OK)
async def get_all_audit_results(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await AuditService.get_all_audit_results(user, db)