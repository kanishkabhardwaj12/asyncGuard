import requests
from app.audit.checks.base import BaseCheck

class RateLimitingCheck(BaseCheck):
    name = "rate_limiting"
    severity = "high"

    def execute(self, api):
        try:
            response = requests.get(api.url, timeout=5)

            rate_headers = [
                "x-ratelimit-limit",
                "x-ratelimit-remaining",
                "retry-after",
            ]

            present = any(h in response.headers for h in rate_headers)

            if not present:
                return {
                    "passed": False,
                    "details": {"issue": "No rate limiting headers detected"},
                }

            return {
                "passed": True,
                "details": {"message": "Rate limiting headers present"},
            }

        except Exception as e:
            return {
                "passed": False,
                "details": {"error": str(e)},
            }
