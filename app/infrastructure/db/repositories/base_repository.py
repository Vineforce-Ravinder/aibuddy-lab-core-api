# app/infrastructure/db/repositories/base_repository.py

from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    # --------------------
    # READ
    # --------------------
    def get_by_id(self, db: Session, entity_id) -> Optional[T]:
        return db.query(self.model).filter(self.model.id == entity_id).first()

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[T]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_field(
        self,
        db: Session,
        field_name: str,
        value
    ) -> Optional[T]:
        if not hasattr(self.model, field_name):
            raise AttributeError(f"{field_name} not found in {self.model.__name__}")

        return (
            db.query(self.model)
            .filter(getattr(self.model, field_name) == value)
            .first()
        )

    # --------------------
    # CREATE
    # --------------------
    def create(self, db: Session, obj: T) -> T:
        try:
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj
        except Exception:
            db.rollback()
            raise

    # --------------------
    # UPDATE
    # --------------------
    def update(
        self,
        db: Session,
        db_obj: T,
        update_data: dict
    ) -> T:
        for key, value in update_data.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)

        try:
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception:
            db.rollback()
            raise

    # --------------------
    # DELETE
    # --------------------
    def delete(self, db: Session, db_obj: T) -> None:
        try:
            db.delete(db_obj)
            db.commit()
        except Exception:
            db.rollback()
            raise
