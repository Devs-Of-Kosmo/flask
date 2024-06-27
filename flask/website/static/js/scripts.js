function compareTexts() {
    const text1 = document.getElementById('text1').value;
    const text2 = document.getElementById('text2').value;

    fetch('/compare', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `text1=${encodeURIComponent(text1)}&text2=${encodeURIComponent(text2)}`
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerHTML = `<p style="color: ${data.result === 'Texts are identical' ? 'green' : 'red'};">${data.result}</p>`;
        if (data.result !== "Texts are identical") {
            document.getElementById('result').innerHTML += `<pre>${data.diff_html}</pre>`;
        }
    });
}