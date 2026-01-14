from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.openapi.utils import get_openapi

from app.api.routes.authentication_router import AuthRouter
from app.api.routes.health import HealthRouter
from app.api.routes.user_router import UserRouter
from app.api.routes.course_router import CourseRouter
from app.api.routes.module_router import ModuleRouter
from app.api.routes.topic_router import TopicRouter
from app.config import settings
from app.config.logging import setup_logging
from app.api.middleware.cors import setup_cors
from app.infrastructure.startup import on_startup, on_shutdown
from app.infrastructure.db.models.role import Role
from app.infrastructure.db.session import SessionLocal


def seed_roles():
    """Checks if roles exist, if not, adds them."""
    db = SessionLocal()
    try:
        # Check if any role exists
        if db.query(Role).first():
            return  # Roles already exist, do nothing

        print("🌱 Seeding default roles...")
        roles = [
            Role(id=0, name="Super Admin", code=0, description="System Super Admin", is_active=True, is_verified=True, is_deleted=False),
            Role(id=1, name="Admin", code=1, description="Administrator", is_active=True, is_verified=True, is_deleted=False),
            Role(id=2, name="Teacher", code=2, description="Teacher", is_active=True, is_verified=True, is_deleted=False),
            Role(id=3, name="Student", code=3, description="Student", is_active=True, is_verified=True, is_deleted=False),
        ]
        db.add_all(roles)
        db.commit()
        print("✅ Roles seeded successfully!")
    except Exception as e:
        print(f"⚠️ Failed to seed roles: {e}")
        db.rollback()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup()
    seed_roles() # Seed roles on startup
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

    course_router = CourseRouter()
    app.include_router(course_router.router, prefix="/api/v1", tags=["Courses"])

    module_router = ModuleRouter()
    app.include_router(module_router.router, prefix="/api/v1", tags=["Modules"])

    topic_router = TopicRouter()
    app.include_router(topic_router.router, prefix="/api/v1", tags=["Topics"])

    auth_router = AuthRouter()
    app.include_router(auth_router.router, prefix="/api", tags=["Auth"])
    return app


app = create_app()
