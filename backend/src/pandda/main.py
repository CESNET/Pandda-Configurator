import os

from src.endpoints.ansible_create_inventory import ANSIBLE_ROOT_DIR
from src.ansible.main import create_inventory
from src.helpers.cryptor import encrypt
from src.helpers.fs import read_file_if_exists
from src.pandda.config import PanddaConfig


def create_config(app, config):
    create_inventory(app, ANSIBLE_ROOT_DIR, config)

    pandda_cfg = PanddaConfig(app, ANSIBLE_ROOT_DIR)
    pandda_cfg.create(config)

    collector_host = config['collector']['host']
    encrypt(app, f'{ANSIBLE_ROOT_DIR}/inventory/group_vars/all/auth.yaml', config['masterPassword'])
    encrypt(app, f'{ANSIBLE_ROOT_DIR}/inventory/host_vars/{collector_host}/vars.yaml', config['masterPassword'])


def load_config(app):
    path = f'{ANSIBLE_ROOT_DIR}/encrypted_config.txt'
    if not os.path.exists(path):
        return False, ''
    return True, read_file_if_exists(path)


def delete_config(app):
    path = f'{ANSIBLE_ROOT_DIR}/encrypted_config.txt'
    if os.path.exists(path):
        os.remove(path)


def save_config(app, config):
    with open(f"{ANSIBLE_ROOT_DIR}/encrypted_config.txt", 'wt') as dst:
        dst.write(f"{config}")
