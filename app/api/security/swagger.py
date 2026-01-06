from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security import HTTPBearer

bearer_scheme = HTTPBearer(
    scheme_name="BearerAuth",
    description="Enter: Bearer <JWT token>"
)
