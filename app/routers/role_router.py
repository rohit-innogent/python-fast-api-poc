import logging
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.schemas.role import RoleResponse, RoleCreate
from app.services import role_service

router = APIRouter()

logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create_role", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user(role_request: RoleCreate, db: Session = Depends(get_db)):
    try:
        return role_service.create_role(db, role_request)
    except Exception:
        raise HTTPException(status_code=500, detail="Error creating user")


@router.get("/get_all", response_model=List[RoleResponse], status_code=status.HTTP_200_OK)
async def get_all_roles(db: Session = Depends(get_db)):
    try:
        roles = role_service.get_all_roles(db)
        return roles
    except Exception as ex:
        logger.error(f"Error fetching roles: {ex}")
        raise HTTPException(status_code=500, detail="Error fetching roles")
