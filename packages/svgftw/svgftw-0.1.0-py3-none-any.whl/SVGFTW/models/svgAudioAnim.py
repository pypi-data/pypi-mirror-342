import librosa
import numpy as np
import svgpathtools
from pydub import AudioSegment
from pydub.playback import play
import threading
import time
from flask import Flask, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Audio Analysis Configuration
BEAT_SENSITIVITY = 1.2
FREQ_BANDS = {
    'bass': (20, 200),
    'mid': (200, 2000),
    'treble': (2000, 20000)
}

class AudioVisualizer:
    def __init__(self, audio_path, svg_path):
        self.audio_path = audio_path
        self.svg_path = svg_path
        self.beat_times = []
        self.tempo = 0
        self.frequencies = None
        self.current_beat = 0
        self.start_time = 0
        self.is_playing = False

        # Load and analyze audio
        self.audio, self.sr = self._load_audio()
        self._analyze_audio()
        
        # Load SVG elements
        self.svg = svgpathtools.Document(svg_path)
        self.elements = {
            'circle': self.svg.paths[0] if self.svg.paths else None,
            'rect': self.svg.rects[0] if self.svg.rects else None
        }

    def _load_audio(self):
        if self.audio_path.endswith('.mid'):
            return self._process_midi()
        return librosa.load(self.audio_path, sr=None)

    def _analyze_audio(self):
        if self.audio_path.endswith('.mid'):
            return  # MIDI processing handled separately
        
        # Detect beats and tempo
        tempo, beat_frames = librosa.beat.beat_track(
            y=self.audio, sr=self.sr, units='time')
        self.beat_times = beat_frames.tolist()
        self.tempo = tempo

        # Frequency analysis
        self.frequencies = np.abs(librosa.stft(self.audio))

    def _process_midi(self):
        import pretty_midi
        midi = pretty_midi.PrettyMIDI(self.audio_path)
        self.tempo = midi.estimate_tempo()
        self.beat_times = midi.get_beats()
        return None, None  # MIDI has no raw audio data

    def _get_energy(self, current_time):
        if self.audio_path.endswith('.mid'):
            return 0.5  # Placeholder for MIDI
        
        frame = int(current_time * self.sr)
        frame_end = frame + 1024
        chunk = self.audio[frame:frame_end]
        
        if len(chunk) < 1024:
            return 0
        
        # Calculate frequency energy
        fft = np.fft.fft(chunk)
        magnitudes = np.abs(fft)
        return {
            band: np.mean(magnitudes[low:high])
            for band, (low, high) in FREQ_BANDS.items()
        }

    def start_visualization(self):
        self.is_playing = True
        self.start_time = time.time()
        
        # Start audio playback thread
        if not self.audio_path.endswith('.mid'):
            audio_thread = threading.Thread(target=self._play_audio)
            audio_thread.start()
        
        # Start visualization loop
        while self.is_playing:
            elapsed = time.time() - self.start_time
            self._update_visuals(elapsed)
            time.sleep(0.001)

    def _play_audio(self):
        audio = AudioSegment.from_file(self.audio_path)
        play(audio)

    def _update_visuals(self, elapsed_time):
        # Check for beat hits
        if self.current_beat < len(self.beat_times):
            next_beat = self.beat_times[self.current_beat]
            if elapsed_time >= next_beat:
                self._trigger_beat_animation()
                self.current_beat += 1

        # Update frequency-based elements
        energy = self._get_energy(elapsed_time)
        self._update_frequency_elements(energy)

        # Send updates to client
        socketio.emit('svg_update', {
            'elements': self._get_svg_state(),
            'beat': self.current_beat,
            'energy': energy
        })

    def _trigger_beat_animation(self):
        # Scale elements on beat
        if self.elements['circle']:
            new_radius = np.random.uniform(10, 50)
            self.elements['circle'].radius = new_radius

    def _update_frequency_elements(self, energy):
        # Update rectangle height based on bass energy
        if self.elements['rect']:
            bass_energy = energy.get('bass', 0)
            new_height = 50 + bass_energy * 100
            self.elements['rect'].height = new_height

    def _get_svg_state(self):
        return {
            'circle': {
                'radius': self.elements['circle'].radius if self.elements['circle'] else None
            },
            'rect': {
                'height': self.elements['rect'].height if self.elements['rect'] else None
            }
        }

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@socketio.on('connect')
def handle_connect():
    visualizer = AudioVisualizer('input.mp3', 'visualization.svg')
    threading.Thread(target=visualizer.start_visualization).start()

if __name__ == '__main__':
    socketio.run(app, port=5000)
