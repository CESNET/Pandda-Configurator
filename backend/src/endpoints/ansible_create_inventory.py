from flask import request, jsonify, make_response, abort

from src.helpers.cors import *
from src.ansible.main import create_inventory


ANSIBLE_ROOT_DIR = '/opt/pandda_playbooks/ansible'


def handle_ansible_create_inventory(app):
    if request.method == "OPTIONS":
        return build_cors_preflight_response(make_response())

    create_inventory(app, ANSIBLE_ROOT_DIR, request.json['config'])
    return corsify_actual_response(make_response())
