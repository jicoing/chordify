from flask import Flask, request, jsonify, render_template
import os
from chordgen import detect_chords

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.mp3'):
        audio_path = os.path.join('uploads', file.filename)
        file.save(audio_path)
        chords = detect_chords(audio_path)
        return jsonify({'chords': chords}), 200
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=False)
