from app.setup_db import SessionLocal
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.constants import JWT_KEY, JWT_METHOD
from fastapi import HTTPException, status, Depends
from app.service.rtokens import RTokenService
from sqlalchemy.orm import Session
from app.service.users import UserService
from app.dao.model.rtokens import TokenModel


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except:  # noqa
        db.rollback()
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login_oauth2")


def jwt_decode(token: str) -> TokenModel:
    try:
        decoded_jwt = jwt.decode(token, JWT_KEY, [JWT_METHOD])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return TokenModel.parse_obj(decoded_jwt)
        # return decoded_jwt


def valid_token(token: str = Depends(oauth2_scheme)) -> TokenModel:
    """
    use it as dependency when authorization required
    """
    return jwt_decode(token)


def valid_admin_token(token: str = Depends(oauth2_scheme)):
    """
    use it as dependency when admin authorization required
    """
    role = jwt_decode(token).role
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin Role Required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


def get_current_user(
    token: TokenModel = Depends(valid_token), db: Session = Depends(get_db)
):
    # return UserService(db).get_all_by_filter({'email': token.get('email')})[0]
    return UserService(db).get_all_by_filter({"email": token.email})[0]


def del_expired_tokens():
    db = SessionLocal()
    RTokenService(db).del_expired()
    db.close()
