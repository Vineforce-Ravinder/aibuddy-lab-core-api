from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import settings
from app.config.logging import setup_logging
from app.api.middleware.cors import setup_cors
from app.api.routes import router as api_router
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

    setup_cors(app)

    app.include_router(api_router, prefix="/api")

    return app


app = create_app()


# if __name__ == "__main__":
#     # Recommended: run via `uvicorn app.main:app` or VS Code launch config.
#     # This convenience runner allows `python -m app.main` (module mode).
#     import uvicorn

#     uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
