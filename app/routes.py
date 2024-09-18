#!/usr/bin/python3

from flask import Blueprint, request, jsonify
from .controllers import *

api_blueprint = Blueprint('api', __name__)

# Routes for Employee information management
@api_blueprint.route('/employees/new', methods=['POST'])
def create_employee():
    data = request.get_json()
    response, status_code = create_employee_controller(data)
    return jsonify(response), status_code

@api_blueprint.route('/tasks/<int:employee_id>', method=['GET'])
def get_employee_tasks(employee_id):
    response, status_code = get_employee_tasks_controller(employee_id)
    return jsonify(response), status_code

@api_blueprint.route('/employees/<int:employee_id>/contact', method=['GET'])
def get_employee_contact(employee_id):
    response, status_code = get_employee_contact_controller(employee_id)
    return jsonify(response), status_code

@api_blueprint.route('/presence/<string:date_str>', method=['GET'])
def get_present_employees(date_str):
    response, status_code = get_present_employees_controller(date_str)
    return jsonify(response), status_code

@api_blueprint.route('/absence/<string:date_str>', method=['GET'])
def get_absent_employees(date_str):
    response, status_code = get_absent_employees_controller(date_str)
    return jsonify(response), status_code

@api_blueprint.route('employees/all', methods=['GET'])
def get_all_employees():
    response, status_code = get_all_employees_controller()
    return jsonify(response), status_code

@api_blueprint.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    response, status_code = get_employee_controller(employee_id)
    return jsonify(response), status_code

@api_blueprint.route('/clock-in', methods=['POST'])
def clock_in_employee():
    data = request.json
    employee_id = data.get('employee_id')

    # Call controller function to handle clock-in
    response, status_code = clock_in_employee_controller(employee_id)
    return jsonify(response), status_code

@api_blueprint.route('/clock-out', methods=['POST'])
def clock_out_employee():
    data = request.json
    employee_id = data.get('employee_id')

    # Call controller function to handle clock-out
    response, status_code = clock_out_employee_controller(employee_id)
    return jsonify(response), status_code

@api_blueprint.route('/attendance/<int:employee_id>', methods=['GET'])
def get_employee_attendance(employee_id):
    # Call controller function to get attendance records
    response, status_code = get_employee_attendance_controller(employee_id)
    return jsonify(response), status_code

@api_blueprint.route('/candidates/new', methods=['POST'])
def create_candidate():
    data = request.get_json()
    response, status_code = create_candidate_controller(data)
    return jsonify(response), status_code

@api_blueprint.route('/candidates/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    response = get_candidate_controller(candidate_id)
    return jsonify(response)

@api_blueprint.route('/candidates/<int:candidate_id>/contact', methods=['GET'])
def get_candidate_contact(candidate_id):
    response = get_candidate_contact_controller(candidate_id)
    return jsonify(response)

@api_blueprint.route('/candidates/<string:position>', methods=['GET'])
def get_candidates_by_position(position):
    response = get_candidates_by_position_controller(position)
    return jsonify(response)

@api_blueprint.route('/documents/upload/<int:candidate_id>', methods=['POST'])
def upload_documents(candidate_id):
    response, status_code = upload_documents_controller(candidate_id)
    return jsonify(response), status_code

@api_blueprint.route('/documents/<string:doc_id>/<string:file_type>', methods=['GET'])
def download_document(doc_id, file_type):
    response = download_document_controller(doc_id, file_type)
    if isinstance(response, dict):  # Handle error messages
        return jsonify(response), 404
    return response

@api_blueprint.route('/departments/new', methods=['POST'])
def create_department():
    data = request.get_json()
    response, status_code = create_department_controller(data)
    return jsonify(response), status_code

@api_blueprint.route('/employees/<int:department_id>', methods=['GET'])
def get_department_employees(department_id):
    response = get_department_employees_controller(department_id)
    return jsonify(response)

@api_blueprint.route('/tasks/<int:department_id>', methods=['GET'])
def get_department_tasks(department_id):
    response = get_department_tasks_controller(department_id)
    return jsonify(response)

@api_blueprint.route('/departments/all', methods=['GET'])
def get_departments():
    response, status_code = get_departments_controller()
    return jsonify(response), status_code

@api_blueprint.route('/departments/<int:department_id>', methods=['GET'])
def get_department(department_id):
    response, status_code = get_department_controller(department_id)
    return jsonify(response), status_code

@api_blueprint.route('/departments/<int:department_id>', methods=['PUT'])
def update_department(department_id):
    data = request.get_json()
    response, status_code = update_department_controller(department_id, data)
    return jsonify(response), status_code

@api_blueprint.route('/departments/<int:department_id>', methods=['DELETE'])
def delete_department(department_id):
    response, status_code = delete_department_controller(department_id)
    return jsonify(response), status_code

@api_blueprint.route('/tasks/new', methods=['POST'])
def create_task():
    data = request.get_json()
    response, status_code = create_task_controller(data)
    return jsonify(response), status_code

@api_blueprint.route('/tasks/all', methods=['GET'])
def get_tasks():
    response, status_code = get_tasks_controller()
    return jsonify(response), status_code

@api_blueprint.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    response, status_code = get_task_controller(task_id)
    return jsonify(response), status_code

@api_blueprint.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    response, status_code = update_task_controller(task_id, data)
    return jsonify(response), status_code

@api_blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    response, status_code = delete_task_controller(task_id)
    return jsonify(response), status_code