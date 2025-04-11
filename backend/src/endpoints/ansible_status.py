from flask import request, jsonify, make_response

from src.endpoints.ansible_create_inventory import ANSIBLE_ROOT_DIR
from src.helpers.cors import *
from src.helpers.cmd_runner import is_process_running, get_command_output


def handle_ansible_status(app):
    if request.method == "OPTIONS":
        return build_cors_preflight_response(make_response())

    command_status = is_process_running(request.json['pid'])
    command_output = get_command_output(ANSIBLE_ROOT_DIR, 'ansible_run')

    return corsify_actual_response(jsonify({
        'isRunning': command_status,
        'output': command_output
    }))
