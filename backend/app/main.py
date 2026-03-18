from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.v1.chat import router as chat_router
from backend.app.api.v1.health import router as health_router
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.scores import router as scores_router
from backend.app.db.session import Base, engine


def create_app() -> FastAPI:
    app = FastAPI(title="MedAssist Backend", version="1.0")

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers
    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(chat_router)
    app.include_router(scores_router)

    @app.on_event("startup")
    def _init_db() -> None:
        Base.metadata.create_all(bind=engine)

    return app


app = create_app()
