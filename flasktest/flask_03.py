from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route('/a_page')
def go_a():
    return 'This is a_page'


@app.route('/c_page')
def go_c():
    return redirect(url_for('go_a'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)