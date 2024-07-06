document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const formData = new FormData();
    const fileInput = document.getElementById('myfile');
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (response.ok) {
            document.getElementById('pageCount').textContent = `Page Count: ${result.pageCount}`;
        } else {
            document.getElementById('pageCount').textContent = `Error: ${result.error}`;
        }
    } catch (error) {
        document.getElementById('pageCount').textContent = `Error: ${error.message}`;
    }
});

document.getElementById('resetButton').addEventListener('click', function() {
    document.getElementById('uploadForm').reset();
    document.getElementById('pageCount').textContent = '';
});
