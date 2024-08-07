from typing import Type

from sqlalchemy.orm import Session, joinedload

from app.models import Adhar


def create_aadhar(db: Session, aadhar_obj: Adhar) -> Adhar:
    db.add(aadhar_obj)
    db.commit()
    db.refresh(aadhar_obj)
    return aadhar_obj


def get_all_adhar(db: Session) -> list[Type[Adhar]]:
    return db.query(Adhar).options(joinedload(Adhar.user)).all()
