import os
import zipfile
import tempfile
import difflib
import re
from flask import render_template, request, jsonify, Blueprint
from markupsafe import Markup

main = Blueprint('main', __name__)
UPLOAD_FOLDER = tempfile.mkdtemp()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload():
    file1 = request.files.get('file1')
    file2 = request.files.get('file2')

    if file1:
        file1_path = os.path.join(UPLOAD_FOLDER, file1.filename)
        file1.save(file1_path)
        print(f"File1 saved at {file1_path}")  # 디버깅용 로그
        dir1 = os.path.join(UPLOAD_FOLDER, os.path.splitext(file1.filename)[0])
        with zipfile.ZipFile(file1_path, 'r') as zip_ref:
            zip_ref.extractall(dir1)
        print(f"File1 extracted to {dir1}")  # 디버깅용 로그
        dir1_structure = get_directory_structure_html(dir1, "original")
        return jsonify(result="Files uploaded successfully", combined_structure={"original_structure": dir1_structure})

    if file2:
        file2_path = os.path.join(UPLOAD_FOLDER, file2.filename)
        file2.save(file2_path)
        print(f"File2 saved at {file2_path}")  # 디버깅용 로그
        with open(file2_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"File2 content: {content[:100]}...")  # 디버깅용 로그 (처음 100자만 출력)
        return jsonify(result="Files uploaded successfully", content=content)

    return jsonify(result="No file uploaded"), 400

def get_directory_structure_html(rootdir, type):
    """
    Creates an HTML representation of the folder structure of rootdir
    """
    structure = "<ul class='directory-list'>"
    for root, dirs, files in os.walk(rootdir):
        for dir_name in dirs:
            structure += f"<li class='directory' data-path='{os.path.join(root, dir_name)}' data-type='{type}'>{dir_name}<ul class='nested'></ul></li>"
        for file_name in files:
            structure += f"<li class='file' data-path='{os.path.join(root, file_name)}' data-type='{type}'>{file_name}</li>"
        break  # Only process the top-level directory
    structure += "</ul>"
    return structure

def get_subdirectories_html(path, type):
    """
    Returns the HTML for the subdirectories and files within the given path
    """
    subdirs = "<ul class='nested active'>"
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            subdirs += f"<li class='directory' data-path='{os.path.join(root, dir_name)}' data-type='{type}'>{dir_name}<ul class='nested'></ul></li>"
        for file_name in files:
            subdirs += f"<li class='file' data-path='{os.path.join(root, file_name)}' data-type='{type}'>{file_name}</li>"
        break
    subdirs += "</ul>"
    return subdirs

@main.route('/subdirectories', methods=['GET'])
def get_subdirectories():
    path = request.args.get('path')
    dir_type = request.args.get('type')
    if not path or not os.path.exists(path):
        return jsonify(result="Directory not found"), 404
    subdirs_html = get_subdirectories_html(path, dir_type)
    return jsonify(result="Subdirectories loaded successfully", subdirectories=subdirs_html)

@main.route('/file', methods=['GET'])
def get_file():
    file_path = request.args.get('path')
    if not file_path or not os.path.exists(file_path):
        return jsonify(result="File not found"), 404
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return jsonify(result="File loaded successfully", content=content)

@main.route('/compare', methods=['POST'])
def compare():
    data = request.get_json()
    original = data.get('original')
    changed = data.get('changed')

    diff = difflib.ndiff(original.splitlines(), changed.splitlines())
    differences = []
    for line in diff:
        if line.startswith('- '):
            differences.append(f"<span style='background-color: #fdd;'>{line[2:]}</span>")
        elif line.startswith('+ '):
            differences.append(f"<span style='background-color: #fdd;'>{line[2:]}</span>")
    differences_html = '<br>'.join(differences)

    return jsonify(differences=Markup(differences_html))
@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    language = data.get('language')
    code = data.get('code')

    # 변환 로직을 호출
    converted_code = code_converter(language, code)

    return jsonify(converted_code=converted_code)

def code_converter(language, code):
    if language == 'python':
        return java_to_python(code)
    elif language == 'java':
        return python_to_java(code)
    elif language == 'c':
        return java_to_c(code)
    else:
        return "Unsupported language"

