import math
from dataclasses import dataclass
from typing import List, Dict

# Music Theory Data Structures
NOTE_FREQUENCIES = {'C': 261.63, 'D': 293.66, 'E': 329.63, 'F': 349.23,
                    'G': 392.00, 'A': 440.00, 'B': 493.88, 'C2': 523.25}

SCALES = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 10],
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
    'phrygian_dominant': [0, 1, 4, 5, 7, 8, 10]
}

CHORD_PROGRESSIONS = {
    'metal': ['i', 'III', 'iv', 'VII'],
    'punk': ['I', 'IV', 'V'],
    'jazz': ['ii', 'V', 'I']
}

@dataclass
class MusicalInput:
    key: str
    scale_type: str
    progression: str
    bpm: int
    time_signature: str

class VisualRiffGenerator:
    def __init__(self, musical_input: MusicalInput, canvas_size=(800, 600)):
        self.music = musical_input
        self.canvas_width, self.canvas_height = canvas_size
        self.elements = []
        
        # Audio-visual mapping parameters
        self.hue_range = 360
        self.shape_sizes = (10, 50)
        self.rhythm_pattern = []
        
    def _calculate_colors(self):
        """Generate color palette based on musical scale"""
        scale_notes = self._get_scale_notes()
        hue_step = self.hue_range // len(scale_notes)
        return [f'hsl({i*hue_step}, 70%, 50%)' for i in range(len(scale_notes))]
    
    def _get_scale_notes(self):
        base_note = self.music.key
        scale_pattern = SCALES[self.music.scale_type]
        return [NOTE_FREQUENCIES.get(base_note, 440) * (2 ** (s/12)) 
                for s in scale_pattern]
    
    def _generate_rhythm_map(self):
        """Convert BPM and time signature to visual spacing"""
        beats, beat_unit = map(int, self.music.time_signature.split('/'))
        beat_duration = 60 / self.music.bpm
        return [beat_duration * (i % beats) for i in range(beats * 4)]
    
    def _chord_to_shape(self, chord: str, position: tuple):
        """Generate geometric shape based on chord type"""
        chord_types = {
            'I': 'circle', 'i': 'circle',
            'IV': 'rect', 'iv': 'rect',
            'V': 'polygon', 'v': 'polygon',
            'VII': 'path', 'vii': 'path'
        }
        shape_type = chord_types.get(chord, 'rect')
        
        if shape_type == 'circle':
            return f'<circle cx="{position[0]}" cy="{position[1]}" r="20"/>'
        elif shape_type == 'rect':
            return f'<rect x="{position[0]}" y="{position[1]}" width="40" height="40"/>'
        elif shape_type == 'polygon':
            points = " ".join([f"{position[0]+math.cos(math.radians(60*i))*20}," 
                              f"{position[1]+math.sin(math.radians(60*i))*20}" 
                              for i in range(6)])
            return f'<polygon points="{points}"/>'
        elif shape_type == 'path':
            return f'''<path d="M {position[0]} {position[1]}
                      Q {position[0]+30} {position[1]-40},
                      {position[0]+60} {position[1]}"/>'''
    
    def generate_svg(self):
        """Main generation method combining musical parameters"""
        colors = self._calculate_colors()
        rhythm = self._generate_rhythm_map()
        progression = CHORD_PROGRESSIONS[self.music.progression]
        
        svg_header = f'''<svg xmlns="http://www.w3.org/2000/svg" 
                           viewBox="0 0 {self.canvas_width} {self.canvas_height}">'''
        
        # Generate visual elements based on musical parameters
        x_step = self.canvas_width // len(progression)
        for i, chord in enumerate(progression):
            y = self.canvas_height // 2 + math.sin(i) * 50
            self.elements.append(
                self._chord_to_shape(chord, (i*x_step + 50, y))
            )
            
        # Add rhythm markers
        rhythm_step = self.canvas_width // len(rhythm)
        for j, beat in enumerate(rhythm):
            self.elements.append(
                f'<rect x="{j*rhythm_step}" y="500" width="5" height="{beat*100}" fill="{colors[j%len(colors)]}"/>'
            )
        
        svg_content = "\n".join(self.elements)
        return f"{svg_header}\n{svg_content}\n</svg>"

# Example Usage
metal_riff = MusicalInput(
    key='E',
    scale_type='phrygian_dominant',
    progression='metal',
    bpm=160,
    time_signature='4/4'
)

generator = VisualRiffGenerator(metal_riff)
svg_output = generator.generate_svg()

# Save to file
with open('metal_riff.svg', 'w') as f:
    f.write(svg_output)
