from fastapi import APIRouter, Depends, status

from app.middleware.auth import get_current_user
from app.models.user import User
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