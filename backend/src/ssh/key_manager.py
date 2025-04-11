import os


PRI_KEY_FILENAME = 'id_ecdsa'
PUB_KEY_FILENAME = f'{PRI_KEY_FILENAME}.pub'


def remove_if_exists(path):
    if os.path.isfile(path):
        os.remove(path)


def ssh_key_exists(path):
    return os.path.isfile(f'{path}/{PRI_KEY_FILENAME}') and os.path.isfile(f'{path}/{PUB_KEY_FILENAME}')


def generate_ssh_keypair(path, force_new):
    if force_new or not ssh_key_exists(path):
        remove_if_exists(f'{path}/{PRI_KEY_FILENAME}')
        remove_if_exists(f'{path}/{PUB_KEY_FILENAME}')

        os.makedirs(path, exist_ok=True)
        os.system(f"ssh-keygen -t ecdsa -b 256 -f {path}/{PRI_KEY_FILENAME} -q -P '' -C pandda@webconftool")

    with open(f'{path}/{PUB_KEY_FILENAME}', 'rt') as src:
        return src.read()
