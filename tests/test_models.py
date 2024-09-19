import pytest
from datetime import datetime
from app import create_app
from app.extensions import db
from app.models import Employee, Department, Task, Attendance, Candidate, CandidateContact, Documents
from mongoengine import disconnect
from unittest.mock import patch

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for testing
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

    disconnect()  # Disconnect MongoDB after tests

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    # Create mock Department
    department = Department(name="Engineering", manager_id=1)
    db.session.add(department)
    db.session.commit()

    yield db

    db.drop_all()

### Testing BaseModel and Inheritance
def test_employee_model_creation(init_database):
    # Create an employee and save to the database
    employee = Employee(first_name="John", last_name="Doe", department_id=None, role="Developer")
    db.session.add(employee)
    db.session.commit()

    # Retrieve the employee and assert
    saved_employee = Employee.query.first()
    assert saved_employee.first_name == "John"
    assert saved_employee.last_name == "Doe"
    assert saved_employee.department_id == None
    assert saved_employee.role == "Developer"

def test_department_model(init_database):
    department = Department.query.first()
    assert department.name == "Engineering"
    assert department.manager_id == 1

### Testing Relationships
def test_employee_department_relationship(init_database):
    employee = Employee(first_name="Alice", last_name="Smith", department_id=1, role="Designer")
    db.session.add(employee)
    db.session.commit()

    department = Department.query.first()
    assert department.name == "Engineering"
    assert len(department.tasks) == 0

def test_task_model_creation(init_database):
    # Add Task for the department
    task = Task(task_name="Design Landing Page", department_id=1, employee_id=None)
    db.session.add(task)
    db.session.commit()

    saved_task = Task.query.first()
    assert saved_task.task_name == "Design Landing Page"
    assert saved_task.department_id == 1

### Testing Attendance Model
def test_attendance_creation(init_database):
    employee = Employee(first_name="Mark", last_name="Taylor", department_id=1, role="Developer")
    db.session.add(employee)
    db.session.commit()

    attendance = Attendance(employee_id=employee.id, clock_in_time=datetime.now(), clock_out_time=None)
    db.session.add(attendance)
    db.session.commit()

    saved_attendance = Attendance.query.first()
    assert saved_attendance.employee_id == employee.id
    assert saved_attendance.clock_out_time is None

### Testing Candidate and Documents (MongoDB)
@patch('app.models.Documents.save', return_value=True)
def test_candidate_creation(mock_save, init_database):
    # Create a candidate and test its data
    candidate = Candidate(first_name="Emily", last_name="Stone", position="Backend Developer", experience=5.0)
    db.session.add(candidate)
    db.session.commit()

    saved_candidate = Candidate.query.first()
    assert saved_candidate.first_name == "Emily"
    assert saved_candidate.last_name == "Stone"
    assert saved_candidate.position == "Backend Developer"
    assert saved_candidate.experience == 5.0

    # Test related document creation
    document = Documents(candidate_id=saved_candidate.id)
    assert document.candidate_id == saved_candidate.id
    mock_save.assert_called_once()  # Ensure that document save was called

### Testing Custom Methods (to_dict)
def test_to_dict_method(init_database):
    employee = Employee(first_name="Jane", last_name="Doe", department_id=1, role="Manager")
    db.session.add(employee)
    db.session.commit()

    saved_employee = Employee.query.first()
    employee_dict = saved_employee.to_dict()

    assert 'id' in employee_dict
    assert employee_dict['first_name'] == 'Jane'
    assert employee_dict['role'] == 'Manager'
    assert 'created_at' in employee_dict
    assert 'updated_at' in employee_dict

### Testing Contact Models (Polymorphism)
def test_candidate_contact(init_database):
    candidate_contact = CandidateContact(email="jane.doe@example.com", phone_number="123456789", contact_id=1)
    db.session.add(candidate_contact)
    db.session.commit()

    saved_contact = CandidateContact.query.first()
    assert saved_contact.email == "jane.doe@example.com"
    assert saved_contact.phone_number == "123456789"
    assert saved_contact.contact_class == "candidate"
