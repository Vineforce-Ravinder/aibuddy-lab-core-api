from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your routers
from app.api.routes.authentication_router import AuthRouter
from app.api.routes.health import HealthRouter
from app.api.routes.user_router import UserRouter

# Import DB session and models for seeding
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.db.models.role import Role

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
    # --- STARTUP LOGIC ---
    print("🚀 AI Buddy starting up")
    seed_roles()  # <--- THIS RUNS AUTOMATICALLY ON START
    yield
    # --- SHUTDOWN LOGIC ---
    print("🛑 AI Buddy shutting down")

def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Buddy API",
        version="1.0.0",
        lifespan=lifespan  # Register the lifespan (startup/shutdown)
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    health_router = HealthRouter()
    user_router = UserRouter()
    auth_router = AuthRouter()

    app.include_router(health_router.router, prefix="/api", tags=["Health"])
    app.include_router(auth_router.router, prefix="/api", tags=["Auth"])
    app.include_router(user_router.router, prefix="/api/v1", tags=["Users"])

    return app

app = create_app()
