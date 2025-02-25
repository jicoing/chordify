# Chord Recognition Web App Context

## Purpose
Create a free web application that analyzes MP3 files and displays recognized musical chords using an existing Python chord recognition script.

## Features
1. **Core Functionality**
   - MP3 file upload (max 5MB)
   - Audio processing with Python backend
   - Chord recognition results display
   - Basic error handling

2. **User Interface**
   - File upload button
   - Progress indicator
   - Results display section
   - Simple instructions/FAQ

3. **Technical**
   - Flask web framework
   - Python audio processing stack
   - Bootstrap frontend
   - Client-side file validation

## Technical Requirements

### Backend
- Python 3.8+
- Flask web framework
- Audio processing libraries:
  - Librosa
  - Essentia
  - Chord recognition script
- FFmpeg (for audio conversion if needed)

### Frontend
- HTML5/CSS3
- Bootstrap 5
- JavaScript for:
  - File upload handling
  - Progress updates
  - Result display

### Infrastructure
- **Development**: Local testing with Flask dev server
- **Production**: Free hosting options:
  - PythonAnywhere (free tier)
  - Render (free tier)
  - Fly.io (free allowance)

## Development Approach

1. **Setup**
```bash
# Basic project structure
/chord-app
  ├── app.py
  ├── chord_detector.py
  ├── templates/
  │    └── index.html
  ├── static/
  ├── requirements.txt