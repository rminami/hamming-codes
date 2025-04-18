#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify, current_app
from collections import namedtuple
import random

from .hammingclasses import HammingChecker, HammingEncoder, add_noise

app = Flask(__name__)


@app.route('/')
def index():
    """Handles the initial load only"""
    current_app.r = 3
    current_app.encoder = HammingEncoder(3)
    current_app.checker = HammingChecker(3)

    return render_template('encoder.html', words='', error_rate=0.00, parameter=3, \
        codeword='', corrupted='', bits_corrupted=0, corrected='', is_success=True)


@app.route('/_rawdata', methods=['POST'])
def rawdata():
    try:
        error_rate = request.form.get('error_rate', type=float)

        if error_rate < 0 or error_rate > 1:
            raise ValueError("Error rate must be between 0 and 1.")

        r = request.form.get('parameter', type=int)
        k = 2 ** r - r - 1

        if request.form.get('submit') == 'Encode':
            words = request.form['words']

            if len(words) % k != 0:
                words += '0' * (k - (len(words) % k)) # adds padding

        elif request.form.get('submit') == 'Random':
            words = ''.join([random.choice(('0', '1')) for _ in range(k)]) 

        if r != current_app.r:
            current_app.r = r
            current_app.encoder = HammingEncoder(r)
            current_app.checker = HammingChecker(r)

        codewords = ''
        corrupted = ''
        corrected = ''
        bits_corrupted = 0

        for i in range(int(len(words) / k)):
            word = words[i*k : (i+1)*k]
            cw = current_app.encoder.encode(word)
            cw_corrupted, cw_bits_corrupted = add_noise(cw, error_rate)
            cw_corrected = current_app.checker.correct(cw_corrupted)

            codewords += cw
            corrupted += cw_corrupted
            bits_corrupted += cw_bits_corrupted
            corrected += cw_corrected

        is_success = (codewords == corrected)

        hamming_data = {
            'words': words,
            'codewords': codewords,
            'corrupted': corrupted,
            'bits_corrupted': bits_corrupted,
            'corrected': corrected,
            'is_success': is_success
        }
        return jsonify(hamming_data)
        
    except ValueError as e:
        response = jsonify({'code': 400,'message': str(e)})
        response.status_code = 400
        return response


@app.route('/_statdata', methods=['POST'])
def statdata():
    r = request.form.get('r', type=int)
    p = request.form.get('p', type=float)
    no_of_tests = request.form.get('no_of_tests', type=int)

    encoder = HammingEncoder(r)
    checker = HammingChecker(r)

    k = 2 ** r - 1 - r
    no_of_successes = 0

    for _ in range(no_of_tests):
        word = random_word(k)
        codeword = encoder.encode(word)
        corrupted, bits_corrupted = add_noise(codeword, p)
        corrected = checker.correct(corrupted)
        if codeword == corrected:
            no_of_successes += 1

    test_rate = '{0:.2f}'.format(no_of_successes / no_of_tests * 100)

    test_data = {
        'test_rate': test_rate
    }
    return jsonify(test_data)


@app.route('/stats', methods=['GET'])
def statview():
    StatRow = namedtuple('StatRow', ['parameter', 'length', 'data_ratio'])
    tablerows = []

    # handles the initial render only
    for r in range(2, 7):
        n = 2 ** r - 1
        row = StatRow(r, n, '{0:.4f}'.format((n - r)/n))
        tablerows.append(row)

    return render_template('stats.html', error_rate=0.01, no_of_tests=1000, tablerows=tablerows)


# ---- Helper functions --- #

def random_word(len):
    """Returns random binary word at the given length"""
    return ''.join([random.choice(('0', '1')) for _ in range(len)])


# ---- Flask app launcher --- #

if __name__ == "__main__":
    with app.app_context():
        app.run(port=8080)
