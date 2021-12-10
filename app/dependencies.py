from app.setup_db import SessionLocal
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.constants import JWT_KEY, JWT_METHOD
from fastapi import HTTPException, status, Depends
from app.service.rtokens import RTokenService
from sqlalchemy.orm import Session
from app.service.users import UserService


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    # except:
    #     db.rollback()
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login_oauth2')


def jwt_decode(token: str):
    try:
        decoded_jwt = jwt.decode(token, JWT_KEY, [JWT_METHOD])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return decoded_jwt


# use it as dependency when authorization required
def valid_token(token: str = Depends(oauth2_scheme)):
    return jwt_decode(token)


# use it as dependency when admin authorization required
def valid_admin_token(token: str = Depends(oauth2_scheme)):
    role = jwt_decode(token).get('role')
    if role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin Role Required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


def get_current_user(token=Depends(valid_token), db: Session = Depends(get_db)):
    return UserService(db).get_all_by_filter({'email': token.get('email')})[0]


def del_expired_tokens():
    db = SessionLocal()
    RTokenService(db).del_expired()
    db.close()
