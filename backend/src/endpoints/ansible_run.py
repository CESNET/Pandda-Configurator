from flask import request, jsonify, make_response

from src.helpers.cors import *
from src.helpers.cmd_runner import run_ansible_playbook
from src.endpoints.ansible_create_inventory import ANSIBLE_ROOT_DIR


def handle_ansible_run(app):
    if request.method == "OPTIONS":
        return build_cors_preflight_response(make_response())

    target = request.json['host'] if 'host' in request.json else 'all'
    password = request.json['password'] if 'password' in request.json else ''
    pid = run_ansible_playbook(app, ANSIBLE_ROOT_DIR, password, target)

    return corsify_actual_response(jsonify({
        'status': 'OK',
        'PID': pid
    }))
