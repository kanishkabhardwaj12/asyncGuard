import time
import requests
from app.audit.checks.base import BaseCheck


class RateLimitingCheck(BaseCheck):
    name = "rate_limiting"
    severity = "high"

    MAX_REQUESTS = 10          
    WINDOW_SECONDS = 2         
    TIMEOUT = 5

    def execute(self, api):
        responses = []
        throttled_at = None

        try:
            for i in range(self.MAX_REQUESTS):
                resp = requests.get(api.url, timeout=self.TIMEOUT)
                responses.append(resp.status_code)

                
                if resp.status_code in (429, 403):
                    throttled_at = i + 1
                    break

                time.sleep(self.WINDOW_SECONDS / self.MAX_REQUESTS)

            
            if throttled_at:
                return {
                    "passed": True,
                    "details": {
                        "method": "burst_test",
                        "throttled_at_request": throttled_at,
                        "status_codes": responses,
                    },
                }

            
            return {
                "passed": False,
                "details": {
                    "method": "burst_test",
                    "issue": "No throttling observed during burst",
                    "status_codes": responses,
                    "note": "Rate limiting may exist but is not externally detectable",
                },
            }

        except Exception as e:
            return {
                "passed": False,
                "details": {
                    "error": str(e),
                    "method": "burst_test",
                },
            }
