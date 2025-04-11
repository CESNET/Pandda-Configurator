from src.ssh.key_manager import PRI_KEY_FILENAME


class Inventory:
    def __init__(self, app, root):
        self.__app = app
        self.__root = root
        self.__password_index = 0
        self.__auth_info = []
        self.__inventory = []

    def create(self, config):
        self.__add_probes_info(config)
        self.__add_collector_info(config)
        self.__save_to_file(f"{self.__root}/inventory/inventory", self.__inventory)
        self.__save_to_file(f"{self.__root}/inventory/group_vars/all/auth.yaml", self.__auth_info)

    def __add_probes_info(self, config):
        self.__inventory.append("[metering_point]")
        for server_info in config["probeList"]:
            self.__add_host(server_info, config["globalSSHLogin"])
            self.__password_index += 1

    def __add_collector_info(self, config):
        self.__inventory.append("[collector]")
        self.__add_host(config["collector"], config["globalSSHLogin"])

    def __add_host(self, host_info, global_ssh_credentials):
        item = host_info["host"]
        ssh_credentials = self.__select_ssh_credentials(host_info, global_ssh_credentials)
        item += f" ansible_ssh_user={ssh_credentials['user']}"
        if ssh_credentials["type"] == "sshLoginTypePasswd":
            self.__auth_info.append(f'host{self.__password_index}_password: "{ssh_credentials["pass"]}"\n')
            item += f' ansible_ssh_pass="{{{{ host{self.__password_index}_password }}}}"'
        else:
            item += f" ansible_ssh_private_key_file={self.__root}/inventory/keys/{PRI_KEY_FILENAME}"

        self.__inventory.append(item)

    @staticmethod
    def __select_ssh_credentials(host_info, global_ssh_credentials):
        return global_ssh_credentials if host_info["sshCredentials"] == "default" else host_info["customCredentials"]

    @staticmethod
    def __save_to_file(path, data):
        with open(path, 'wt') as dst:
            dst.write('\n'.join(data))
            dst.write('\n')
