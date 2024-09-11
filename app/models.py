#!/usr/bin/python3

import datetime
import uuid
from sqlalchemy import Column, String, DateTime

class BaseModel(Base):
    """The BaseModel class from which future classes will be derived"""
    __abstract__ = True

    # Define the 'id' column as a string with a maximum length of 60 characters, 
    # set it as the primary key, and assign a default value using uuid.uuid4()
    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """String representation of the BaseModel class"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def to_dict(self, save_fs=None):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        
        new_dict["created_at"] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        new_dict["updated_at"] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        new_dict["__class__"] = self.__class__.__name__
        
        new_dict.pop('_sa_instance_state', None)
        if save_fs is None and "password" in new_dict:
            del new_dict["password"]
        return new_dict
    
    def save(self, session):
        """updates the attribute 'updated_at' with the current datetime and commits the session"""
        session = Session
        
        self.updated_at = datetime.utcnow()
        session.add(self)
        session.commit()

    def delete(self, session):
        """delete the current instance from the storage and commits the session"""
        session = Session
        session.delete(self)
        session.commit()