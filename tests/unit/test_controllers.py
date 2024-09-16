import pytest
from unittest.mock import patch, MagicMock
from app.controllers import create_employee_controller, clock_in_employee, clock_out_employee

# Unit test for create_employee_controller
def test_create_employee_controller():
    mock_data = {
        'last_name': 'Doe',
        'first_name': 'John',
        'department_id': 1,
        'role': 'Developer',
        'email': 'john.doe@example.com',
        'phone_number': '123456789'
    }
    
    # Mock the database session and models
    with patch('yourapp.controllers.db.session') as mock_session, \
         patch('yourapp.controllers.Employee') as MockEmployee, \
         patch('yourapp.controllers.EmployeeContact') as MockEmployeeContact:

        response, status_code = create_employee_controller(mock_data)
        
        assert status_code == 201
        assert response['message'] == "Employee and contact information added successfully!"
        
        # Ensure that the Employee and EmployeeContact objects were created
        mock_session.add.assert_any_call(MockEmployee())
        mock_session.add.assert_any_call(MockEmployeeContact())
        mock_session.commit.assert_called()

# Unit test for clock_in_employee
def test_clock_in_employee():
    mock_employee_id = 1

    with patch('yourapp.controllers.Employee.query.get') as mock_get, \
         patch('yourapp.controllers.db.session') as mock_session, \
         patch('yourapp.controllers.Attendance') as MockAttendance:

        # Simulate finding an employee
        mock_get.return_value = MagicMock(id=mock_employee_id)

        response = clock_in_employee(mock_employee_id)
        
        assert response['message'] == "Clock-in successful"
        MockAttendance.assert_called_once_with(employee_id=mock_employee_id, clock_in_time=MagicMock())
        mock_session.commit.assert_called()

# Unit test for clock_out_employee
def test_clock_out_employee():
    mock_employee_id = 1

    with patch('yourapp.controllers.Attendance.query.filter_by') as mock_filter_by, \
         patch('yourapp.controllers.db.session') as mock_session:

        # Simulate an existing clock-in record
        mock_filter_by.return_value.order_by.return_value.first.return_value = MagicMock(clock_out_time=None)

        response = clock_out_employee(mock_employee_id)
        
        assert response['message'] == "Clock-out successful"
        mock_session.commit.assert_called()
