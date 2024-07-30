from logging.config import dictConfig

from fastapi import FastAPI

from app.config.base import Base
from app.config.database import engine
from app.routers import user_router, post_router, role_router, aadhar_router, app_router as app_router, app_request_router
import logging
from app.config.logging_config import LOGGING_CONFIG
from app.custom_exceptions.custom_exceptions import UserNotFoundException, not_found_exception_handler, \
    user_not_found_exception_handler, NotFoundException

dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(user_router.router, prefix="/user", tags=["user"])
app.include_router(post_router.router, prefix="/post", tags=["post"])
app.include_router(role_router.router, prefix="/role", tags=["role"])
app.include_router(aadhar_router.router, prefix="/aadhar", tags=["aadhar"])
app.include_router(app_router.router, prefix="/app", tags=["app"])
app.include_router(app_request_router.router, prefix="/app_request", tags=["app_request"])

app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)


@app.get("/")
def read_root() -> dict[str, str]:
    logger.info("Root endpoint called")
    return {"message": "Welcome to FastAPI, got to /docs to access all the endpoints via swagger"}


@app.get("/about")
async def about() -> str:
    return "this is about page"
