#!/usr/bin/python3

import pytest
from unittest.mock import patch
from flask import Flask
from app.routes import api_blueprint

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(api_blueprint)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_employee(client):
    data = {"name": "John Doe", "email": "john@example.com", "phone": "123456789"}
    with patch('yourapp.controllers.create_employee_controller') as mock_controller:
        mock_controller.return_value = ({"message": "Employee created"}, 201)
        response = client.post('/create_employee', json=data)
        assert response.status_code == 201
        assert response.json['message'] == 'Employee created'

def test_clock_in(client):
    data = {"employee_id": 1}
    with patch('yourapp.controllers.clock_in_employee') as mock_controller:
        mock_controller.return_value = ({"message": "Clocked in"}, 200)
        response = client.post('/clock-in', json=data)
        assert response.status_code == 200
        assert response.json['message'] == 'Clocked in'

def test_clock_out(client):
    data = {"employee_id": 1}
    with patch('yourapp.controllers.clock_out_employee') as mock_controller:
        mock_controller.return_value = ({"message": "Clocked out"}, 200)
        response = client.post('/clock-out', json=data)
        assert response.status_code == 200
        assert response.json['message'] == 'Clocked out'

def test_get_attendance(client):
    with patch('yourapp.controllers.get_employee_attendance') as mock_controller:
        mock_controller.return_value = ({"attendance": []}, 200)
        response = client.get('/attendance/1')
        assert response.status_code == 200
        assert response.json['attendance'] == []
