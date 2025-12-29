import requests
from app.audit.checks.base import BaseCheck


class AuthenticationRequiredCheck(BaseCheck):
    name = "authentication_required"
    severity = "critical"

    AUTH_KEYWORDS = [
        "unauthorized",
        "authentication required",
        "access denied",
        "forbidden",
        "login required",
    ]

    def execute(self, api):
        try:
            r = requests.get(
                api.url,
                timeout=5,
                allow_redirects=False,
            )

            
            if r.status_code in (401, 403):
                return {
                    "passed": True,
                    "details": {"message": "Authentication enforced (status code)"},
                }

            
            if r.status_code in (301, 302, 307, 308):
                location = r.headers.get("Location", "").lower()
                if "login" in location or "auth" in location:
                    return {
                        "passed": True,
                        "details": {"message": "Authentication enforced (redirect)"},
                    }

            
            body = r.text.lower()
            if any(keyword in body for keyword in self.AUTH_KEYWORDS):
                return {
                    "passed": True,
                    "details": {"message": "Authentication enforced (response body)"},
                }

            
            return {
                "passed": False,
                "details": {
                    "issue": "Endpoint appears accessible without authentication",
                    "status_code": r.status_code,
                },
            }

        except Exception as e:
            return {
                "passed": False,
                "details": {"error": str(e)},
            }
