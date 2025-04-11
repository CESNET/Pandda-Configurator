import json
import os


MACHINE_INFO_ROOT = '/opt/pandda_autodiscovery/machine_info'


def read_machine_info(host):
    path = f'{MACHINE_INFO_ROOT}/{host}/extracted_machine_info.json'

    if not os.path.isfile(path):
        return dict()

    with open(path, 'rt') as src:
        return json.load(src)
