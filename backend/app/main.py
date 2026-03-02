from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from backend.app.api.v1.chat import router as chat_router
from backend.app.api.v1.health import router as health_router


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
    app.include_router(chat_router)

    return app


app = create_app()
