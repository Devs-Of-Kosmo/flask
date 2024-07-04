from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello World flask_02 !!!!'


@app.route('/user/<userName>')
def user(userName):
    return 'Hello %s' %(userName)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="9999", debug=False)