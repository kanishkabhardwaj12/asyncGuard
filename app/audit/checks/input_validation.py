import requests
from app.audit.checks.base import BaseCheck

class InputValidationCheck(BaseCheck):
    name = "input_validation"
    severity = "high"

    def execute(self, api):
        results = []

        try:
            
            r1 = requests.post(
                api.url,
                data="{invalid_json",
                headers={"Content-Type": "application/json"},
                timeout=5,
            )
            results.append(("invalid_json", r1.status_code))

           
            r2 = requests.post(
                api.url,
                json={},
                timeout=5,
            )
            results.append(("empty_body", r2.status_code))

            
            r3 = requests.post(
                api.url,
                json={"id": "string_instead_of_int"},
                timeout=5,
            )
            results.append(("type_mismatch", r3.status_code))


            accepted = [
                name for name, code in results if code < 400
            ]

            if accepted:
                return {
                    "passed": False,
                    "details": {
                        "accepted_invalid_inputs": accepted,
                        "results": results,
                    },
                }

            return {
                "passed": True,
                "details": {
                    "message": "API rejects malformed input correctly",
                    "results": results,
                },
            }

        except Exception as e:
            return {
                "passed": False,
                "details": {"error": str(e)},
            }
