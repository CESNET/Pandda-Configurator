import os
import subprocess

from flask import request, jsonify, make_response, abort

from src.auto_discovery.main import read_machine_info
from src.endpoints.ansible_create_inventory import ANSIBLE_ROOT_DIR
from src.helpers.cmd_runner import run_auto_detection, get_command_output
from src.helpers.cors import *

AUTO_DISCOVERY_ROOT = '/opt/pandda_autodiscovery'


def handle_machine_info(app):
    if request.method == "OPTIONS":
        return build_cors_preflight_response(make_response())

    root = ANSIBLE_ROOT_DIR
    ad_root = AUTO_DISCOVERY_ROOT
    master_password = request.json['masterPassword']
    target = request.json['host']

    try:
        run_auto_detection(app, root, ad_root, master_password, target)
        machine_info = read_machine_info(target)
        cmd_output = get_command_output(root, 'auto_discovery')
    except Exception as e:
        app.logger.error(f'Exception handle_machine_info(): {e}')
        return abort(500)

    return corsify_actual_response(make_response({
        'machine_info': machine_info,
        'ad_output': cmd_output
    }))
