document.getElementById('convert-btn').addEventListener('click', function() {
    const selectedLanguage = document.getElementById('language-select').value;
    const codeInput = document.getElementById('code-input').value;

    fetch('/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            language: selectedLanguage,
            code: codeInput
        }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('code-output').textContent = data.converted_code;
    })
    .catch(error => console.error('Error:', error));
});
