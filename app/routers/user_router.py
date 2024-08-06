import logging
from typing import Optional, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.custom_exceptions.custom_exceptions import UserNotFoundException
from app.schemas.user import UserResponse, UserCreate
from app.security.auth import get_current_user
from app.services import user_service

router = APIRouter()

logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/create_user", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db, user)
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Error creating user")


@router.get("/get_user_by_id/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(user: user_dependency, user_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"user validated successfully: {user}")
        return user_service.get_user_by_id(db, user_id)
    except UserNotFoundException as ex:
        raise ex
    except Exception as ex:
        logger.error(f"Error while retrieving user: {user_id}, exception: {ex}")
        raise HTTPException(status_code=500, detail="Error retrieving user")


@router.get("/get_all_users", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users_with_pagination(user: user_dependency,
                                        limit: Optional[int] = 10,
                                        offset: Optional[int] = 0,
                                        direction: Optional[str] = "asc",
                                        db: Session = Depends(get_db)
                                        ):
    try:
        logger.info(f"user validated successfully: {user}")
        return user_service.get_all_users_with_pagination(db, limit=limit, offset=offset, direction=direction)
    except Exception as ex:
        logger.error(f"Error fetching users: {ex}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
