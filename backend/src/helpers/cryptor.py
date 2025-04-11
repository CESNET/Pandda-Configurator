import pexpect
import os


def encrypt(app, file, password):
    try:
        child = pexpect.spawn(f'ansible-vault encrypt {file}')
        child.expect(".*password.*")
        child.sendline(password)
        child.expect(".*password.*")
        child.sendline(password)
        child.expect(pexpect.EOF)
        os.system(f'chmod 0644 {file}')
    except Exception as e:
        app.error(f'crypt::encrypt_file: {e}')
