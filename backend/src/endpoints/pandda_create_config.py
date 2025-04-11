from flask import request, jsonify, make_response

from src.helpers.cors import *
from src.pandda.main import create_config, save_config


def handle_pandda_create_config(app):
    if request.method == "OPTIONS":
        return build_cors_preflight_response(make_response())

    create_config(app, request.json['config'])
    save_config(app, request.json['encrypted'])

    response = jsonify(request.json['config'])
    return corsify_actual_response(response)
