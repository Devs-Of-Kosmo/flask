from flask import Flask, render_template, request, jsonify, Blueprint
import difflib
import requests

app = Flask(__name__)

# Flask 블루프린트 생성
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/compare', methods=['POST'])
def compare():
    text1 = request.form.get('text1', '').strip()
    text2 = request.form.get('text2', '').strip()

    if not text1 or not text2:
        return jsonify(result="Both text fields must be filled"), 400

    diff_html = generate_diff_html(text1, text2)

    result = "Texts are identical" if text1 == text2 else "Texts are different"
    return jsonify(result=result, diff_html=diff_html)

def generate_diff_html(text1, text2):
    diff = list(difflib.ndiff(text1, text2))
    diff_html = []

    for char in diff:
        if char.startswith('- '):
            diff_html.append(f"<span style='background-color: red;'>{char[2]}</span>")
        elif char.startswith('+ '):
            diff_html.append(f"<span style='background-color: green;'>{char[2]}</span>")
        else:
            diff_html.append(char[2])

    return ''.join(diff_html)

@main.route('/submit', methods=['POST'])
def submit_data():
    data = {
        "name": request.form['name'],
        "age": request.form['age']
    }
    response = requests.post('http://localhost:8080/send-data', json=data)
    return jsonify(response.json())

received_data = []

@main.route('/receive-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    received_data.append(data)
    return jsonify({"message": "Data received", "data": data}), 200

@main.route('/view-data', methods=['GET'])
def view_data():
    return jsonify(received_data), 200

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(port=5000)
