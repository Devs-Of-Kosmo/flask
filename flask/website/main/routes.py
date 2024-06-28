import os
import zipfile
import tempfile
import shutil
from flask import render_template, request, jsonify, Blueprint

main = Blueprint('main', __name__)
UPLOAD_FOLDER = tempfile.mkdtemp()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files.get('project')

    if not uploaded_file:
        return jsonify(result="No file uploaded"), 400

    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(file_path)

    # Extract the uploaded file
    project_dir = os.path.join(UPLOAD_FOLDER, os.path.splitext(uploaded_file.filename)[0])
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(project_dir)

    # Get the top-level directory structure
    dir_structure = get_top_level_structure(project_dir)

    return jsonify(result="File uploaded successfully", dir_structure=dir_structure, project_dir=project_dir)

def get_top_level_structure(rootdir):
    """
    Creates a dictionary that represents the top-level folder structure of rootdir
    """
    dir_structure = {}
    for item in os.listdir(rootdir):
        item_path = os.path.join(rootdir, item)
        if os.path.isdir(item_path):
            dir_structure[item] = 'directory'
        else:
            dir_structure[item] = 'file'
    return dir_structure

@main.route('/package', methods=['POST'])
def package():
    project_dir = request.form.get('project_dir')
    package_name = request.form.get('package_name')

    if not project_dir or not package_name:
        return jsonify(result="Project directory or package name not specified"), 400

    package_path = os.path.join(project_dir, package_name)

    if not os.path.exists(package_path):
        return jsonify(result="Specified package does not exist"), 400

    dir_structure = get_directory_structure(package_path)

    return jsonify(result="Package directory fetched successfully", dir_structure=dir_structure)

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir_structure = {}
    for dirpath, dirnames, filenames in os.walk(rootdir):
        folder = os.path.relpath(dirpath, rootdir)
        subdir = dir_structure
        if folder != '.':
            for part in folder.split(os.sep):
                subdir = subdir.setdefault(part, {})
        for filename in filenames:
            subdir[filename] = None
    return dir_structure