#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base64 import b64decode

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import detectUtils

# configuration
# DEBUG = False

# instantiate the app
app = Flask(__name__, template_folder='templates',
            static_folder='static')
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/detectAudio', methods=['GET', 'POST'])
def detect_audio():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        # transform MIME string to bytes
        audio = b64decode(post_data.get('audio'))
        # call audio detection model here
        # then return its result

        label, max_score = detectUtils.detect_audio(audio)

        response_object['message'] = label

    return jsonify(response_object)


@app.route('/detectImage', methods=['GET', 'POST'])
def detect_image():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        # transform MIME string to bytes
        image = b64decode(post_data.get('image'))
        # call image detection model here
        # then return its result
        label = detectUtils.detect_image(image)

        response_object['message'] = label

    return jsonify(response_object)


@app.route('/detectBoth', methods=['GET', 'POST'])
def detect_both():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        # transform MIME string to bytes
        image = b64decode(post_data.get('image'))
        audio = b64decode(post_data.get('audio'))
        # call image detection model here
        # then return its result
        label = detectUtils.detect_both(audio, image)

        response_object['message'] = label

    return jsonify(response_object)


@app.route('/showResult')
def show_result():
    label = request.args.get('label')
    return render_template('show_file_template.html', label=label, is_image=True, is_show_button=False)


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.config['DEBUG'] = True
    app.run(host="0.0.0.0")
