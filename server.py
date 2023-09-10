
from flask import Flask, jsonify, request
from flask_cors import CORS
from wrapper import *
import re

HEIGHT_REGEX = re.compile(r'height="(\d+\.?\d*)(\w*)"', re.IGNORECASE)
WIDTH_REGEX = re.compile(r'width="(\d+\.?\d*)(\w*)"', re.IGNORECASE)

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['POST'])
def work_post():
    data = request.json
    expression = data['expression']

    images = wrapper(
        expression, HEIGHT_REGEX, WIDTH_REGEX)

    response = {
        'expression': expression,
        'images': images
    }

    return jsonify(response), 200


@app.route("/healthz", methods=['GET'])
def salute():
    return 'Hello from iAutomaton server!', 200
