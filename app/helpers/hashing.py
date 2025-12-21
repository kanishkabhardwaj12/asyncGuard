import hashlib
from passlib.context import CryptContext

_pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def _prehash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def hash_password(password: str) -> str:
    prehashed = _prehash(password)
    return _pwd_context.hash(prehashed)

def verify_password(password: str, hashed: str) -> bool:
    prehashed = _prehash(password)
    return _pwd_context.verify(prehashed, hashed)
