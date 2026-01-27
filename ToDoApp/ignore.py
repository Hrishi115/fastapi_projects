from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated="auto"
)

def hash_pass(password: str):
    return pwd_context.hash(password)

def verify_pass(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)


SECRET_KEY = "be26fc73cb2f8ca2c22a653ba9afe795"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expiry = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(
        {
            "exp": expiry
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload

# if __name__ == '__main__':
#     token = create_access_token(
#         {
#             "user_id": 1,
#             "email": "User@gmail.com",
#             "name": "User1"
#         }
#     )
#
#     print(decode_token(token))
#
# if __name__ == '__main__':
#     print(hash_pass("Secret123"))
#     hashed = "$2b$12$gq0Cj3E6m08aTGQp7d6jTOCRXuMEm/.BwiPhrtZqi1ZwrHWOE93iO"
#
#     print(verify_pass("Secret123", hashed))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth")

@router.get("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = {
        "user": form_data.username,
        "password": form_data.password,
        "scope": form_data.scopes
    }

    token = create_access_token(data=user)

    return {"access_token": token, "token_type": "bearer"}

def get_user_through_login(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return payload