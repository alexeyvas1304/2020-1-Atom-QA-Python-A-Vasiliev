import pytest
import requests
from user_data import PASSWORD, CENTOS_HOSTNAME, NON_DEFAULT_HTTP_PORT


@pytest.mark.LINUX
def test_root(ssh_client):
    res1 = ssh_client.exec_cmd('whoami')
    assert res1.strip() == 'centos'
    res2 = ssh_client.exec_cmd(f'echo {PASSWORD} | sudo -S whoami')
    assert res2.strip() == 'root'
    messages = ssh_client.exec_cmd(f'echo {PASSWORD} | sudo -S cat /var/log/messages')
    assert len(messages) != 0


@pytest.mark.LINUX
def test_nginx_running_http(ssh_client):
    r = requests.get(f'http://{CENTOS_HOSTNAME}:{NON_DEFAULT_HTTP_PORT}')
    assert r.status_code == 200


@pytest.mark.LINUX
def test_nginx_running_ssh(ssh_client):
    command = ssh_client.exec_cmd('systemctl status nginx')
    assert "active (running)" in command
    command = ssh_client.exec_cmd(F'echo {PASSWORD} | sudo -S netstat -tulpn | grep nginx')
    assert f':{NON_DEFAULT_HTTP_PORT}' in command
    assert ':80' not in command


@pytest.mark.LINUX
def test_access_log(ssh_client):
    lines_before = ssh_client.exec_cmd(f'echo {PASSWORD} | sudo -S cat /var/log/nginx/access.log | wc -l')
    r = requests.get(f'http://{CENTOS_HOSTNAME}:{NON_DEFAULT_HTTP_PORT}')
    lines_after = ssh_client.exec_cmd(f'echo {PASSWORD} | sudo -S cat /var/log/nginx/access.log | wc -l')
    assert int(lines_after) == int(lines_before) + 1
    last_string = ssh_client.exec_cmd(f'echo {PASSWORD} | sudo -S cat /var/log/nginx/access.log | tail -n 1')
    assert 'python-requests' in last_string


@pytest.mark.LINUX
def test_nginx_firewalld(ssh_client):
    ssh_client.exec_cmd(
        f'echo {PASSWORD} | sudo -S firewall-cmd --permanent --zone=public --remove-port={NON_DEFAULT_HTTP_PORT}/tcp')
    ssh_client.exec_cmd(f'echo {PASSWORD} | sudo -S firewall-cmd --reload')  # ОБЯЗАТЕЛЬНО !!!
    ssh_client.exec_cmd(f'echo {PASSWORD} | sudo -S systemctl restart nginx')  # вроде не обязательно

    command = ssh_client.exec_cmd(f'echo {PASSWORD} | sudo -S systemctl status nginx')
    assert "active (running)" in command

    with pytest.raises(requests.exceptions.ConnectionError):
        r = requests.get(f'http://{CENTOS_HOSTNAME}:{NON_DEFAULT_HTTP_PORT}')

    ssh_client.exec_cmd(
        f'echo {PASSWORD} | sudo -S firewall-cmd --permanent --zone=public --add-port={NON_DEFAULT_HTTP_PORT}/tcp')  # подчищаю за собой
    ssh_client.exec_cmd(f'echo {PASSWORD} | sudo -S firewall-cmd --reload')
    ssh_client.exec_cmd(f'echo {PASSWORD} | sudo -S systemctl restart nginx')
