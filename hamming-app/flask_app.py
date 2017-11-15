from flask import Flask, render_template, request, url_for, abort, session
from random import randint

from hammingclasses_v2 import HammingEncoder
from hammingclasses_v2 import HammingChecker

import helper

app = Flask(__name__)


@app.route('/')
def index():
    # needs: word, error_rate, codeword, corrupted, corrected, is_success

    if (not session.get('inital_load')):
        word=''
        error_rate=0.00
        codeword=''
        corrupted=''
        corrected=''
        is_success=True

    session['inital_load'] = False

    return render_template('encoder.html', 
                            word=word,
                            error_rate=error_rate,
                            codeword=codeword,
                            corrupted=corrupted,
                            corrected=corrected,
                            is_success=is_success
                        )


@app.route('/', methods=['POST'])
def encode():    
    error_rate = request.form['error-rate']
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
    corrupted = codeword # TODO make corrupt function later
    corrected = checker.correct(corrupted)

    is_success = (codeword == corrected)

    return render_template('encoder.html', 
                            word=word,
                            error_rate=error_rate,
                            codeword=codeword,
                            corrupted=corrupted,
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


# Just leaving this as an example
# Won't actually be used
@app.route('/form', methods=['GET', 'POST'])
def my_form():
    if(request.method == 'GET'):
        return render_template('my-form.html')

    if(request.method == 'POST'):
        data = mangle(request.form.get('my-text'))
        return data


if __name__ == "__main__":
    app.run(port=8080, debug=True)
