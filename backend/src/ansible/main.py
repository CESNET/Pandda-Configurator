from src.ansible.inventory import Inventory
from src.helpers.cryptor import encrypt
from src.helpers.fs import prepare_ansible_directory


def create_inventory(app, root, config):
    prepare_ansible_directory(root)

    inventory = Inventory(app, root)
    inventory.create(config)

    encrypt(app, f'{root}/inventory/group_vars/all/auth.yaml', config['masterPassword'])
