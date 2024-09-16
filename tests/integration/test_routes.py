#!/usr/bin/python3

import pytest
from flask import Flask
from app.routes import api_blueprint

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(api_blueprint)
    # Initialize the actual DB if needed here.
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_employee_integration(client):
    data = {"name": "John Doe", "email": "john@example.com", "phone": "123456789"}
    response = client.post('/create_employee', json=data)
    assert response.status_code == 201
    assert response.json['message'] == 'Employee created'

def test_get_attendance_integration(client):
    response = client.get('/attendance/1')
    assert response.status_code == 200
    assert isinstance(response.json['attendance'], list)
