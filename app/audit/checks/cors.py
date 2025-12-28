import requests
from app.audit.checks.base import BaseCheck

class CORSMisconfigurationCheck(BaseCheck):
    name = "cors_misconfiguration"
    severity = "high"

    def execute(self, api):
        try:
            headers = {"Origin": "https://evil.com"}
            response = requests.get(api.url, headers=headers, timeout=5)

            acao = response.headers.get("Access-Control-Allow-Origin")

            if acao == "*" or acao == "https://evil.com":
                return {
                    "passed": False,
                    "details": {"issue": "Overly permissive CORS policy"},
                }

            return {
                "passed": True,
                "details": {"message": "CORS policy looks safe"},
            }

        except Exception as e:
            return {
                "passed": False,
                "details": {"error": str(e)},
            }
