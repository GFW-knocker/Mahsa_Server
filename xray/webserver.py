import os
import random
from flask import Flask, jsonify
from xray_config_tester import do_test
from flask import request

app = Flask(__name__)


def generate_random_port_number(pid):
    # Set a seed for random number generation based on the process ID
    random.seed(pid)

    # Generate a random number between 100000 and 65535
    random_number = random.randint(10000, 60000)
    return random_number


@app.route("/run-test", methods=['POST'])
def run_test():
    data = request.get_json()

    url = data.get('url')
    outbound_port = generate_random_port_number(os.getpid())
    if url is None:
        return jsonify({"error": "url is missing!"}), 400

    try:
        # run the test
        is_test_ok, avg_speed, avg_latency, ip_result = do_test(url, outbound_port)
    except Exception as e:
        print(f"XRay Test failed: {str(e)}")
        return jsonify({"error": str(e)}), 400

    # return the results
    return jsonify({
        'successful': is_test_ok,
        'avg_speed': avg_speed,
        'avg_latency': avg_latency,
        'server_ip': ip_result,
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
