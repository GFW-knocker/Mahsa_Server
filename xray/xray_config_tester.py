import json
import shutil
import subprocess
from typing import Tuple
import socket
import time
import requests
import os

xray_path = "../../../bin/xray-linux-amd64-1.8.3"
n_try = 1

def wait_for_port(port: int, host: str = 'localhost', timeout: float = 5.0) -> None:
    # Wait until a port starts accepting TCP connections.
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError as ex:
            time.sleep(0.01)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError(
                    f'Timeout exceeded for the port {port} on host {host} to start accepting connections.') from ex


def start_xray_service(config_path_dir: str, binary_path: str, timeout=5) -> Tuple[subprocess.Popen, dict]:
    # starts the proxy (v2ray/xray) service and waits for the respective port to open
    config_path = config_path_dir+"/config.json"

    with open(config_path, "r") as infile:
        proxy_conf = json.load(infile)

    proxy_listen = "127.0.0.1"  # proxy_conf["inbounds"][0]["listen"]
    # proxy_port = proxy_conf["inbounds"][0]["port"]  # Socks port
    proxy_port = proxy_conf["inbounds"][1]["port"]  # HTTPS port
    proxy_process = subprocess.Popen([binary_path, "-c", "config.json"],
                                     stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL,
                                     cwd=config_path_dir)
    try:
        wait_for_port(host=proxy_listen, port=proxy_port, timeout=timeout)
    except Exception as e:
        remove_dir(config_path_dir)
        proxy_process.kill()
        raise TimeoutError(str(e)) from e
        # proxies = dict(http=f"socks5://{proxy_listen}:{proxy_port}",https=f"socks5://{proxy_listen}:{proxy_port}")
    proxies = dict(http=f"{proxy_listen}:{proxy_port}", https=f"{proxy_listen}:{proxy_port}")

    return proxy_process, proxies


def download_speed_test(n_bytes: int, proxies: dict, timeout: int) -> Tuple[float, float]:
    # tests the download speed using cloudflare servers
    if proxies is None:
        raise TimeoutError("No Xray service available")

    start_time = time.perf_counter()
    r = requests.get(url="https://speed.cloudflare.com/__down",
                     params={"bytes": n_bytes},
                     timeout=timeout,
                     proxies=proxies)
    total_time = time.perf_counter() - start_time
    cf_time = float(r.headers.get("Server-Timing").split("=")[1]) / 1000
    latency = r.elapsed.total_seconds() - cf_time
    download_time = total_time - latency

    mb = n_bytes * 8 / (10 ** 6)
    download_speed = mb / download_time

    return download_speed, latency


def remove_dir(directory):
    # delete the directory
    os.system(f"rm -rf {directory}")


def do_test(config_link, outbound_port):
    config_path_dir = f"./link2json/ports/{outbound_port}"  # path of config , generated by link2json.jar

    if not os.path.exists(config_path_dir):
        os.makedirs(config_path_dir)

    v2ray_config_path = f"{config_path_dir}/v2ray_config.json"

    # copy v2ray_config.json template to the config_path_dir
    shutil.copy("./link2json/v2ray_config_template.json", v2ray_config_path)

    min_dl_speed = 20 * 1024  # 20KBps
    max_dl_time = 3  # sec

    n_bytes = min_dl_speed * max_dl_time

    try:
        # Run the JAR file as a subprocess
        process_java = subprocess.Popen(["java", "-jar", "../../Link2Json.jar", config_link],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        cwd=config_path_dir)
        # Wait for the process to finish and get the output
        stdout, stderr = process_java.communicate()
        # Decode the output
        if len(stdout) != 0:
            output = stdout.decode("utf-8")
        else:
            output = stderr.decode("utf-8")
        if 'Empty' in output:
            remove_dir(config_path_dir)
            raise Exception("empty config.json generated - invalid link (url)")

        xray_config_path = config_path_dir + "/config.json"
        with open(xray_config_path, 'r') as file:
            content = file.read()

        # Replace the port with ours
        new_content = content.replace('10809', str(outbound_port))

        with open(xray_config_path, 'w') as file:
            file.write(new_content)

    except Exception as e:
        remove_dir(config_path_dir)
        raise Exception("Link2Json has failed! " + str(e))

    process_xray, proxies = start_xray_service(config_path_dir, xray_path, 3)

    count = 0
    Ave_speed = 0
    avg_latency = 0
    for try_idx in range(n_try):
        try:
            dl_speed, dl_latency = download_speed_test(n_bytes, proxies, 3)
            Ave_speed = Ave_speed + dl_speed
            avg_latency = avg_latency + dl_latency
            count = count + 1
        except Exception as e:
            remove_dir(config_path_dir)
            process_xray.kill()
            raise Exception("download timeout exceeded? -> " + str(e))

    # make a request to the website
    url = os.environ.get('WEBSITE_URL', 'http://localhost')
    ip_result = None
    try:
        r = requests.get(f"{url}/backend/app/config/ip/", proxies=proxies, timeout=5)
        if r.status_code == 200:
            ip_result = r.json()
    except Exception as e:
        remove_dir(config_path_dir)
        process_xray.kill()
        raise Exception(f"Failed check config server ip! {str(e)}")

    process_xray.kill()

    if count > 0:
        Ave_speed = round(Ave_speed / count, 2)
        avg_latency = round(avg_latency / count, 2)
        print(config_link[:50]+"...", " - successful", "    DL_speed =", Ave_speed, "Mbps", "    Latency =", avg_latency, "sec")
        is_test_ok = True
        return is_test_ok, Ave_speed, avg_latency, ip_result
    else:
        raise Exception("XRay test failed! count = 0")


def check_working_directory():
    current_dir = os.getcwd()
    actual_file_dir = os.path.dirname(os.path.realpath(__file__))
    if current_dir != actual_file_dir:
        os.chdir(actual_file_dir)


# if __name__ == '__main__':
#     check_working_directory()
#
#     do_test(
#         "vless://fa0e6e80-7ede-4c01-b9aa-aa2f43e0afe8@web.yahoo.com:2087?encryption=none&flow=xtls-rprx-vision&security=reality&sni=sni.yahoo.com&fp=firefox&pbk=mykey&sid=myid&spx=myx&type=grpc#test2")
#     do_test(
#         "vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogInRlc3QxIiwNCiAgImFkZCI6ICJ3ZWIuZ29vZ2xlLmNvbSIsDQogICJwb3J0IjogIjQ0MyIsDQogICJpZCI6ICI2MjBjNjAzMS03MDE4LTQ4ODAtOGI3Ny0wOGY4NDY5ZDlmNmQiLA0KICAiYWlkIjogIjAiLA0KICAic2N5IjogImF1dG8iLA0KICAibmV0IjogInRjcCIsDQogICJ0eXBlIjogIm5vbmUiLA0KICAiaG9zdCI6ICJnb29nbGUuY29tIiwNCiAgInBhdGgiOiAiIiwNCiAgInRscyI6ICJ0bHMiLA0KICAic25pIjogInNuaS5nb29nbGUuY29tIiwNCiAgImFscG4iOiAiaDIiLA0KICAiZnAiOiAiYW5kcm9pZCINCn0=")
