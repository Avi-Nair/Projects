# app.py
from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_program', methods=['POST'])
def run_program():
    Kc = request.form['Kc']
    BluetoothAddress = request.form['BluetoothAddress']
    Clock = request.form['Clock']
    L = request.form['L']
    PlainText = request.form['PlainText']
    mode = request.form['mode']

    # Get the absolute path to the Python program
    script_path = os.path.abspath('main.py')

    # Construct the command to run the Python program
    command = ['python', script_path, Kc, BluetoothAddress, Clock, L, PlainText, mode]

    try:
        # Run the Python program using subprocess
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

        return render_template('result.html', result=result.stdout, error=result.stderr)
    except Exception as e:
        return render_template('result.html', result='', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)