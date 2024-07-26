# import logging
#
# from sqlalchemy.orm import Session
# from app.model.category import Category
#
# logger = logging.getLogger(__name__)
#
#
# def create_category(db: Session, category: str):
#     try:
#         cat_obj = Category(category_name=category)
#         db.add(cat_obj)
#         db.commit()
#         db.refresh(cat_obj)
#         logger.info(f"Category created successfully with cat_id: {cat_obj.id}")
#     except Exception as ex:
#         logger.error(f"Error while creating cat_obj: {ex}")
#         db.rollback()
#         raise
#
#
# def get_all_category(db: Session):
#     try:
#         logger.info("Retrieving all categories from the database")
#         return db.query(Category).all()
#     except Exception as ex:
#         logger.error(f"Error retrieving all categories: {ex}")
#         raise
