import pytest
from flask import Flask, jsonify
from app import create_app
from app.models import Employee, Attendance, Candidate, Contact, Task, Department
from app.controllers import (
    create_employee_controller, get_employee_tasks_controller, 
    get_employee_contact_controller, clock_in_employee_controller, 
    clock_out_employee_controller, create_candidate_controller,
    get_present_employees_controller, get_absent_employees_controller,
    create_department_controller, create_task_controller
)

# Setup Flask test client
@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

# Employee Management Tests
def test_create_employee_controller(client):
    """Test the creation of an employee"""
    data = {
        "last_name": "Doe",
        "first_name": "John",
        "role": "Developer",
        "email": "john.doe@example.com",
        "phone_number": "1234567890"
    }
    response = create_employee_controller(data)
    assert response[1] == 201
    assert response[0]['message'] == "Employee and contact information added successfully!"

def test_get_employee_tasks_controller(client):
    """Test retrieving tasks assigned to an employee"""
    employee_id = 1
    tasks = get_employee_tasks_controller(employee_id)
    assert isinstance(tasks, list)

def test_get_employee_contact_controller(client):
    """Test retrieving contact information of an employee"""
    contact_id = 1
    contact = get_employee_contact_controller(contact_id)
    assert isinstance(contact, list)

# Time and Attendance Tests
def test_clock_in_employee_controller(client):
    """Test employee clock-in"""
    employee_id = 1
    response = clock_in_employee_controller(employee_id)
    assert response[1] == 200
    assert "clock_in_time" in response[0]

# Candidate Management Tests
def test_create_candidate_controller(client):
    """Test creating a candidate"""
    data = {
        "last_name": "Smith",
        "first_name": "Jane",
        "position": "Manager",
        "experience": 5,
        "email": "jane.smith@example.com",
        "phone_number": "9876543210"
    }
    response = create_candidate_controller(data)
    assert response[1] == 201
    assert response[0]['message'] == "Candidate created successfully"

# Department Management Tests
def test_create_department_controller(client):
    """Test creating a department"""
    data = {
        "name": "Human Resources"
    }
    response = create_department_controller(data)
    assert response[1] == 201
    assert response[0]['message'] == "Department created successfully!"

# Task Management Tests
def test_create_task_controller(client):
    """Test creating a task"""
    data = {
        "task_name": "Prepare report",
        "department_id": 1,
        "employee_id": 1,
        "completed": False
    }
    response = create_task_controller(data)
    assert response[1] == 201
    assert response[0]['message'] == "Task created successfully!"
