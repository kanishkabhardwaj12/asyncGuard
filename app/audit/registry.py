from app.audit.checks.security_headers import SecurityHeadersCheck
from app.audit.checks.cors import CORSMisconfigurationCheck
from app.audit.checks.rate_limit import RateLimitingCheck
from app.audit.checks.authentication import AuthenticationRequiredCheck
from app.audit.checks.input_validation import InputValidationCheck

CHECK_REGISTRY = [
    SecurityHeadersCheck(),
    CORSMisconfigurationCheck(),
    RateLimitingCheck(),
    AuthenticationRequiredCheck(),
    InputValidationCheck(),
]
