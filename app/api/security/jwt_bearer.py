from datetime import datetime, timedelta
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError

from app.config.authconfig import JWT_ALGORITHM, SECRET_KEY
from app.utility.auth import ACCESS_TOKEN_EXPIRE_HOURS

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials or credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=401,
                detail="Missing or invalid token"
            )

        token = credentials.credentials

        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[JWT_ALGORITHM]
            )
            request.state.user = payload
            return payload

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
def generate_token(user: dict) -> str:
    payload = {
        "sub": user["sub"],
        "role": user["role"],
        "permissions": user["permissions"],
        "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

