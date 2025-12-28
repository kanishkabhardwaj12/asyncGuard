from app.audit.registry import CHECK_REGISTRY
from app.models.audit_result import AuditResult

SEVERITY_WEIGHTS = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}

class AuditRunner:
    @staticmethod
    def run(api, audit_run, db):
        total_weight = 0
        deductions = 0
        
        for check in CHECK_REGISTRY:
            total_weight += SEVERITY_WEIGHTS.get(check.severity, 1)

        for check in CHECK_REGISTRY:
            result = check.execute(api)
            weight = SEVERITY_WEIGHTS.get(check.severity, 1)
            if not result["passed"]:
                deductions += (weight / total_weight) * 100
            db.add(
                AuditResult(
                    audit_run_id=audit_run.id,
                    check_name=check.name,
                    passed=result["passed"],
                    severity=check.severity,
                    details=result["details"],
                )
            )
        audit_run.score = max(round(100 - deductions, 2), 0)
        db.commit()
