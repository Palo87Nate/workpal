import pytest
from unittest.mock import patch, MagicMock
from app.models import Employee, Attendance, Candidate, Task

# Unit test for BaseModel's to_dict method
def test_base_model_to_dict():
    mock_employee = Employee(first_name='John', last_name='Doe', department_id=1, role='Manager')
    expected_dict = mock_employee.to_dict()
    assert expected_dict['first_name'] == 'John'
    assert expected_dict['last_name'] == 'Doe'
    assert '__class__' in expected_dict

# Unit test for BaseModel's save method
def test_base_model_save():
    mock_session = MagicMock()
    mock_employee = Employee(first_name='Jane', last_name='Doe', department_id=2, role='Engineer')
    
    with patch('yourapp.models.db.session', mock_session):
        mock_employee.save(mock_session)
        mock_session.add.assert_called_once_with(mock_employee)
        mock_session.commit.assert_called_once()

# Unit test for BaseModel's delete method
def test_base_model_delete():
    mock_session = MagicMock()
    mock_employee = Employee(first_name='Jane', last_name='Doe', department_id=2, role='Engineer')
    
    with patch('yourapp.models.db.session', mock_session):
        mock_employee.delete(mock_session)
        mock_session.delete.assert_called_once_with(mock_employee)
        mock_session.commit.assert_called_once()

# Unit test for Employee model
def test_employee_model():
    employee = Employee(first_name="John", last_name="Smith", department_id=1, role="Developer")
    assert employee.first_name == "John"
    assert employee.role == "Developer"

# Unit test for Task model repr method
def test_task_repr():
    task = Task(task_name="Code Review", department_id=1)
    assert repr(task) == '<Task Code Review in Department 1>'
