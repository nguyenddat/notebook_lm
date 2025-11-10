from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from db import get_db
from api.v1 import auth_router, thread_router, message_router

def getApplication() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    """Register API routers."""
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(thread_router, prefix="/api/v1/thread", tags=["Threads"])
    app.include_router(message_router, prefix="/api/v1/message", tags=["Messages"])

    # app.mount("/artifacts", StaticFiles(directory="/backend/artifacts"), name="artifacts")
    return app


app = getApplication()