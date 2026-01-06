from datetime import datetime, timedelta
from jose import jwt
from app.api.security.jwt_bearer import SECRET_KEY
from app.config.authconfig import JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_HOURS = 1

class TokenGenerator:
    def __init__(self):
        pass