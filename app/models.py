#!/usr/bin/python3

from datetime import datetime
import uuid
from .extensions import db
from mongoengine import Document, ReferenceField, FileField, connect

Base = db.Model
class BaseModel(Base):
    """The BaseModel class from which future classes will be derived"""
    __abstract__ = True

    # Define the 'id' column as a string with a maximum length of 60 characters, 
    # set it as the primary key, and assign a default value using uuid.uuid4()
    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
        self.updated_at = db.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self, session):
        """delete the current instance from the storage and commits the session"""
        db.session.delete(self)
        db.session.commit()

class Employee(BaseModel):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Attendance(BaseModel):
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    clock_in_time = db.Column(db.DateTime, nullable=True)
    clock_out_time = db.Column(db.DateTime, nullable=True)

class Candidate(BaseModel):
    __tablename__ = 'candidates'
    
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Float, nullable=False)

# MongoEngine Setup
connect('files_db')

class Documents(Document):
    candidate_id = ReferenceField('Candidate')
    resume = FileField()
    national_id_copy = FileField()
    photo = FileField()
    application_letter = FileField()
    degree_copy = FileField()

class Department(BaseModel):
    __tablename__ = 'departments'
    name = db.Column(db.String(100), nullable=False)
    manager_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Department {self.name}>'