from flask import request, jsonify, make_response

from src.helpers.cors import *
from src.ssh.key_manager import generate_ssh_keypair


def handle_ssh_get_key(app):
    if request.method == "OPTIONS":
        return build_cors_preflight_response(make_response())

    force_new = request.json['forceNew'] if 'forceNew' in request.json else False
    response = jsonify({
        'pubKey': generate_ssh_keypair('/opt/pandda_playbooks/ansible/inventory/keys', force_new)
    })

    return corsify_actual_response(response)
