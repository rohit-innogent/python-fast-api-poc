from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.exception.custom_exceptions import UserNotFoundException
from app.schema.user import UserResponse, UserCreate
from app.service import user_service
import logging

router = APIRouter()


logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=str, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_service.create_user(db, user)
        return "User created successfully"
    except Exception as ex:
        logger.error(f"Error while creating user with email {user.email}: {ex}")
        raise HTTPException(status_code=500, detail="Error creating user")


@router.get("/get_by_id/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        user = user_service.get_user(user_id, db)
        if user is None:
            raise UserNotFoundException(user_id)
        return user
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    except Exception as ex:
        logger.error(f"Error while retrieving user {user_id}: {ex}")
        raise HTTPException(status_code=500, detail="Error retrieving user")


@router.get("/get_all", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    direction: Optional[str] = "asc",
    db: Session = Depends(get_db)
):
    try:
        users = user_service.get_all_users(db, limit=limit, offset=offset, direction=direction)
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        return users
    except Exception as ex:
        logger.error(f"Error fetching users: {ex}")
        raise HTTPException(status_code=500, detail="Internal Server Error")