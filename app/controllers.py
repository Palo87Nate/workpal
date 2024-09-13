#!/usr/bin/python3

from datetime import datetime
from .models import *
from .extensions import db

def clock_in_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return {"error": "Employee not found"}, 404

    # Create attendance record with clock-in time
    attendance = Attendance(employee_id=employee_id, clock_in_time=datetime.now())
    db.session.add(attendance)
    db.session.commit()

    return {"message": "Clock-in successful", "clock_in_time": attendance.clock_in_time}

def clock_out_employee(employee_id):
    # Find the latest clock-in record for this employee
    attendance = Attendance.query.filter_by(employee_id=employee_id, clock_out_time=None).order_by(Attendance.clock_in_time.desc()).first()

    if not attendance:
        return {"error": "No active clock-in record found"}, 404

    # Update the record with clock-out time
    attendance.clock_out_time = datetime.now()
    db.session.commit()

    return {"message": "Clock-out successful", "clock_out_time": attendance.clock_out_time}

def get_employee_attendance(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return {"error": "Employee not found"}, 404

    records = Attendance.query.filter_by(employee_id=employee_id).all()
    return [{
        "clock_in": record.clock_in_time,
        "clock_out": record.clock_out_time
    } for record in records]

def create_candidate_controller(data):
    candidate = Candidate(
        first_name=data['first_name'],
        last_name=data['last_name'],
        position=data['position'],
        experience=data['experience']
    )
    db.session.add(candidate)
    db.session.commit()
    return {'message': 'Candidate created successfully'}, 201