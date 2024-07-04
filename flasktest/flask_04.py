from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route('/a_page')
def go_a():
    return 'This is a_page'


@app.route('/b_page/<c_data>')
def go_b(c_data):
    return 'This is b_page with %s' %c_data


@app.route('/c_page/<c_value>')
def go_c_data(c_value):
    print(c_value)
    if c_value == "a":
        return redirect(url_for('go_a'))
    else:
        return redirect(url_for('go_b', c_data = c_value))


if __name__ == '__main__':
    app.run(host='0.0.0.0')