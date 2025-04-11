from flask import request, jsonify, make_response

from src.helpers.cors import *
from src.pandda.main import load_config


def handle_pandda_load_config(app):
    if request.method == "OPTIONS":
        return build_cors_preflight_response(make_response())

    exists, pandda_cfg = load_config(app)
    response = jsonify({
        'exists': exists,
        'encrypted': pandda_cfg
    })

    return corsify_actual_response(response)
