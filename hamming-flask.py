from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def index():
	return render_template('encoder.html')

@app.route('/stats')
def stats():
	return render_template('stats.html')

@app.route('/visualization')
def vis():
	return render_template('visualization.html')

@app.route('/countdown')
def countdown():
	return render_template('countdown.html')

@app.route('/form', methods=['GET', 'POST'])
def my_form():
	if(request.method == 'GET'):
		return render_template('my-form.html')

	if(request.method == 'POST'):
		data = mangle(request.form.get('my-text'))
		return data


def mangle(text):
	return text.upper()

if __name__ == "__main__":
    app.run(port=8080, debug=True)
