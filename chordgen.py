import logging
import librosa
import numpy as np
from scipy.signal import medfilt
import soundfile as sf

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chord_detection.log'),
        logging.StreamHandler()
    ]
)

def generate_chord_templates():
    """Generate chord templates for major and minor triads"""
    logging.debug("Generating chord templates...")
    templates = []
    chord_names = []
    for root in range(12):
        # Major triad template
        major = np.zeros(12)
        major[[root, (root+4)%12, (root+7)%12]] = 1
        major /= np.linalg.norm(major)
        templates.append(major)
        chord_names.append(f"{librosa.midi_to_note(root+60)[:-1]}:maj")
        
        # Minor triad template
        minor = np.zeros(12)
        minor[[root, (root+3)%12, (root+7)%12]] = 1
        minor /= np.linalg.norm(minor)
        templates.append(minor)
        chord_names.append(f"{librosa.midi_to_note(root+60)[:-1]}:min")
    
    logging.info(f"Generated {len(templates)} chord templates")
    return np.array(templates), chord_names

def format_time(seconds):
    """Convert seconds to minutes:seconds format"""
    return f"{int(seconds//60)}:{int(seconds%60):02d}"

def detect_chords(audio_path, hop_length=4096, n_fft=2048, 
                  min_duration=0.5, output_file=None):
    """Optimized chord detection with reduced computational complexity"""
    try:
        # Load audio and convert to mono
        y, sr = sf.read(audio_path)
        if y.ndim > 1:
            y = np.mean(y, axis=1)
        
        # Downsample to 16 kHz with faster resampling
        y = librosa.resample(y, orig_sr=sr, target_sr=16000, res_type='kaiser_fast')
        sr = 16000
        logging.info(f"Resampled to {sr}Hz, new length: {len(y)/sr:.2f}s")

        # Compute optimized chromagram
        chroma = librosa.feature.chroma_stft(
            y=y, sr=sr,
            hop_length=hop_length,
            n_fft=n_fft,
            norm=2,
            center=False  # Faster computation with reduced padding
        )
        
        # Get chord templates
        templates, chord_names = generate_chord_templates()
        
        # Template matching with matrix multiplication
        chord_scores = templates @ chroma
        chord_ids = np.argmax(chord_scores, axis=0)
        
        # Smooth with median filter
        chord_ids = medfilt(chord_ids, kernel_size=3)  # Reduced kernel size
        
        # Convert frame indices to timestamps
        times = librosa.frames_to_time(
            np.arange(chroma.shape[1]), 
            sr=sr, hop_length=hop_length
        )
        
        # Track chord segments
        current_chord = None
        start_time = 0
        results = []
        for time, cid in zip(times, chord_ids):
            if cid != current_chord:
                if current_chord is not None and (time - start_time) >= min_duration:
                    results.append((
                        chord_names[current_chord],
                        format_time(start_time),
                        format_time(time)
                    ))
                current_chord = cid
                start_time = time
        
        # Add final segment
        if current_chord is not None and (times[-1] - start_time) >= min_duration:
            results.append((
                chord_names[current_chord],
                format_time(start_time),
                format_time(times[-1])
            ))
        
        # Optional output file
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                for name, start, end in results:
                    f.write(f"{start}-{end}: {name}\n")
        
        return results
    except Exception as e:
        logging.error(f"Error processing audio: {str(e)}", exc_info=True)
        return []

if __name__ == "__main__":
    audio_file = "abyss-173653.mp3"
    logging.info(f"Processing audio file: {audio_file}")
    detected_chords = detect_chords(audio_file)
    
    if detected_chords:
        logging.info("Chord detection completed successfully")
        print("\nDetected chords:")
        for chord, start, end in detected_chords:
            print(f"{start}-{end}: {chord}")
    else:
        logging.warning("No chords detected or processing failed")
        print("No chords detected in the audio file")