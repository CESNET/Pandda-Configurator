import os


def prepare_ansible_directory(root):
    os.makedirs(root, exist_ok=True)
    os.makedirs(f"{root}/cmd_outputs", exist_ok=True)
    os.makedirs(f"{root}/inventory", exist_ok=True)
    os.makedirs(f"{root}/inventory/group_vars/all", exist_ok=True)
    os.makedirs(f"{root}/inventory/host_files", exist_ok=True)
    os.makedirs(f"{root}/inventory/host_vars", exist_ok=True)


def prepare_host_files_directories(root, hosts):
    for host in hosts:
        os.makedirs(f"{root}/inventory/host_files/{host}", exist_ok=True)


def prepare_host_vars_directory(root, host):
    os.makedirs(f"{root}/inventory/host_vars/{host}", exist_ok=True)


def prepare_hugepages_directory(root, host):
    os.makedirs(f"{root}/inventory/host_files/{host}/hugepages", exist_ok=True)


def read_file_if_exists(path, flatten=True):
    if not os.path.exists(path):
        return ''

    with open(path, 'rt') as src:
        lines = src.readlines()
        return lines[0] if flatten and len(lines) == 1 else lines
