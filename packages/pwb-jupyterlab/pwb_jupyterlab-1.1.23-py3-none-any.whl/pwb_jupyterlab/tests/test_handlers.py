import signal
import json
import os
import psutil
import pytest
import requests
import subprocess
import time

from pwb_jupyterlab.constants import URL_ENDPOINT, SERVER_ENDPOINT, QUARTO_APP

async def test_url_endpoint(jp_fetch):
    response = await jp_fetch("pwb-jupyterlab", URL_ENDPOINT)
    assert response.code == 200, "Failed to fetch URL endpoint"
    payload = json.loads(response.body)
    assert payload == {
        "baseSessionUrl": os.getenv('RS_SERVER_URL') + os.getenv('RS_SESSION_URL')
    }

async def test_servers_endpoint_empty(jp_fetch, request):
    response = await jp_fetch("pwb-jupyterlab", SERVER_ENDPOINT)
    assert response.code == 200, "Failed to fetch servers"
    assert json.loads(response.body) == {"servers": []}, "Servers should be empty"

async def test_servers_endpoint(jp_fetch, request):
    # initialize servers endpoint
    response = await jp_fetch("pwb-jupyterlab", SERVER_ENDPOINT)
    assert response.code == 200, "Failed to fetch servers"
    assert json.loads(response.body) == {"servers": []}, "Servers should be empty"

    # start a server in a subprocess
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8044"])
    def terminate_process():
        server_process.terminate()
        server_process.wait()
    request.addfinalizer(terminate_process)

    # allow time for the server to start
    time.sleep(1)
    response = requests.get("http://localhost:8044")
    assert response.status_code == 200, "Server is not running or accessible"

    # test the servers endpoint contains the proxied server
    response = await jp_fetch("pwb-jupyterlab", SERVER_ENDPOINT)
    assert response.code == 200, "Failed to fetch servers"
    payload = json.loads(response.body)
    server = payload['servers'][0]
    assert server['port'] == '8044', f"Expected server port 8044, got '{server['port']}'"
    assert server['pid'] == f'{server_process.pid}', f"Expected server pid {server_process.pid}, got '{server['pid']}'"
    if os.path.exists('/usr/lib/rstudio-server/bin/rserver-url'):
        assert server['secure_port'] == '9b2cf135', f"Expected server secure port 9b2cf135, got '{server['secure_port']}'"

async def test_quarto_server(jp_fetch, request):
    if request.config.getoption("--jenkins"):
        pytest.skip("Test skipped on Jenkins")
    # initialize servers endpoint
    response = await jp_fetch("pwb-jupyterlab", SERVER_ENDPOINT)
    assert response.code == 200, "Failed to fetch servers"
    assert json.loads(response.body) == {"servers": []}, "Servers should be empty"

    # start a quarto server in a subprocess, requires a process group to terminate children processes
    quarto_process = subprocess.Popen(["quarto", "preview", "./pwb_jupyterlab/tests/resources/hello.qmd"], preexec_fn=os.setsid)
    def terminate_process():
        if quarto_process and quarto_process.pid and psutil.pid_exists(quarto_process.pid):
           os.killpg(os.getpgid(quarto_process.pid), signal.SIGTERM)
    request.addfinalizer(terminate_process)

    # quarto requires additional time to start up
    time.sleep(10)

    response = await jp_fetch("pwb-jupyterlab", SERVER_ENDPOINT)
    assert response.code == 200, "Failed to fetch servers"
    server = json.loads(response.body)['servers'][0]
    
    # assert quarto server has expected name
    current_dir = os.path.basename(os.getcwd())
    expected_label = f'{current_dir} - {QUARTO_APP}'
    server['label'] = server['label'].strip()
    assert server['label'] == expected_label, f"Expected server label '{expected_label}', got '{server['label']}'"

async def test_quarto_notebook(jp_fetch, request):
    if request.config.getoption("--jenkins"):
        pytest.skip("Test skipped on Jenkins")
    # initialize servers endpoint
    response = await jp_fetch("pwb-jupyterlab", SERVER_ENDPOINT)
    assert response.code == 200, "Failed to fetch servers"
    assert json.loads(response.body) == {"servers": []}, "Servers should be empty"
    
    # start a quarto server in a subprocess, requires a process group to terminate children processes
    quarto_process = subprocess.Popen(["quarto", "preview", "./pwb_jupyterlab/tests/resources/basics-jupyter.ipynb"], preexec_fn=os.setsid)
    def terminate_process():
        if quarto_process and quarto_process.pid and psutil.pid_exists(quarto_process.pid):
           os.killpg(os.getpgid(quarto_process.pid), signal.SIGTERM)
    request.addfinalizer(terminate_process)

    # quarto requires additional time to start up
    time.sleep(5)

    response = await jp_fetch("pwb-jupyterlab", SERVER_ENDPOINT)
    assert response.code == 200, "Failed to fetch servers"
    server = json.loads(response.body)['servers'][0]
    # assert quarto server has expected name
    current_dir = os.path.basename(os.getcwd())
    expected_label = f'{current_dir} - {QUARTO_APP}'
    server['label'] = server['label'].strip()
    assert server['label'] == expected_label, f"Expected server label '{expected_label}', got '{server['label']}'"
    print(f"All assertions made")
