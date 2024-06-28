document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(event.target);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === "File uploaded successfully") {
            document.getElementById('directoryStructure').innerHTML = '<pre>' + JSON.stringify(data.dir_structure, null, 2) + '</pre>';
            document.getElementById('projectDir').value = data.project_dir;
            document.getElementById('packageForm').style.display = 'block';
        } else {
            document.getElementById('directoryStructure').innerHTML = data.result;
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('packageSelectForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(event.target);

    fetch('/package', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === "Package directory fetched successfully") {
            document.getElementById('directoryStructure').innerHTML = '<pre>' + JSON.stringify(data.dir_structure, null, 2) + '</pre>';
        } else {
            document.getElementById('directoryStructure').innerHTML = data.result;
        }
    })
    .catch(error => console.error('Error:', error));
});