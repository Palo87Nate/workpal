import pytest
from unittest.mock import patch
from app import create_app
from flask import json
from datetime import datetime, date

# Set up the test client
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test create_employee route
@patch('app.routes.create_employee_controller')
def test_create_employee(mock_create_employee, client):
    mock_create_employee.return_value = ({"message": "Employee and contact information added successfully!"}, 201)
    
    # Simulate a POST request
    response = client.post('/employees/new', json={
        'last_name': 'Doe',
        'first_name': 'John',
        'role': 'Engineer',
        'email': 'johndoe@example.com',
        'phone_number': '1234567890'
    })
    
    # Assertions
    assert response.status_code == 201
    assert response.json == {"message": "Employee and contact information added successfully!"}
    mock_create_employee.assert_called_once_with({
        'last_name': 'Doe',
        'first_name': 'John',
        'role': 'Engineer',
        'email': 'johndoe@example.com',
        'phone_number': '1234567890'
        })

# Test get_employee_tasks route
@patch('app.routes.get_employee_tasks_controller')
def test_get_employee_tasks(mock_get_employee_tasks, client):
    mock_get_employee_tasks.return_value = ({"tasks": []}, 200)

    # Simulate a GET request
    response = client.get('/tasks/1')

    # Assertions
    assert response.status_code == 200
    assert response.json == {"tasks": []}
    mock_get_employee_tasks.assert_called_once_with(1)

# Test get_employee_contact route
@patch('app.routes.get_employee_contact_controller')
def test_get_employee_contact(mock_get_employee_contact, client):
    mock_get_employee_contact.return_value = ({"email": "john@example.com", "phone": "1234567890"}, 200)
    
    # Simulate a GET request
    response = client.get('/employees/1/contact')

    # Assertions
    assert response.status_code == 200
    assert response.json == {"email": "john@example.com", "phone": "1234567890"}
    mock_get_employee_contact.assert_called_once_with(1)

# Test get_present_employees route
@patch('app.routes.get_present_employees_controller')
def test_get_present_employees(client):
    response = client.get('/present_employees')
    assert response.status_code == 200
    data = response.get_json()  # Extract JSON data from the response
    assert isinstance(data, list)

# Test get_absent_employees route
@patch('app.routes.get_absent_employees_controller')
def test_get_absent_employees(client):
    response = client.get('/absent_employees')
    assert response.status_code == 200
    data = response.get_json()  # Extract JSON data from the response
    assert isinstance(data, list)

# Test clock_in_employee route
@patch('app.routes.clock_in_employee_controller')
def test_clock_in_employee(mock_clock_in_employee, client):
    mock_clock_in_employee.return_value = ({"message": "Clock-in successful"}, 200)

    # Simulate a POST request
    response = client.post('/clock-in', json={'employee_id': 1})

    # Assertions
    assert response.status_code == 200
    assert response.json == {"message": "Clock-in successful"}
    mock_clock_in_employee.assert_called_once_with(1)

# Test create_candidate route
@patch('app.routes.create_candidate_controller')
def test_create_candidate(mock_create_candidate, client):
    mock_create_candidate.return_value = ({"message": "Candidate created successfully"}, 201)

    # Simulate a POST request
    response = client.post('/candidates/new', json={
        'first_name': 'Jane',
        'last_name': 'Doe',
        'position': 'Developer',
        'experience': 5,
        'email': 'example@jandoe.com',
        'phone_number': '1112131415'
    })

    # Assertions
    assert response.status_code == 201
    assert response.json == {"message": "Candidate created successfully"}
    mock_create_candidate.assert_called_once_with({
        'first_name': 'Jane',
        'last_name': 'Doe',
        'position': 'Developer',
        'experience': 5,
        'email': 'example@jandoe.com',
        'phone_number': '1112131415'
    })

