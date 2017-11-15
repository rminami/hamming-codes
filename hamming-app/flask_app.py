from flask import Flask, render_template, request, url_for, abort, session

from hammingclasses import HammingEncoder
from hammingclasses import HammingChecker

import helper

app = Flask(__name__)


@app.route('/')
def index():
    # needs: word, error_rate, codeword, corrupted, corrected, is_success

    if (not session.get('inital_load')):
        word='0110'
        error_rate=0.00
        codeword='1100110'
        corrupted='1100110'
        corrected='1100110'
        is_success=True

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

    word = request.form['word']
    error_rate = request.form['error-rate']

    parameter = request.form['parameter']

    # Here comes the fun part
    encoder = HammingEncoder(4) # do size stuff later
    checker = HammingChecker(4)

    codeword = helper.arr_to_str(encoder.encode(helper.str_to_arr(word)))
    corrupted = helper.arr_to_str(helper.corrupt(helper.str_to_arr(codeword), error_rate))
    corrected = helper.arr_to_str(checker.correct(helper.str_to_arr(corrupted)))
    is_success = (codeword == corrected)

    return render_template('encoder.html', 
                            word=word,
                            error_rate=error_rate,
                            codeword=codeword,
                            corrupted=corrupted,
                            corrected=corrected,
                            is_success=is_success
                        )

@app.route('/random', methods=['POST'])


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
