from flask import Blueprint, render_template, request, jsonify
import difflib

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
            continue
        else:
            diff_html.append(char[2])

    return ''.join(diff_html)