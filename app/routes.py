#!/usr/bin/python3

from flask import Blueprint, request, jsonify
from .controllers import *

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/clock-in', methods=['POST'])
def clock_in():
    data = request.json
    employee_id = data.get('employee_id')

    # Call controller function to handle clock-in
    response, status_code = clock_in_employee(employee_id)
    return jsonify(response), status_code

@api_blueprint.route('/clock-out', methods=['POST'])
def clock_out():
    data = request.json
    employee_id = data.get('employee_id')

    # Call controller function to handle clock-out
    response, status_code = clock_out_employee(employee_id)
    return jsonify(response), status_code

@api_blueprint.route('/attendance/<int:employee_id>', methods=['GET'])
def get_attendance(employee_id):
    # Call controller function to get attendance records
    response, status_code = get_employee_attendance(employee_id)
    return jsonify(response), status_code

@api_blueprint.route('/candidates', methods=['POST'])
def create_candidate():
    data = request.get_json()
    response, status_code = create_candidate_controller(data)
    return jsonify(response), status_code

@api_blueprint.route('/candidates/<int:id>', methods=['GET'])
def get_candidate(id):
    response = get_candidate_controller(id)
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

@api_blueprint.route('/departments', methods=['POST'])
def create_department():
    data = request.get_json()
    response, status_code = create_department_controller(data)
    return jsonify(response), status_code