import numpy as np
import requests

import logging
import os
import time

from flask import (Flask, request, url_for, render_template, abort,
                   send_from_directory)
# POI analysis model
from model import poi
app = Flask(__name__)
app.config['PATH_TO_OUPUT_DATA'] = os.path.join(os.getcwd(), 'result_data')


@app.route('/poiAnalysis/place', methods=['GET', 'POST'])
def place_read():
    return render_template('place_read.html')


@app.route('/poiAnalysis/result', methods=['POST'])
def process_place_result():
    """
    Handles HTTP request by saving and processing place.

    Returns:
        method call to `show_place_success` that calls to render our results'
        template with the request result
    """
    place_result = {}
    request_timestamp = int(time.time() * 1000)
    place_result['timestamp'] = request_timestamp

    input_text = request.form['text']
    if input_text == '':
        abort(406, "No text provided")

    place_result['text_input'] = input_text

    processed_place_output = poi.main(
        input_text, app.config['PATH_TO_OUPUT_DATA'])
    print('Pre-processing done! \n')
    place_result['poi_data'] = url_for('get_file', filename='poi_data.png')
    place_result['street_with_poi'] = url_for(
        'get_file', filename='street_with_poi.png')
    place_result['type_of_poi'] = url_for(
        'get_file', filename='type_of_poi.png')
    print (place_result['poi_data'])
    return show_place_result(place_result)


@app.route('/poiAnalysis/result/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['PATH_TO_OUPUT_DATA'], filename,
                               as_attachment=True)


def show_place_result(place_result):
    """
    Handles successful place Analysis
    and returns the render_template for Flask

    Args:
        place_result (dict): Request processing and result information

    Returns:
        (:obj:`flask.render_template`)
    """
    return render_template('place_result.html', **place_result)


def main():
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == '__main__':
    main()
