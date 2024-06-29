document.getElementById('file1').addEventListener('change', function() {
    var fileName = this.files[0].name;
    document.getElementById('file1-name').textContent = fileName;
    uploadFile(this, 'original');
});

document.getElementById('file2').addEventListener('change', function() {
    var fileName = this.files[0].name;
    document.getElementById('file2-name').textContent = fileName;
    uploadFile(this, 'changed');
});

function uploadFile(input, type) {
    var formData = new FormData();
    formData.append(input.name, input.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === "Files uploaded successfully") {
            if (type === 'original') {
                document.getElementById('original-structure-container').innerHTML = data.combined_structure.original_structure;
            } else {
                document.getElementById('changed-structure-container').innerHTML = data.combined_structure.changed_structure;
            }
            addDirectoryToggle();
            addFileClickEvent();
        } else {
            alert(data.result);
        }
    })
    .catch(error => console.error('Error:', error));
}

function addDirectoryToggle() {
    var toggler = document.getElementsByClassName("directory");
    for (var i = 0; i < toggler.length; i++) {
        toggler[i].addEventListener("click", function() {
            var nested = this.querySelector(".nested");
            if (nested) {
                nested.classList.toggle("active");
                this.classList.toggle("directory-open");

                if (nested.innerHTML === "") {
                    var path = this.getAttribute("data-path");
                    var type = this.getAttribute("data-type");
                    fetch(`/subdirectories?path=${encodeURIComponent(path)}&type=${type}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.result === "Subdirectories loaded successfully") {
                            nested.innerHTML = data.subdirectories;
                            addDirectoryToggle();
                            addFileClickEvent();
                        } else {
                            alert(data.result);
                        }
                    })
                    .catch(error => console.error('Error:', error));
                }
            }
        });
    }
}

function addFileClickEvent() {
    var files = document.getElementsByClassName("file");
    for (var i = 0; i < files.length; i++) {
        files[i].addEventListener("click", function() {
            var filePath = this.getAttribute("data-path");
            var fileType = this.getAttribute("data-type");
            fetch('/file?path=' + encodeURIComponent(filePath))
            .then(response => response.json())
            .then(data => {
                if (data.result === "File loaded successfully") {
                    if (fileType === 'original') {
                        document.getElementById('original-file-content').innerText = data.content;
                    } else {
                        document.getElementById('changed-file-content').innerText = data.content;
                    }
                } else {
                    alert(data.result);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
}
