from logging.config import dictConfig

from fastapi import FastAPI

from app.config.base import Base
from app.config.database import engine
from app.controller import user_controller, post_controller
import logging
from app.config.logging_config import LOGGING_CONFIG
from app.exception.custom_exceptions import UserNotFoundException, user_not_found_exception_handler

# logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
#                     format="%(asctime)s - %(levelname)s - %(message)s")
# logging.basicConfig(level=logging.INFO,
#                     format="%(asctime)s - %(levelname)s - %(message)s")

dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(user_controller.router, prefix="/user", tags=["user"])
app.include_router(post_controller.router, prefix="/post", tags=["post"])

app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)


@app.get("/")
def read_root() -> dict[str, str]:
    logger.info("Root endpoint called")
    return {"message": "Welcome to FastAPI"}


@app.get("/about")
async def about() -> str:
    return "this is about page"
