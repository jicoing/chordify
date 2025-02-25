document.getElementById('uploadButton').addEventListener('click', function() {
    const fileInput = document.getElementById('fileUpload');
    const file = fileInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        // Show the loading indicator
        const loadingIndicator = document.getElementById('loadingIndicator');
        loadingIndicator.style.display = 'block';

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Hide the loading indicator
            loadingIndicator.style.display = 'none';
            
            if (data.chords) {
                document.getElementById('chordResults').innerText = 'Recognized Chords,Duration(min:sec):\n' + data.chords.join('\n');
            } else {
                document.getElementById('chordResults').innerText = 'Error: ' + data.error;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert('Please select an MP3 file to upload.');
    }
});
