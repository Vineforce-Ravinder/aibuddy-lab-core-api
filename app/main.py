from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.openapi.utils import get_openapi

from app.api.routes.authentication_router import AuthRouter
from app.api.routes.health import HealthRouter
from app.api.routes.user_router import UserRouter
from app.config import settings
from app.config.logging import setup_logging
from app.api.middleware.cors import setup_cors
from app.infrastructure.startup import on_startup, on_shutdown


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup()
    yield
    await on_shutdown()


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        lifespan=lifespan,
        docs_url="/docs" if settings.ENV != "production" else None,
        redoc_url="/redoc" if settings.ENV != "production" else None,
    )

    # Reset schema cache
    app.openapi_schema = None

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=settings.PROJECT_NAME,
            version=settings.VERSION,
            routes=app.routes,
        )

        # 🔐 JWT Bearer Security Scheme
        openapi_schema.setdefault("components", {})
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }

        # 🔐 Apply globally
        openapi_schema["security"] = [{"BearerAuth": []}]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    # Override OpenAPI
    app.openapi = custom_openapi

    # Middlewares & Routers
    setup_cors(app)

    health_router = HealthRouter()
    app.include_router(health_router.router, prefix="/api", tags=["Health"])

    user_router = UserRouter()
    app.include_router(user_router.router, prefix="/api/v1", tags=["Users"])

    auth_router = AuthRouter()
    app.include_router(auth_router.router, prefix="/api", tags=["Auth"])
    return app


app = create_app()
