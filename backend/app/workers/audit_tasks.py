from sqlalchemy import select
from app.config.celery import celery_app
from app.config.db_sync import SessionLocal
from app.services.audit_service import AuditService
from app.models.api_endpoint import ApiEndpoints
from app.models.dead_letter import DeadLetterTask


@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def run_audit_task(self, api_id: int):
    db = SessionLocal()
    try:
        AuditService.run_audit_sync(api_id, db)
    except Exception as exc:
        db.rollback()
        if self.request.retries >= self.max_retries:
            _send_to_dlq(api_id, exc, self.request.retries)
        raise self.retry(exc=exc)
    finally:
        db.close()


@celery_app.task
def run_all_audits():
    db = SessionLocal()
    try:
        apis = db.execute(select(ApiEndpoints)).scalars().all()
        for api in apis:
            run_audit_task.delay(api.id)
    finally:
        db.close()


def _send_to_dlq(api_id: int, exc: Exception, retries: int):
    db = SessionLocal()
    try:
        db.add(
            DeadLetterTask(
                task_name="run_audit_task",
                payload=str({"api_id": api_id}),
                error=str(exc),
                retry_count=retries,
            )
        )
        db.commit()
    finally:
        db.close()
