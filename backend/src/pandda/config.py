import hashlib

from src.helpers.fs import prepare_host_files_directories, prepare_host_vars_directory, prepare_hugepages_directory
from src.pandda.parser import read_cfg_from_UI


class PanddaConfig:
    def __init__(self, app, root):
        self.__app = app
        self.__root = root

    def create(self, config):
        per_ip_configs = read_cfg_from_UI(config)

        prepare_host_files_directories(self.__root, per_ip_configs.keys())
        prepare_host_vars_directory(self.__root, config['collector']['host'])

        self.__create_host_vars(config)
        self.__create_yamls(per_ip_configs)
        self.__create_hugepages_cfgs(per_ip_configs)

    def __create_yamls(self, per_ip_configs):
        for host, cfg in per_ip_configs.items():
            self.__cfg_to_yaml(self.__get_pandda_config_path(host), cfg)

    def __create_hugepages_cfgs(self, per_ip_configs):
        for host, cfg in per_ip_configs.items():
            self.__create_hugepages_cfg_if_needed(host, cfg)

    def __create_host_vars(self, config):
        col_host = config['collector']['host']
        install_adict = 'true' if config['collector']['adict'] else 'false'

        with open(f"{self.__root}/inventory/host_vars/{col_host}/vars.yaml", 'wt') as vars:
            vars.write(f'install_adict: {install_adict}\n')
            if config['collector']['adict']:
                vars.write(f'adict_gui_user: "{config["adict"]["user"]["name"]}"\n')
                vars.write(f'adict_gui_pass: "{config["adict"]["user"]["pass"]}"\n')

    def __get_hugepages_cfg_path(self, host):
        return f"{self.__root}/inventory/host_files/{host}/hugepages/hugepages.cfg"

    def __get_pandda_config_path(self, host):
        return f"{self.__root}/inventory/host_files/{host}/pandda.yaml"

    def __create_hugepages_cfg_if_needed(self, host, config):
        if self.__is_dpdk_present(config):
            prepare_hugepages_directory(self.__root, host)
            with open(self.__get_hugepages_cfg_path(host), 'wt') as dst:
                dst.write(f'{config["probe"]["hugepages"]}\n')

    def __cfg_to_yaml(self, path, config):
        with open(path, 'wt') as cfg_file:
            if 'probe' in config:
                self.__put_probe_cfg(cfg_file, config)
            if 'collector' in config:
                self.__put_collector_cfg(cfg_file, config)
                if config['collector']['adict']['enabled']:
                    self.__put_adict_cfg(cfg_file, config['collector']['adict'])

    def __put_adict_cfg(self, cfg_file, adict):
        cfg_file.write('- adict:\n')
        cfg_file.write(f'    data_folder: "{adict["data_folder"]}"\n')
        if len(adict['protected_ranges']) > 0:
            cfg_file.write('    protected_prefixes:\n')
            for protected in adict['protected_ranges']:
                cfg_file.write(f'        - "{protected}"\n')

    def __put_collector_cfg(self, cfg_file, collector):
        cfg_file.write('- collector:\n')
        cfg_file.write(f'    host: {collector["collector"]["host"]}\n')
        cfg_file.write(f'    port: {collector["collector"]["port"]}\n')
        cfg_file.write(f'    proto: "{collector["collector"]["proto"]}"\n')
        if len(collector['collector']['forward_targets']) > 0:
            cfg_file.write('    forward_targets:\n')
            for fwdTarget in collector['collector']['forward_targets']:
                cfg_file.write(f'        - {{ host: "{fwdTarget["host"]}", port: {fwdTarget["port"]}, proto: "{fwdTarget["proto"]}" }}\n')

    def __put_probe_cfg(self, cfg_file, probe):
        cfg_file.write('- probes:\n')
        for idx, ins in enumerate(probe['probe']['ipfixprobe_instances']):
            uid = self.__unique_name(ins["host"], ins["type"], idx)
            instance_name = f'{ins["type"]}_{uid}'
            cfg_file.write(f'    - instance_name: {instance_name}\n')

            cfg_file.write(f'      input_plugin:\n')
            cfg_file.write(f'        {ins["type"]}:\n')
            for k, v in ins[ins['type']].items():
                if isinstance(v, str):
                    cfg_file.write(f'          {k}: "{v}"\n')
                else:
                    cfg_file.write(f'          {k}: {v}\n')

            cfg_file.write(f'      storage:\n')
            cfg_file.write(f'        cache:\n')
            cfg_file.write(f'          size_exponent: {ins["cacheSize"]}\n')
            cfg_file.write(f'        timeouts:\n')
            cfg_file.write(f'          active: {ins["activeTimeout"]}\n')
            cfg_file.write(f'          inactive: {ins["passiveTimeout"]}\n')

            cfg_file.write(f'      process_plugins:\n')
            for k, v in ins['plugins'].items():
                cfg_file.write(f'        - {k}\n')

            cfg_file.write(f'      output_plugin:\n')
            cfg_file.write(f'        ipfix:\n')
            cfg_file.write(f'          collector:\n')
            cfg_file.write(f'            host: "{ins["colHost"]}"\n')
            cfg_file.write(f'            port: {ins["colPort"]}\n')
            cfg_file.write(f'          exporter:\n')
            cfg_file.write(f'            id: {ins["linkID"]}\n')
            cfg_file.write(f'          protocol:\n')
            cfg_file.write(f'            {ins["protocol"]}:\n')
            if ins["protocol"] == 'tcp':
                cfg_file.write(f'              non_blocking: false\n')
            else:
                cfg_file.write(f'              template_refresh: 60\n')

            cfg_file.write(f'      telemetry:\n')
            cfg_file.write(f'        appfs:\n')
            cfg_file.write(f'          enabled: true\n')
            cfg_file.write(f'          mount_point: "/run/ipfixprobe_{instance_name}"\n')

    @staticmethod
    def __unique_name(host, in_type, index):
        return hashlib.sha256(f'{host}{in_type}{index}'.encode('utf-8')).hexdigest()[0:4]

    @staticmethod
    def __is_dpdk_present(config):
        if 'probe' not in config:
            return False
        for ins in config['probe']['ipfixprobe_instances']:
            if ins['type'] == 'dpdk':
                return True
        return False
