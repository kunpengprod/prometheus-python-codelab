# The Docker image contains the following code
from flask import Flask
from prometheus_client import start_http_server, Counter, Summary

import logging
import os
import random
import socket
import sys
import time

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request.')

REQUEST_COUNT = Counter('request_count', 'Count of requests received.', ['endpoint'])

app = Flask(__name__)

@app.route("/")
@REQUEST_TIME.time()
def index():
    REQUEST_COUNT.labels('/').inc()
    print "Responding to client."
    html = "<h3>Hello, World!</h3>\n"
    time.sleep(random.random())
    return html

@app.route("/contact")
@REQUEST_TIME.time()
def contact():
    REQUEST_COUNT.labels('/contact').inc()
    print "Responding to client in Chinese."
    html = "<h3>Please call us at +1 234 567 8901</h3>\n"
    time.sleep(random.random() + 0.5)
    return html

if __name__ == "__main__":
  # Redirect logging to stdout.
  logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

  # Metrics.
  logging.info("Starting exporting metrics.")
  start_http_server(9090)

  # Http server.
  logging.info("Starting http server.")
  app.run(host='0.0.0.0', port=80)

