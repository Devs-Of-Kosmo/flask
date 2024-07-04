from flask import Flask

app = Flask(__name__)


@app.route('/abc')
def index():
    return '<html><body><h1>Hello World !!!!</h1><hr></body></html>'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
