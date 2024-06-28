document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(event.target);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === "Files uploaded successfully") {
            document.getElementById('results').innerHTML = data.combined_structure;
            addDirectoryToggle();
        } else {
            document.getElementById('results').innerHTML = data.result;
        }
    })
    .catch(error => console.error('Error:', error));
});

function addDirectoryToggle() {
    var toggler = document.getElementsByClassName("directory");
    for (var i = 0; i < toggler.length; i++) {
        toggler[i].addEventListener("click", function() {
            this.parentElement.querySelector(".nested").classList.toggle("active");
            this.classList.toggle("directory-open");
        });
    }
}