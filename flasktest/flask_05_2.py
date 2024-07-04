from flask import Flask, render_template

#from flask_cors import CORS

app = Flask(__name__)

#CORS(app)

@app.route('/hello/<int:score>')
def hello_name(score):
    return render_template('templates_05_2.html', marks=score)


if __name__ == '__main__':
    app.run(debug=True)