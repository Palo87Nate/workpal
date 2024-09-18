#!/usr/bin/python3

# The controllers serve as the business logic for the application
# Each controller is a function that is designed to perform a task
# called on by a route
# The controllers are organized by model, with each model having its
# own controller
# This facilitates code readability and undersandability by separating
# business loic from app logic and organising functions by feature

from datetime import datetime
from .models import *
from .extensions import db
from flask import request, jsonify, send_file
from datetime import datetime, date
from sqlalchemy import func
import io



# These controllers are part of the Employee Information management feature
def create_employee_controller(data):
    """Creates an emloyee and save it to the daabade"""
    last_name = data['last_name']
    first_name = data['first_name']
    department_id = data['department_id']
    role=data['role']
    email = data['email']
    phone_number = data['phone_number']

    # Create and add the employee
    employee = Employee(last_name=last_name, first_name=first_name, department_id=department_id, role=role)
    db.session.add(employee)
    db.session.commit()

    # Add the employee's contact information
    employee_contact = EmployeeContact(email=email, phone_number=phone_number, contact_id=employee.id)
    db.session.add(employee_contact)
    db.session.commit()

    return {"message": "Employee and contact information added successfully!"}, 201

def get_employee_tasks_controller(employee_id):
    """Returns a list of tasks assigned to an employee"""
    tasks = Task.query.filter_by(employee_id=employee_id).all()
    return tasks

def get_employee_contact_controller(employee_id):
    """Returns the contact details of an an employee"""
    contact = Contact.query.filter_by(employee_id=employee_id).all()
    return contact

def get_present_employees_controller():
    """Returns a list of employees who have clocked in today."""
    today = date.today()
    # Get all attendance records where clock_in_time is today
    attendance_today = Attendance.query.filter(
        db.func.date(Attendance.clock_in_time) == today
    ).all()

    # Get employee details from the attendance records
    employee_ids = [record.employee_id for record in attendance_today]
    employees = Employee.query.filter(Employee.id.in_(employee_ids)).all()
    
    return employees
def get_absent_employees_controller():
    """Returns a list of employees who have not clocked in today."""
    today = date.today()
    
    # Get all attendance records where clock_in_time is today
    attendance_today = Attendance.query.filter(
        db.func.date(Attendance.clock_in_time) == today
    ).all()
    
    # Get a list of employee IDs who have clocked in today
    present_employee_ids = [record.employee_id for record in attendance_today]
    
    # Get all employees except those who have clocked in
    absent_employees = Employee.query.filter(
        ~Employee.id.in_(present_employee_ids)
    ).all()
    
    return absent_employees

def get_all_employees_controller():
    """Returns a list of all employees in the company."""
    employees = Employee.query.all()
    return employees

def get_employee_controller(employee_id):
    """Returns an employee based on their ID."""
    employee = Employee.query.get(employee_id)
    if not employee:
        return {"error": "Employee not found"}, 404
    return employee

# These controllers are part of the time and attendance registry feature
def clock_in_employee_controller(employee_id):
    """Clocks in an employee"""
    employee = Employee.query.get(employee_id)
    if not employee:
        return {"error": "Employee not found"}, 404

    # Create attendance record with clock-in time
    attendance = Attendance(employee_id=employee_id, clock_in_time=datetime.now())
    db.session.add(attendance)
    db.session.commit()

    return {"message": "Clock-in successful", "clock_in_time": attendance.clock_in_time}

def clock_out_employee_controller(employee_id):
    # Find the latest clock-in record for this employee
    attendance = Attendance.query.filter_by(employee_id=employee_id, clock_out_time=None).order_by(Attendance.clock_in_time.desc()).first()

    if not attendance:
        return {"error": "No active clock-in record found"}, 404

    # Update the record with clock-out time
    attendance.clock_out_time = datetime.now()
    db.session.commit()

    return {"message": "Clock-out successful", "clock_out_time": attendance.clock_out_time}

