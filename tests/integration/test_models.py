import pytest
from app import create_app
from app.models import db, Employee, Department, Task

@pytest.fixture
def app():
    app = create_app('testing')  # Assuming you have a 'testing' config for test DB
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

# Integration test for creating an Employee and Department
def test_create_employee_integration(client, app):
    department = Department(name="Engineering", manager_id=1)
    db.session.add(department)
    db.session.commit()

    employee = Employee(first_name="John", last_name="Smith", department_id=department.id, role="Developer")
    db.session.add(employee)
    db.session.commit()

    retrieved_employee = Employee.query.filter_by(first_name="John").first()
    assert retrieved_employee.last_name == "Smith"
    assert retrieved_employee.role == "Developer"

# Integration test for creating a Task
def test_create_task_integration(client, app):
    department = Department(name="HR", manager_id=2)
    db.session.add(department)
    db.session.commit()

    task = Task(task_name="Interview Scheduling", department_id=department.id, completed=False)
    db.session.add(task)
    db.session.commit()

    retrieved_task = Task.query.filter_by(task_name="Interview Scheduling").first()
    assert retrieved_task.task_name == "Interview Scheduling"
    assert not retrieved_task.completed
