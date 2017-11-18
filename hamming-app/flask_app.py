#!/usr/bin/env python3

from flask import Flask, render_template, request, url_for, abort, session
from random import randint
from collections import namedtuple

from hammingclasses import HammingEncoder
from hammingclasses import HammingChecker
from hammingclasses import add_noise

app = Flask(__name__)


@app.route('/')
def index():
    """Handles the initial load only"""
    return render_template('encoder.html', word='', error_rate=0.00, codeword='', \
        corrupted='', bits_corrupted=0, corrected='', is_success=True)


@app.route('/', methods=['POST'])
def encode():    
    error_rate = float(request.form['error-rate'])
    parameter = int(request.form['parameter'])

    if request.form['submit'] == 'Encode':
        word = request.form['word']
    elif request.form['submit'] == 'Random':
        # create random word
        word = ''
        for _ in range(2 ** parameter - parameter - 1):
            word += str(randint(0, 1))

    encoder = HammingEncoder(parameter)
    checker = HammingChecker(parameter)

    codeword = encoder.encode(word)

    noise_value = add_noise(codeword, error_rate)
    corrupted = noise_value[0]
    bits_corrupted = noise_value[1]
    corrected = checker.correct(corrupted)

    is_success = (codeword == corrected)

    return render_template('encoder.html', 
                            word=word,
                            error_rate=error_rate,
                            codeword=codeword,
                            corrupted=corrupted,
                            bits_corrupted=bits_corrupted,
                            corrected=corrected,
                            is_success=is_success
                        )



@app.route('/stats')
def stats():
    return render_template('stats.html')


@app.route('/visualization')
def vis():
    return render_template('visualization.html')


@app.route('/countdown')
def countdown():
    return render_template('countdown.html')


if __name__ == "__main__":
    app.run(port=8080, debug=True)
