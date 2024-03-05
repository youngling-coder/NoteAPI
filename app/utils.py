from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(plain: str):
    return pwd_context.hash(plain)


def verify(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)
