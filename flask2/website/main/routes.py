import os
import zipfile
import tempfile
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
        dir1 = os.path.join(UPLOAD_FOLDER, os.path.splitext(file1.filename)[0])
        with zipfile.ZipFile(file1_path, 'r') as zip_ref:
            zip_ref.extractall(dir1)
        dir1_structure = get_directory_structure_html(dir1, "original")
        return jsonify(result="Files uploaded successfully", combined_structure={"original_structure": dir1_structure})

    if file2:
        file2_path = os.path.join(UPLOAD_FOLDER, file2.filename)
        file2.save(file2_path)
        dir2 = os.path.join(UPLOAD_FOLDER, os.path.splitext(file2.filename)[0])
        with zipfile.ZipFile(file2_path, 'r') as zip_ref:
            zip_ref.extractall(dir2)
        dir2_structure = get_directory_structure_html(dir2, "changed")
        return jsonify(result="Files uploaded successfully", combined_structure={"changed_structure": dir2_structure})

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
