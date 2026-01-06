from functools import wraps
from fastapi import Request, HTTPException

def authorize(roles=None, permissions=None):
    roles = roles or []
    permissions = permissions or []

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            user = request.state.user

            if roles and user["role"] not in roles:
                raise HTTPException(403, "Role not allowed")

            if permissions:
                for p in permissions:
                    if p not in user.get("permissions", []):
                        raise HTTPException(403, f"Missing permission: {p}")

            return await func(*args, **kwargs)
        return wrapper
    return decorator
