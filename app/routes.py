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