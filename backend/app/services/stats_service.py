from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.api_endpoint import ApiEndpoints
from app.models.audit_run import AuditRun

class StatsService:

    @staticmethod
    async def get_global_overview(db: AsyncSession):
        api_count_stmt = select(func.count(ApiEndpoints.id))
        audit_count_stmt = select(func.count(AuditRun.id))

        api_count = await db.scalar(api_count_stmt)
        audit_count = await db.scalar(audit_count_stmt)

        return {
            "apis_registered": api_count,
            "audits_performed": audit_count
        }

    