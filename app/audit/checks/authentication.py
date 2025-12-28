import requests
from app.audit.checks.base import BaseCheck

class AuthenticationRequiredCheck(BaseCheck):
    name = "authentication_required"
    severity = "critical"

    def execute(self, api):
        try:
            response = requests.get(api.url, timeout=5)

            if response.status_code in (401, 403):
                return {
                    "passed": True,
                    "details": {"message": "Authentication enforced"},
                }

            return {
                "passed": False,
                "details": {
                    "issue": "Endpoint accessible without authentication",
                    "status_code": response.status_code,
                },
            }

        except Exception as e:
            return {
                "passed": False,
                "details": {"error": str(e)},
            }
