import requests
from app.audit.checks.base import BaseCheck


class CORSCheck(BaseCheck):
    name = "cors_misconfiguration"
    severity = "high"

    def execute(self, api):
        try:
            headers = {
                "Origin": "https://evil.com"
            }

            r = requests.get(api.url, headers=headers, timeout=5)

            allow_origin = r.headers.get("access-control-allow-origin")
            allow_creds = r.headers.get("access-control-allow-credentials")

            issues = []

            if allow_origin == "*":
                issues.append("Wildcard ACAO")

            if allow_origin == "https://evil.com":
                issues.append("Reflected Origin")

            if allow_creds == "true" and allow_origin in ("*", "https://evil.com"):
                issues.append("Credentials allowed with insecure origin")

            if issues:
                return {
                    "passed": False,
                    "details": {
                        "issues": issues,
                        "allow_origin": allow_origin,
                        "allow_credentials": allow_creds,
                    },
                }

            return {
                "passed": True,
                "details": {
                    "message": "No dangerous CORS misconfiguration detected",
                    "allow_origin": allow_origin,
                    "allow_credentials": allow_creds,
                },
            }

        except Exception as e:
            return {
                "passed": False,
                "details": {"error": str(e)},
            }
