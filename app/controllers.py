#!/usr/bin/python3

from datetime import datetime
from .models import *
from .extensions import db
from flask import request, jsonify, send_file
import io

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

def get_candidate_controller(id):
    candidate = Candidate.query.get_or_404(id)
    return {
        'id': candidate.id,
        'first_name': candidate.first_name,
        'last_name': candidate.last_name,
        'role_applied_for': candidate.position,
        'experience_years': candidate.experience
    }

def upload_documents_controller(candidate_id):
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

def create_department_controller(data):
    new_department = Department(name=data['name'], manager_id=data['manager_id'])
    db.session.add(new_department)
    db.session.commit()
    return {"message": "Department created successfully!"}, 201

def get_departments_controller():
    departments = Department.query.all()
    result = [{"id": d.id, "name": d.name, "manager_id": d.manager_id} for d in departments]
    return result, 200