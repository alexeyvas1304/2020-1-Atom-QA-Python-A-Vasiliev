from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, SSHException
from user_data import CENTOS_HOSTNAME, USERNAME, PASSWORD, NON_DEFAULT_SSH_PORT


class SSH:
    def __init__(self, **kwargs):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.kwargs = kwargs

    def __enter__(self):
        kw = self.kwargs
        try:
            self.client.connect(
                hostname=kw.get('hostname'),
                port=int(kw.get('port', 22)),
                username=kw.get('username'),
                password=kw.get('password'),
            )
        except AuthenticationException:
            print("Authentication failed, please verify your credentials")
        except SSHException as sshException:
            print(f"Could not establish SSH connection {sshException}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def exec_cmd(self, cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        data = stdout.read()
        data = data.decode()

        return data


if __name__ == '__main__':
    with SSH(hostname=CENTOS_HOSTNAME, username=USERNAME, password=PASSWORD, port=NON_DEFAULT_SSH_PORT) as ssh:
        print(ssh.exec_cmd('echo centos | sudo -S cat /var/log/messages'))
