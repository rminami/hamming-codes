#!/usr/bin/env python3

from flask import Flask, render_template, request, url_for, abort, session
from collections import namedtuple
import random

from hammingclasses import HammingEncoder
from hammingclasses import HammingChecker
from hammingclasses import add_noise

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def encode():

    if request.method == 'POST':

        error_rate = float(request.form['error-rate'])
        parameter = int(request.form['parameter'])

        if request.form['submit'] == 'Encode':
            word = request.form['word']

        elif request.form['submit'] == 'Random':
            word = ''.join([random.choice(('0', '1')) for _ in range(2 ** parameter - parameter - 1)])

        encoder = HammingEncoder(parameter) # TODO use previous one if parameter hasn't changed
        checker = HammingChecker(parameter)

        codeword = encoder.encode(word)
        corrupted, bits_corrupted = add_noise(codeword, error_rate)
        corrected = checker.correct(corrupted)
        is_success = (codeword == corrected)

        return render_template('encoder.html', word=word, error_rate=error_rate, \
            parameter=parameter, codeword=codeword, corrupted=corrupted, \
            bits_corrupted=bits_corrupted, corrected=corrected, is_success=is_success)

    elif request.method == 'GET':
        """Handles the initial load only"""
        return render_template('encoder.html', word='', error_rate=0.00, parameter=3, \
            codeword='', corrupted='', bits_corrupted=0, corrected='', is_success=True)



@app.route('/stats', methods=['GET', 'POST'])
def statview():
    StatRow = namedtuple('StatRow', ['parameter', 'length', 'data_ratio', 'theory_rate', 'test_rate'])
    tablerows = []

    if request.method == 'POST':
        
        p = float(request.form['error-rate'])
        no_of_tests = int(request.form['no-of-tests'])


        for r in range(2, 7):
            n = 2 ** r - 1
            theory_rate = (1 - p) ** n + n * p * (1 - p) ** (n - 1)

            encoder = HammingEncoder(r)
            checker = HammingChecker(r)

            no_successful = 0

            for _ in range(no_of_tests):
                word = random_word(n - r)
                codeword = encoder.encode(word)
                corrupted, bits_corrupted = add_noise(codeword, p)

                corrected = checker.correct(corrupted)
                if codeword == corrected:
                    no_successful += 1

            theory_rate = (1 - p) ** n + n * p * (1 - p) ** (n - 1)
            test_rate = no_successful / no_of_tests

            row = StatRow(r, n, '{0:.4f}'.format((n - r)/n), '{0:.2f}%'.format(theory_rate * 100), '{0:.2f}%'.format(test_rate * 100))
            tablerows.append(row)

        return render_template('stats.html', error_rate=p, no_of_tests=no_of_tests, tablerows=tablerows)

    elif request.method == 'GET':
        # handles the initial render only
        p = 0.01 
        for r in range(2, 7):
            n = 2 ** r - 1
            row = StatRow(r, n, '{0:.2f}'.format((n - r)/n), '-', '-')
            tablerows.append(row)

        return render_template('stats.html', error_rate=0.01, no_of_tests=500, tablerows=tablerows)


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


