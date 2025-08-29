# app/repositories/base_repository.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import and_, or_, desc, asc
from app.config.database import get_db_context
from app.models.user import User

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


class BaseRepository(Generic[ModelType], ABC):
    """Base repository class with common CRUD operations."""
    
    def __init__(self, model: type[ModelType]):
        self.model = model
    
    def get_by_id(self, id: Any) -> Optional[ModelType]:
        """Get a single record by ID."""
        with get_db_context() as session:
            return session.query(self.model).filter(getattr(self.model, "id") == id).first()
    
    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        order_desc: bool = False
    ) -> List[ModelType]:
        """Get all records with optional filtering and pagination."""
        with get_db_context() as session:
            query = session.query(self.model)
            
            # Apply filters
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        if isinstance(value, list):
                            query = query.filter(getattr(self.model, field).in_(value))
                        else:
                            query = query.filter(getattr(self.model, field) == value)
            
            # Apply ordering
            if order_by and hasattr(self.model, order_by):
                if order_desc:
                    query = query.order_by(desc(getattr(self.model, order_by)))
                else:
                    query = query.order_by(asc(getattr(self.model, order_by)))
            
            return query.offset(skip).limit(limit).all()
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count records with optional filtering."""
        with get_db_context() as session:
            query = session.query(self.model)
            
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        if isinstance(value, list):
                            query = query.filter(getattr(self.model, field).in_(value))
                        else:
                            query = query.filter(getattr(self.model, field) == value)
            
            return query.count()
    
    def create(self, obj_data: Dict[str, Any]) -> ModelType:
        """Create a new record."""
        print(obj_data)
        with get_db_context() as session:
            db_obj = self.model(**obj_data)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj
    
    def update(self, id: Any, obj_data: Dict[str, Any]) -> Optional[ModelType]:
        """Update an existing record."""
        with get_db_context() as session:
            db_obj = session.query(self.model).filter(getattr(self.model, "id") == id).first()
            if db_obj:
                for field, value in obj_data.items():
                    if hasattr(db_obj, field):
                        setattr(db_obj, field, value)
                session.commit()
                session.refresh(db_obj)
                return db_obj
            return None
    
    def delete(self, id: Any) -> bool:
        """Delete a record by ID."""
        with get_db_context() as session:
            db_obj = session.query(self.model).filter(getattr((self.model),"id") == id).first()
            if db_obj:
                session.delete(db_obj)
                session.commit()
                return True
            return False
    
    def bulk_create(self, objects_data: List[Dict[str, Any]]) -> List[ModelType]:
        """Create multiple records in a single transaction."""
        with get_db_context() as session:
            db_objects = [self.model(obj_data) for obj_data in objects_data]
            session.add_all(db_objects)
            session.commit()
            for obj in db_objects:
                session.refresh(obj)
            return db_objects
    
    def exists(self, id: Any) -> bool:
        """Check if a record exists by ID."""
        with get_db_context() as session:
            return session.query(self.model).filter(getattr(self.model, "id") == id).first() is not None
    
    def get_by_field(self, field_name: str, field_value: Any) -> Optional[ModelType]:
        """Get a record by a specific field."""
        with get_db_context() as session:
            if hasattr(self.model, field_name):
                return session.query(self.model).filter(
                    getattr(self.model, field_name) == field_value
                ).first()
            return None
    
    def get_multiple_by_field(
        self, 
        field_name: str, 
        field_values: List[Any]
    ) -> List[ModelType]:
        """Get multiple records by field values."""
        with get_db_context() as session:
            if hasattr(self.model, field_name):
                return session.query(self.model).filter(
                    getattr(self.model, field_name).in_(field_values)
                ).all()
            return []