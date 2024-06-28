import os
import zipfile
import tempfile
import shutil
from flask import render_template, request, jsonify, Blueprint, Markup

main = Blueprint('main', __name__)
UPLOAD_FOLDER = tempfile.mkdtemp()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload():
    file1 = request.files.get('file1')
    file2 = request.files.get('file2')

    if not file1 or not file2:
        return jsonify(result="Both files must be uploaded"), 400

    file1_path = os.path.join(UPLOAD_FOLDER, file1.filename)
    file2_path = os.path.join(UPLOAD_FOLDER, file2.filename)

    file1.save(file1_path)
    file2.save(file2_path)

    # Extract the uploaded files
    dir1 = os.path.join(UPLOAD_FOLDER, os.path.splitext(file1.filename)[0])
    dir2 = os.path.join(UPLOAD_FOLDER, os.path.splitext(file2.filename)[0])

    with zipfile.ZipFile(file1_path, 'r') as zip_ref:
        zip_ref.extractall(dir1)
    with zipfile.ZipFile(file2_path, 'r') as zip_ref:
        zip_ref.extractall(dir2)

    # Get the directory structures
    dir1_structure = get_directory_structure_html(dir1)
    dir2_structure = get_directory_structure_html(dir2)

    combined_structure = Markup(f"""
        <div class='structure-container'>
            <div class='structure'>
                <h3>Original File Structure</h3>
                {dir1_structure}
            </div>
            <div class='structure'>
                <h3>Changed File Structure</h3>
                {dir2_structure}
            </div>
        </div>
    """)

    return jsonify(result="Files uploaded successfully", combined_structure=combined_structure)

def get_directory_structure_html(rootdir):
    """
    Creates an HTML representation of the folder structure of rootdir
    """
    structure = "<ul class='directory-list'>"
    for root, dirs, files in os.walk(rootdir):
        if root == rootdir:
            for dir_name in dirs:
                structure += f"<li class='directory'>{dir_name}{get_subdirectories(os.path.join(root, dir_name))}</li>"
            for file_name in files:
                structure += f"<li class='file'>{file_name}</li>"
            break  # Only process the top-level directory
    structure += "</ul>"
    return structure

def get_subdirectories(rootdir):
    """
    Creates an HTML representation of subdirectories for a given directory
    """
    structure = "<ul class='nested'>"
    for root, dirs, files in os.walk(rootdir):
        for dir_name in dirs:
            structure += f"<li class='directory'>{dir_name}{get_subdirectories(os.path.join(root, dir_name))}</li>"
        for file_name in files:
            structure += f"<li class='file'>{file_name}</li>"
        break  # Only process the immediate subdirectories
    structure += "</ul>"
    return structure