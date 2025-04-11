import pexpect
import os
import threading

from src.helpers.fs import prepare_ansible_directory


def run_ansible_playbook_async(app, root, process, password):
    process.logfile_read = open(f'{root}/cmd_outputs/ansible_run.txt', 'wt')
    process.expect("Vault password:")
    process.sendline(password)
    process.expect(pexpect.EOF)
    process.interact()

    app.logger.info('Waiting finished')


def prepare_ansible_playbook_command(root, target):
    if target.lower() == 'all':
        return f'ansible-playbook -i {root}/inventory/inventory pandda.yml --ask-vault-pass'
    else:
        return f'ansible-playbook -i {root}/inventory/inventory pandda.yml --limit {target} --ask-vault-pass'


def run_ansible_playbook(app, root, master_password, target):
    prepare_ansible_directory(root)
    command = prepare_ansible_playbook_command(root, target)

    app.logger.info(f'Running {command}')

    my_env = os.environ.copy()
    my_env["ANSIBLE_REMOTE_TEMP"] = "/tmp/.ansible_pandda/tmp"

    child = pexpect.spawn(
        command,
        cwd=root,
        env=my_env,
        encoding="utf-8",
        timeout=None
    )

    child_pid = child.pid

    thread = threading.Thread(target=run_ansible_playbook_async, args=(app, root, child, master_password))
    thread.start()

    return child_pid


def prepare_auto_detection_command(root, ad_root, target):
    return f'ansible-playbook -i {root}/inventory/inventory {ad_root}/auto_discovery.yaml --limit {target} --ask-vault-pass'


def run_auto_detection(app, root, ad_root, master_password, target):
    prepare_ansible_directory(root)
    command = prepare_auto_detection_command(root, ad_root, target)

    app.logger.info(f'Executing "{command}"')

    my_env = os.environ.copy()
    my_env["ANSIBLE_REMOTE_TEMP"] = "/tmp/.ansible_pandda/tmp"

    child = pexpect.spawn(
        command,
        env=my_env,
        encoding="utf-8",
        timeout=None
    )

    child.logfile_read = open(f'{root}/cmd_outputs/auto_discovery.txt', 'wt')
    child.expect("Vault password:")
    child.sendline(master_password)
    child.expect(pexpect.EOF)
    child.wait()


def is_process_running(pid):
    return os.path.exists(f'/proc/{pid}')


def get_command_output(root, program):
    with open(f'{root}/cmd_outputs/{program}.txt', 'rt') as src:
        return src.readlines()
