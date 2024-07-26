# import logging
# from typing import List
#
# from fastapi import APIRouter, status, Depends, HTTPException
# from sqlalchemy.orm import Session
#
# from app.config.database import SessionLocal
# from app.schema.role import RoleResponse, RoleCreate
# from app.service import role_service, category_service
#
# router = APIRouter()
#
# logger = logging.getLogger(__name__)
#
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# @router.post("/create_category", status_code=status.HTTP_201_CREATED)
# async def create_category(category: str, db: Session = Depends(get_db)):
#     try:
#         category_service.create_category(db, category)
#         return "category created successfully"
#     except Exception as ex:
#         logger.error(f"Error while creating category: {category} with exception: {ex}")
#         raise HTTPException(status_code=500, detail="Error creating category")
#
#
# @router.get("/get_all", status_code=status.HTTP_200_OK)
# async def get_all_category(db: Session = Depends(get_db)):
#     try:
#         roles = category_service.get_all_category(db)
#         if not roles:
#             raise HTTPException(status_code=404, detail="No category found")
#         return roles
#     except Exception as ex:
#         logger.error(f"Error fetching roles: {ex}")
#         raise HTTPException(status_code=500, detail="Error fetching category")
