import requests
from app.audit.checks.base import BaseCheck

class InputValidationCheck(BaseCheck):
    name = "input_validation"
    severity = "medium"

    def execute(self, api):
        try:
            payload = {"test": "' OR 1=1 --"}
            response = requests.post(api.url, json=payload, timeout=5)

            if response.status_code >= 500:
                return {
                    "passed": False,
                    "details": {"issue": "Server error on malformed input"},
                }

            return {
                "passed": True,
                "details": {"message": "Input handling seems safe"},
            }

        except Exception as e:
            return {
                "passed": False,
                "details": {"error": str(e)},
            }
