import pytest
from app import create_app, db
from app.models import Employee, Department, Task

@pytest.fixture
def app():
    app = create_app('testing')  # Use the testing config
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

# Integration test for create_employee_controller
def test_create_employee_integration(client, app):
    department = Department(name="Engineering", manager_id=1)
    db.session.add(department)
    db.session.commit()

    data = {
        'last_name': 'Doe',
        'first_name': 'John',
        'department_id': department.id,
        'role': 'Developer',
        'email': 'john.doe@example.com',
        'phone_number': '123456789'
    }

    response = client.post('/api/employee', json=data)
    json_data = response.get_json()

    assert response.status_code == 201
    assert json_data['message'] == "Employee and contact information added successfully!"

# Integration test for clock_in_employee
def test_clock_in_employee_integration(client, app):
    department = Department(name="Engineering", manager_id=1)
    db.session.add(department)
    db.session.commit()

    employee = Employee(first_name="John", last_name="Doe", department_id=department.id, role="Developer")
    db.session.add(employee)
    db.session.commit()

    response = client.post(f'/api/employee/{employee.id}/clock-in')
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['message'] == "Clock-in successful"
    assert 'clock_in_time' in json_data

# Integration test for clock_out_employee
def test_clock_out_employee_integration(client, app):
    department = Department(name="Engineering", manager_id=1)
    db.session.add(department)
    db.session.commit()

    employee = Employee(first_name="John", last_name="Doe", department_id=department.id, role="Developer")
    db.session.add(employee)
    db.session.commit()

    # First clock-in
    client.post(f'/api/employee/{employee.id}/clock-in')

    # Clock-out
    response = client.post(f'/api/employee/{employee.id}/clock-out')
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['message'] == "Clock-out successful"
    assert 'clock_out_time' in json_data
