import logging
import traceback

from flask import Flask, abort

from src.endpoints.ansible_create_inventory import handle_ansible_create_inventory
from src.endpoints.ansible_run import handle_ansible_run
from src.endpoints.ansible_status import handle_ansible_status
from src.endpoints.machine_info import handle_machine_info
from src.endpoints.pandda_create_config import handle_pandda_create_config
from src.endpoints.pandda_load_config import handle_pandda_load_config
from src.endpoints.pandda_delete_config import handle_pandda_delete_config
from src.endpoints.ssh_get_key import handle_ssh_get_key


app = Flask(__name__)


def handle_request(endpoint, callback):
    app.logger.info(f'Processing /{endpoint}')
    try:
        return callback(app)
    except Exception as e:
        app.logger.critical(e)
        app.logger.critical(traceback.format_exc())
        return abort(500)


@app.route("/ANSIBLE_CREATE_INVENTORY", methods=['POST','OPTIONS'])
def ansible_create_inventory():
    return handle_request('ANSIBLE_CREATE_INVENTORY', handle_ansible_create_inventory)


@app.route("/ANSIBLE_RUN", methods=['POST','OPTIONS'])
def ansible_run():
    return handle_request('ANSIBLE_RUN', handle_ansible_run)


@app.route("/ANSIBLE_STATUS", methods=['POST','OPTIONS'])
def ansible_status():
    return handle_request('ANSIBLE_STATUS', handle_ansible_status)


@app.route("/MACHINE_INFO", methods=['POST','OPTIONS'])
def machine_info():
    return handle_request('MACHINE_INFO', handle_machine_info)


@app.route("/PANDDA_CREATE_CONFIG", methods=['POST','OPTIONS'])
def pandda_create_config():
    return handle_request('PANDDA_CREATE_CONFIG', handle_pandda_create_config)


@app.route("/PANDDA_LOAD_CONFIG", methods=['POST','OPTIONS'])
def pandda_load_config():
    return handle_request('PANDDA_LOAD_CONFIG', handle_pandda_load_config)


@app.route("/PANDDA_DELETE_CONFIG", methods=['POST','OPTIONS'])
def pandda_delete_config():
    return handle_request('PANDDA_DELETE_CONFIG', handle_pandda_delete_config)


@app.route("/SSH_GET_KEY", methods=['POST','OPTIONS'])
def ssh_get_key():
    return handle_request('SSH_GET_KEY', handle_ssh_get_key)


if '__name__' == '__main__':
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
