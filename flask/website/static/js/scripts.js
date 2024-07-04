document.getElementById('file1').addEventListener('change', function() {
    var fileName = this.files[0].name;
    document.getElementById('file1-name').textContent = fileName;
    uploadFile(this, 'original');
});

document.getElementById('file2').addEventListener('change', function() {
    var fileName = this.files[0].name;
    document.getElementById('file2-name').textContent = fileName;
    readFile(this, 'changed');
});

document.getElementById('compare-btn').addEventListener('click', function() {
    compareFiles();
});

document.getElementById('save-changes-btn').addEventListener('click', function() {
    saveChanges();
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
        if (type === 'original') {
            document.getElementById('original-structure-container').innerHTML = data.combined_structure.original_structure;
            addDirectoryToggle();
            addFileClickEvent();
        } else if (type === 'changed') {
            document.getElementById('changed-file-content').innerText = data.content;
        }
    })
    .catch(error => console.error('Error:', error));
}

function readFile(input, type) {
    var file = input.files[0];
    var reader = new FileReader();

    reader.onload = function(event) {
        var content = event.target.result;
        if (type === 'changed') {
            document.getElementById('changed-file-content').innerText = content;
        }
    };

    reader.readAsText(file);
}

function compareFiles() {
    var originalContent = document.getElementById('original-file-content').innerText;
    var changedContent = document.getElementById('changed-file-content').innerText;

    fetch('/compare', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            original: originalContent,
            changed: changedContent
        })
    })
    .then(response => response.json())
    .then(data => {
        var resultElement = document.getElementById('comparison-result');
        resultElement.innerHTML = data.differences;
        resultElement.classList.add('show'); // Add this line to show the result
    })
    .catch(error => console.error('Error:', error));
}

function saveChanges() {
    var changedContent = document.getElementById('changed-file-content').innerText;

    fetch('/save_changes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            changed: changedContent
        })
    })
    .then(response => response.json())
    .then(data => {
        var resultMessageElement = document.getElementById('result-message');
        resultMessageElement.textContent = data.result;

        if (data.result === "File saved successfully.") {
            resultMessageElement.classList.add('success');
            resultMessageElement.classList.remove('error');
            reloadOriginalFile(data.file_path);
        } else {
            resultMessageElement.classList.add('error');
            resultMessageElement.classList.remove('success');
        }
    })
    .catch(error => {
        var resultMessageElement = document.getElementById('result-message');
        resultMessageElement.textContent = 'Failed to save changes.';
        resultMessageElement.classList.add('error');
        resultMessageElement.classList.remove('success');
        console.error('Error:', error);
    });
}

function reloadOriginalFile(filePath) {
    fetch('/file?path=' + encodeURIComponent(filePath))
    .then(response => response.json())
    .then(data => {
        if (data.result === "File loaded successfully") {
            document.getElementById('original-file-content').innerText = data.content;
        } else {
            alert(data.result);
        }
    })
    .catch(error => console.error('Error:', error));
}

let openDirectories = {}; // 열린 디렉토리 상태를 추적하는 객체

function addDirectoryToggle() {
    var toggler = document.getElementsByClassName("directory");
    for (var i = 0; i < toggler.length; i++) {
        var directoryPath = toggler[i].getAttribute("data-path");

        if (!toggler[i].classList.contains("bound")) {
            toggler[i].classList.add("bound");
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
                                openDirectories[path] = true; // 디렉토리를 열린 상태로 설정
                                updateOpenDirectories();
                            } else {
                                alert(data.result);
                            }
                        })
                        .catch(error => console.error('Error:', error));
                    } else {
                        if (nested.classList.contains("active")) {
                            openDirectories[directoryPath] = true;
                        } else {
                            delete openDirectories[directoryPath];
                        }
                        updateOpenDirectories();
                    }
                }
            });
        }

        // 열린 디렉토리를 유지
        if (openDirectories[directoryPath]) {
            toggler[i].classList.add("directory-open");
            var nested = toggler[i].querySelector(".nested");
            if (nested) {
                nested.classList.add("active");
            }
        }
    }
}

function updateOpenDirectories() {
    var toggler = document.getElementsByClassName("directory");
    for (var i = 0; i < toggler.length; i++) {
        var directoryPath = toggler[i].getAttribute("data-path");
        if (openDirectories[directoryPath]) {
            toggler[i].classList.add("directory-open");
            var nested = toggler[i].querySelector(".nested");
            if (nested) {
                nested.classList.add("active");
            }
        } else {
            toggler[i].classList.remove("directory-open");
            var nested = toggler[i].querySelector(".nested");
            if (nested) {
                nested.classList.remove("active");
            }
        }
    }
}

function addFileClickEvent() {
    var files = document.getElementsByClassName("file");
    for (var i = 0; i < files.length; i++) {
        if (!files[i].classList.contains("bound")) {
            files[i].classList.add("bound");
            files[i].addEventListener("click", function() {
                var filePath = this.getAttribute("data-path");
                var fileType = this.getAttribute("data-type");
                fetch('/file?path=' + encodeURIComponent(filePath))
                .then(response => response.json())
                .then(data => {
                    if (data.result === "File loaded successfully") {
                        if (fileType === 'original') {
                            document.getElementById('original-file-content').innerText = data.content;
                        }
                    } else {
                        alert(data.result);
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        }
    }
}
