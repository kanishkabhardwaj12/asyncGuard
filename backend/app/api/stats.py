from fastapi import APIRouter, Depends, Response, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.api_endpoint import ApiEndpoints
from app.models.audit_run import AuditRun
from app.config.db import get_db
from sqlalchemy import select, func
from app.services.stats_service import StatsService

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/overview")
async def get_overview_stats(db: AsyncSession = Depends(get_db)):
   return await StatsService.get_global_overview(db)