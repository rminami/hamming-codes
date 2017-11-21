#!/usr/bin/env python3

from flask import Flask, render_template, request, url_for, abort, session, jsonify
from collections import namedtuple
import random
import time

from hammingclasses import HammingEncoder
from hammingclasses import HammingChecker
from hammingclasses import add_noise

app = Flask(__name__)


@app.route('/')
def index():
    """Handles the initial load only"""
    return render_template('jqueryencoder.html', words='', error_rate=0.00, parameter=3, \
        codeword='', corrupted='', bits_corrupted=0, corrected='', is_success=True)


@app.route('/_rawdata', methods=['POST'])
def rawdata():
    # return data as dict
    error_rate = request.form.get('error_rate', 0, type=float)
    r = request.form.get('parameter', 3, type=int)
    k = 2 ** r - r - 1

    if request.form.get('submit') == 'Encode':
        words = request.form['words']
        remainder = len(words) % k

        if remainder != 0:
            words += '0' * (k - remainder)

    elif request.form.get('submit') == 'Random':
        words = ''.join([random.choice(('0', '1')) for _ in range(k)])

    encoder = HammingEncoder(r) # TODO use previous one if parameter hasn't changed
    checker = HammingChecker(r)

    codewords = ''
    corrupted = ''
    corrected = ''
    bits_corrupted = 0
    try:
        for i in range(int(len(words) / k)):
            word = words[i*k : (i+1)*k]
            cw = encoder.encode(word)
            cw_corrupted, cw_bits_corrupted = add_noise(cw, error_rate)
            cw_corrected = checker.correct(cw_corrupted)

            codewords += cw
            corrupted += cw_corrupted
            bits_corrupted += cw_bits_corrupted
            corrected += cw_corrected

        is_success = (codewords == corrected)

        hamming_dict = {
            'words': words,
            'codewords': codewords,
            'corrupted': corrupted,
            'bits_corrupted': bits_corrupted,
            'corrected': corrected,
            'is_success': is_success
        }
        return jsonify(hamming_dict)
        
    except ValueError as e:
        response = jsonify({'code': 400,'message': str(e)})
        response.status_code = 400
        return response


@app.route('/stats', methods=['GET', 'POST'])
def statview():
    StatRow = namedtuple('StatRow', ['parameter', 'length', 'data_ratio', 'theory_rate', 'test_rate'])
    tablerows = []

    if request.method == 'POST':
        
        p = float(request.form['error-rate'])
        no_of_tests = int(request.form['no-of-tests'])

        start_time_all = time.time()

        for r in range(2, 7):

            start_time = time.time()

            n = 2 ** r - 1
            theory_rate = (1 - p) ** n + n * p * (1 - p) ** (n - 1)

            encoder = HammingEncoder(r)
            checker = HammingChecker(r)

            no_of_successes = 0

            for _ in range(no_of_tests):
                word = random_word(n - r)
                codeword = encoder.encode(word)
                corrupted, bits_corrupted = add_noise(codeword, p)
                corrected = checker.correct(corrupted)
                if codeword == corrected:
                    no_of_successes += 1

            theory_rate = (1 - p) ** n + n * p * (1 - p) ** (n - 1)
            test_rate = no_of_successes / no_of_tests

            row = StatRow(r, n, '{0:.4f}'.format((n - r)/n), '{0:.2f}%'.format(theory_rate * 100), '{0:.2f}%'.format(test_rate * 100))
            tablerows.append(row)

            print('r = %d took %f seconds' % (r, time.time() - start_time))

        print('total time %f seconds' % (time.time() - start_time_all))

        return render_template('stats.html', error_rate=p, no_of_tests=no_of_tests, tablerows=tablerows)

    elif request.method == 'GET':
        # handles the initial render only
        for r in range(2, 7):
            n = 2 ** r - 1
            row = StatRow(r, n, '{0:.2f}'.format((n - r)/n), '-', '-')
            tablerows.append(row)

        return render_template('stats.html', error_rate=0.01, no_of_tests=1000, tablerows=tablerows)


@app.route('/visualization')
def vis():
    return render_template('visualization.html')


@app.route('/countdown')
def countdown():
    return render_template('countdown.html')

def random_word(len):
    """Returns random binary word at the given length"""
    return ''.join([random.choice(('0', '1')) for _ in range(len)])


if __name__ == "__main__":
    app.run(port=8080, debug=True)


