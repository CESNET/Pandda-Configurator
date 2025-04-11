from flask import request, jsonify, make_response

from src.helpers.cors import *
from src.pandda.main import delete_config


def handle_pandda_delete_config(app):
    if request.method == "OPTIONS":
        return build_cors_preflight_response(make_response())

    delete_config(app)

    return corsify_actual_response(make_response())
