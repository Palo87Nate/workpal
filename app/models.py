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
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    role = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "position": self.role
        }

class Attendance(BaseModel):
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    clock_in_time = db.Column(db.DateTime, nullable=True)
    clock_out_time = db.Column(db.DateTime, nullable=True)

class Candidate(BaseModel):
    __tablename__ = 'candidates'
    
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "position": self.position
        }

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
    manager_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<Department {self.name}>'

class Task(BaseModel):
    __tablename__ = 'tasks'
    task_name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)  # New field for task completion

    department = db.relationship('Department', backref='tasks')

    def __repr__(self):
        return f'<Task {self.task_name} in Department {self.department_id}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "task": self.task_name,
            "employee_id": self.employee_id,
            "completion": self.completed
        }
    
class Contact(BaseModel):
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    contact_id = db.Column(db.Integer)  # ID from either Candidate or Employee
    contact_class = db.Column(db.String(50))  # Polymorphic identifier

    __mapper_args__ = {
        'polymorphic_on': contact_class,
        'polymorphic_identity': 'contact'
    }

    def to_dict(self):
        """Serialize the Contact object into a JSON-friendly dictionary."""
        return {
            "email": self.email,
            "phone_number": self.phone_number,
            "contact_id": self.contact_id,
            "contact_class": self.contact_class
        }

class CandidateContact(Contact):
    __mapper_args__ = {
        'polymorphic_identity': 'candidate'
    }

class EmployeeContact(Contact):
    __mapper_args__ = {
        'polymorphic_identity': 'employee'
    }