def java_to_python(code):
    # 주석 변환
    code = re.sub(r'// (.*)', r'# \1', code)

    # 함수 정의 변환
    code = re.sub(r'public static int (\w+)\((.*?)\) {', r'def \1(\2):', code)
    code = re.sub(r'public static void (\w+)\((.*?)\) {', r'def \1(\2):', code)
    code = re.sub(r'public static (\w+) (\w+)\((.*?)\) {', r'def \2(\3):', code)
    code = re.sub(r'public int (\w+)\((.*?)\) {', r'def \1(self, \2):', code)
    code = re.sub(r'public void (\w+)\((.*?)\) {', r'def \1(self, \2):', code)

    # main 함수 변환
    code = re.sub(r'public static void main\(String\[\] args\) {', 'def main():', code)

    # return 변환
    code = re.sub(r'return (.*);', r'return \1', code)

    # print 구문 변환
    code = re.sub(r'System.out.println\((.*?)\);', r'print(\1)', code)

    # 중괄호 및 들여쓰기 변환
    code = code.replace('{', '')
    code = code.replace('}', '')
    code = re.sub(r'(\n\s*)\{(\n\s*)', r'\1\2', code)
    code = re.sub(r'\n\s*\}', r'\n', code)
    code = re.sub(r';', '', code)

    # 클래스 선언 변환
    code = re.sub(r'public class (\w+) {', r'class \1:', code)

    # if 문 변환
    code = re.sub(r'if \((.*?)\) {', r'if \1:', code)
    code = re.sub(r'else {', r'else:', code)

    # 기타 변환
    code = re.sub(r'\n\s*\n', '\n', code)

    # None 반환 처리
    code = re.sub(r'\bnull\b', 'None', code)

    # 들여쓰기 변환
    code = re.sub(r'    ', '    ', code)

    return code.strip()

def python_to_java(code):
    # 주석 변환
    code = re.sub(r'# (.*)', r'// \1', code)

    # 함수 정의 변환
    code = re.sub(r'def (\w+)\((.*?)\):', r'public static int \1(\2) {', code)
    code = re.sub(r'def main\(\):', 'public static void main(String[] args) {', code)

    # return 변환
    code = re.sub(r'return (.*)', r'return \1;', code)

    # print 구문 변환
    code = re.sub(r'print\((.*?)\)', r'System.out.println(\1);', code)

    # 클래스 선언 변환
    code = re.sub(r'class (\w+):', r'public class \1 {', code)

    # if 문 변환
    code = re.sub(r'if (.*):', r'if (\1) {', code)
    code = re.sub(r'else:', r'else {', code)

    # 들여쓰기 변환
    code = re.sub(r'    ', '    ', code)

    # 블록 마무리 변환
    code = re.sub(r'\n(?![^\n]*{)', r'\n}', code)
    code = re.sub(r'\n\s*\n', '\n', code)

    return code.strip()

def java_to_c(code):
    # 주석 변환 (한 줄 주석 및 여러 줄 주석)
    code = re.sub(r'//(.*)', r'/* \1 */', code)
    code = re.sub(r'/\*\*([^*]*\*+)+[^/]*\*/', lambda m: '/*' + m.group(1).replace('*', '').strip() + ' */', code)

    # 함수 정의 변환
    code = re.sub(r'public static int (\w+)\s*\((.*?)\)\s*\{', r'int \1(\2) {', code)
    code = re.sub(r'public static int (\w+)\((.*?)\)\s*\{', r'int \1(\2) {', code)
    code = re.sub(r'public static (\w+)\s+(\w+)\((.*?)\)\s*\{', r'\1 \2(\3) {', code)

    # main 함수 변환
    code = re.sub(r'public static void main\(String\[\] args\)\s*\{', 'int main() {', code)

    # print 구문 변환
    code = re.sub(r'System.out.println\("Error: (.*?)"\);', r'printf("Error: \1\\n");', code)
    code = re.sub(r'System.out.println\("(.*?)"\);', r'printf("\1\\n");', code)
    code = re.sub(r'System.out.println\((.*?)\);', r'printf("%d\\n", \1);', code)
    code = re.sub(r'System.out.println\((.*?), (.*?)\);', r'printf("%s: %d\\n", \1, \2);', code)

    # 변수 선언 변환
    code = re.sub(r'int (\w+) = (.*?);', r'int \1 = \2;', code)

    # 클래스 제거
    code = re.sub(r'public class \w+ \{', '', code)
    code = re.sub(r'\}\s*$', '', code)

    # 중괄호 변환
    code = re.sub(r'\{', '{\n', code)
    code = re.sub(r'\}', '\n}', code)

    # return 0 추가
    code = re.sub(r'\n\s*\}\s*$', '\n    return 0;\n}', code, flags=re.MULTILINE)

    # 최상단에 #include <stdio.h> 추가
    code = '#include <stdio.h>\n\n' + code.strip()

    return code

@main.route('/services')
def services():
    return render_template('services.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/support')
def support():
    return render_template('support.html')

@main.route('/save_changes', methods=['POST'])
def save_changes():
    data = request.get_json()
    changed_content = data.get('changed')

    if not changed_content:
        return jsonify(result="No file content to save."), 400

    save_path = os.path.join(UPLOAD_FOLDER, 'changed_file.txt')

    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(changed_content)
        return jsonify(result="File saved successfully.", file_path=save_path)
    except Exception as e:
        return jsonify(result=f"Failed to save changes: {e}"), 500


