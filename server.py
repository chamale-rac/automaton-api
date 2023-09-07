
from flask import Flask, jsonify, request
from flask_cors import CORS
from wrappers import *
import re

HEIGHT_REGEX = re.compile(r'height="(\d+\.?\d*)(\w*)"', re.IGNORECASE)
WIDTH_REGEX = re.compile(r'width="(\d+\.?\d*)(\w*)"', re.IGNORECASE)

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['POST'])
def work_post():
    data = request.json
    expression = data['expression']

    images = []
    images.append(AbstractSyntaxTreeWrapper(
        expression, HEIGHT_REGEX, WIDTH_REGEX))
    images.append(AbstractSyntaxTreeWrapper(
        'a|b|c*asd', HEIGHT_REGEX, WIDTH_REGEX))
    images.append(AbstractSyntaxTreeWrapper(
        'ax?', HEIGHT_REGEX, WIDTH_REGEX))
    images.append(AbstractSyntaxTreeWrapper(
        'npm(install)*', HEIGHT_REGEX, WIDTH_REGEX))

    images.append(AbstractSyntaxTreeWrapper(
        expression, HEIGHT_REGEX, WIDTH_REGEX))
    images.append(AbstractSyntaxTreeWrapper(
        'a|b|c*asd', HEIGHT_REGEX, WIDTH_REGEX))
    images.append(AbstractSyntaxTreeWrapper(
        'ax?', HEIGHT_REGEX, WIDTH_REGEX))
    images.append(AbstractSyntaxTreeWrapper(
        'npm(install)*', HEIGHT_REGEX, WIDTH_REGEX))

    response = {
        'expression': expression,
        'images': images
    }

    return jsonify(response), 200


@app.route("/", methods=['GET'])
def work_get():
    # data = request.json
    # expression = data['expression']
    expression = "[0-3]"

    images = []
    images.append(AbstractSyntaxTreeWrapper(
        expression, HEIGHT_REGEX, WIDTH_REGEX))

    response = {
        'expression': expression,
        'images': images
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run()