def get_employee_attendance_controller(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return {"error": "Employee not found"}, 404

    records = Attendance.query.filter_by(employee_id=employee_id).all()
    return [{
        "clock_in": record.clock_in_time,
        "clock_out": record.clock_out_time
    } for record in records]

# The following controllers are part of the recruitment feature
def create_candidate_controller(data):
    """Creates a candidate for a position and their contact and saves to database"""
    last_name = data['last_name']
    first_name = data['first_name']
    position = data['role']
    experience = data['experience']
    email = data['email']
    phone_number = data['phone_number']

    candidate = Candidate(
        first_name=first_name,
        last_name=last_name,
        position=position,
        experience=experience
    )
        
    db.session.add(candidate)
    db.session.commit()

    candidate_contact = CandidateContact(
        email=email,
        phone_number=phone_number,
        contact_id=candidate.id
    )

    db.session.add(candidate_contact)
    db.session.commit()

    return {'message': 'Candidate created successfully'}, 201

def get_candidate_controller(id):
    """Retrieves a candidate by their id"""
    candidate = Candidate.query.get_or_404(id)
    return {
        'id': candidate.id,
        'first_name': candidate.first_name,
        'last_name': candidate.last_name,
        'role_applied_for': candidate.position,
        'experience_years': candidate.experience
    }

def get_candidate_contact_controller(candidate_id):
    """Returns the contact details of a cadidate"""
    contact = Contact.query.filter_by(candidate_id=candidate_id).all()
    return contact

def get_candidates_by_position_controller(position):
    """Returns a list of candidates who applied for a specific position (case-insensitive)."""
    candidates = Candidate.query.filter(func.lower(Candidate.position) == func.lower(position)).all()
    return candidates

def upload_documents_controller(candidate_id):
    """Uploads documents for a candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    documents = Documents(candidate_id=candidate.id)

    if 'resume' in request.files:
        documents.resume.put(request.files['resume'], content_type='application/pdf')

    if 'national_id_copy' in request.files:
        documents.national_id_copy.put(request.files['national_id_copy'], content_type='image/jpeg')

    if 'photo' in request.files:
        documents.photo.put(request.files['photo'], content_type='image/jpeg')

    if 'application_letter' in request.files:
        documents.application_letter.put(request.files['application_letter'], content_type='application/pdf')

    if 'degree_copy' in request.files:
        documents.degree_copy.put(request.files['degree_copy'], content_type='application/pdf')

    documents.save()
    return {'message': 'Documents uploaded successfully'}, 201

def download_document_controller(doc_id, file_type):
    """Downloads a document"""
    documents = Documents.objects.get(id=doc_id)

    file_data = None
    if file_type == 'resume':
        file_data = documents.resume
    elif file_type == 'national_id_copy':
        file_data = documents.national_id_copy
    elif file_type == 'photo':
        file_data = documents.photo
    elif file_type == 'application_letter':
        file_data = documents.application_letter
    elif file_type == 'degree_copy':
        file_data = documents.degree_copy

    if not file_data:
        return {'message': 'File not found'}, 404

    return send_file(
        io.BytesIO(file_data.read()),
        download_name=f"{file_type}.pdf" if file_type != 'photo' else f"{file_type}.jpeg",
        as_attachment=True
    )

# These controllers ar part of the Departments management feature
def create_department_controller(data):
    """Creates a department and saves the information to the database"""
    new_department = Department(name=data['name'])
    db.session.add(new_department)
    db.session.commit()
    return {"message": "Department created successfully!"}, 201

def get_department_employees_controller(department_id):
    """Returns a list of employees belonging to a specific department."""
    employees = Employee.query.filter_by(department_id=department_id).all()
    return employees

def get_department_tasks_controller(department_id):
    """Returns a list of tasks belonging to a specific department."""
    tasks = Task.query.filter_by(department_id=department_id).all()
    return tasks

def get_departments_controller():
    """Returns a list of all departments."""
    departments = Department.query.all()
    result = [{"id": d.id, "name": d.name, "manager_id": d.manager_id} for d in departments]
    return result, 200

def get_department_controller(id):
    """Returns a specific department by its id."""
    department = Department.query.get_or_404(id)
    result = {"id": department.id, "name": department.name, "manager_id": department.manager_id}
    return result, 200

def update_department_controller(id, data):
    """Updates a department and saves the information to the database."""
    department = Department.query.get_or_404(id)
    department.name = data.get('name', department.name)
    department.manager_id = data.get('manager_id', department.manager_id)
    db.session.commit()
    return {"message": "Department updated successfully!"}, 200

def delete_department_controller(id):
    """Deletes a department and saves the information to the database."""
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    return {"message": "Department deleted successfully!"}, 200

# The following controllers are part of the task management feature
def create_task_controller(data):
    """Creates a task and saves the information to the database."""
    new_task = Task(task_name=data['task_name'], department_id=data['department_id'], employee_id=data['employee_id'], completed=data.get('completed', False))
    db.session.add(new_task)
    db.session.commit()
    return {"message": "Task created successfully!"}, 201

def get_tasks_controller():
    """Returns a list of all tasks."""
    tasks = Task.query.all()
    result = [{"id": t.id, "task_name": t.task_name, "department_id": t.department_id, "employee_id": t.employee_id, "completed": t.completed} for t in tasks]
    return result, 200

def get_task_controller(id):
    """Returns a specific task by its id."""
    task = Task.query.get_or_404(id)
    result = {"id": task.id, "task_name": task.task_name, "department_id": task.department_id, "employee_id": task.employee_id, "completed": task.completed}
    return result, 200

def update_task_controller(id, data):
    """Updates a task and saves the information to the database."""
    task = Task.query.get_or_404(id)
    task.task_name = data.get('task_name', task.task_name)
    task.department_id = data.get('department_id', task.department_id)
    task.employee_id = data.get('employee_id', task.employee_id)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return {"message": "Task updated successfully!"}, 200

def delete_task_controller(id):
    """Deletes a task and saves the information to the database."""
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return {"message": "Task deleted successfully!"}, 200