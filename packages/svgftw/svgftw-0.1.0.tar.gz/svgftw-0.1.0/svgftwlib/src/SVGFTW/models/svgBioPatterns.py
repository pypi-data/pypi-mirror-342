"""
Bio-inspired pattern generation and visualization for SVG elements.
Enhanced with neural-evolved patterns and advanced biological simulations.
"""

from typing import Dict, Any, List, Tuple, Optional, Union
import numpy as np
from dataclasses import dataclass
from ..utils.feature_loader import FeatureRegistry, requires_feature

@dataclass
class MyceliumParams:
    """Parameters for mycelium growth simulation."""
    branching_prob: float = 0.3
    branch_angle_var: float = 0.5
    growth_speed: float = 1.0
    max_branches: int = 1000
    nutrient_sensitivity: float = 0.5
    obstacle_avoidance: float = 1.0
    chemical_gradients: Dict[str, np.ndarray] = None
    oxygen_level: float = 1.0
    moisture_level: float = 0.7
    temperature: float = 298.0  # Kelvin
    ph_level: float = 7.0
    dna_guidance: bool = False  # Use DNA patterns for growth
    gene_expression: Dict[str, float] = None  # Gene expression levels

@dataclass
class BioSimParams:
    """Parameters for biological system simulation."""
    temperature: float = 310.0  # Kelvin
    ph: float = 7.4
    ion_concentrations: Dict[str, float] = None
    enzyme_levels: Dict[str, float] = None
    metabolic_rate: float = 1.0
    atp_availability: float = 1.0
    membrane_potential: float = -70.0  # Membrane potential in mV
    dna_repair_rate: float = 1.0  # DNA repair efficiency
    telomere_length: int = 1000  # Telomere length in base pairs

@dataclass
class DNAVisualizationParams:
    """Parameters for DNA sequence visualization."""
    helix_radius: float = 20.0
    base_spacing: float = 5.0
    turns_per_segment: float = 0.5
    highlight_mutations: bool = True
    animate_transcription: bool = False
    show_base_pairs: bool = True
    chromatin_packing: bool = False  # Show chromatin structure
    methylation_sites: List[int] = None  # DNA methylation positions
    genome_coordinates: Tuple[int, int] = None  # Genomic region to visualize

@dataclass
class ChromatinPatternParams:
    """Parameters for chromatin pattern visualization."""
    nucleosome_spacing: float = 10.0  # Spacing between nucleosomes
    compaction_level: float = 1.0  # Chromatin compaction (1-30)
    histone_modifications: Dict[str, List[int]] = None  # Histone marks
    tad_boundaries: List[int] = None  # Topological domain boundaries
    loop_formations: List[Tuple[int, int]] = None  # Chromatin loops
    regulatory_regions: Dict[str, List[int]] = None  # Enhancers/promoters

@dataclass
class CellularPatternParams:
    """Parameters for cellular pattern generation."""
    cell_types: List[str] = None  # Different cell types to include
    signaling_molecules: Dict[str, float] = None  # Morphogen concentrations
    adhesion_strength: float = 1.0  # Cell-cell adhesion
    division_rate: float = 0.1  # Cell division probability
    migration_speed: float = 0.5  # Cell migration rate
    ecm_density: float = 1.0  # Extracellular matrix density
    tissue_polarity: Optional[Tuple[float, float]] = None  # Tissue axis
    mechanical_constraints: Dict[str, float] = None  # Physical constraints

@FeatureRegistry.register('bio-basic', ['numpy', 'scipy'])
class BioPatternEngine:
    """Generate bio-inspired patterns for SVG elements."""
    
    def __init__(self):
        """Initialize bio-pattern generation system."""
        self.rng = np.random.default_rng()
        self.pattern_net = None

    def generate_bio_pattern(
        self,
        pattern_type: str,
        bounds: Tuple[float, float, float, float],
        bio_params: Optional[BioSimParams] = None,
        cellular_params: Optional[CellularPatternParams] = None,
        chromatin_params: Optional[ChromatinPatternParams] = None,
        dna_params: Optional[DNAVisualizationParams] = None
    ) -> Dict[str, Any]:
        """Generate biological pattern based on specified type."""
        if pattern_type == "mycelium":
            return self.generate_mycelium_network(
                bounds,
                MyceliumParams(dna_guidance=True),
                bio_params=bio_params
            )
        elif pattern_type == "chromatin":
            return self.generate_chromatin_structure(
                bounds,
                chromatin_params or ChromatinPatternParams()
            )
        elif pattern_type == "cellular":
            return self.generate_cellular_pattern(
                bounds,
                cellular_params or CellularPatternParams()
            )
        else:
            raise ValueError(f"Unknown pattern type: {pattern_type}")
            
    def generate_mycelium_network(
        self,
        bounds: Tuple[float, float, float, float],
        params: Optional[MyceliumParams] = None,
        nutrients: Optional[np.ndarray] = None,
        bio_params: Optional[BioSimParams] = None
    ) -> Dict[str, Any]:
        """Create organic branching patterns using fungal growth algorithms."""
        if params is None:
            params = MyceliumParams()
        if bio_params is None:
            bio_params = BioSimParams()

        # Initialize growth points
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        
        roots = [{
            'x': bounds[0] + width/2,
            'y': bounds[3],  # Start from bottom
            'angle': -np.pi/2,  # Grow upward
            'generation': 0,
            'metabolic_state': self._initialize_metabolic_state(bio_params)
        }]
        
        branches = [root]
        paths = []
        branch_count = 0
        
        while branches and branch_count < params.max_branches:
            branch = branches.pop(0)
            
            # Generate branch segment
            new_branches = self._grow_branch(
                branch,
                bounds,
                params,
                nutrients
            )
            
            paths.extend(new_branches['paths'])
            branches.extend(new_branches['branches'])
            branch_count += len(new_branches['branches'])
            
        # Combine all path segments
        path_data = self._combine_paths(paths)
        
        return {
            'type': 'path',
            'd': path_data,
            'style': (
                'fill:none;stroke:#2a6;'
                'stroke-width:1.5;stroke-linecap:round'
            )
        }

    def dna_sequence_visualizer(
        self,
        sequence: str,
        params: Optional[DNAVisualizationParams] = None
    ) -> List[Dict[str, Any]]:
        """Create animated DNA sequence visualization."""
        if params is None:
            params = DNAVisualizationParams()
            
        elements = []
        
        # Generate double helix backbone
        helix_paths = self._generate_helix(
            len(sequence),
            params
        )
        
        elements.extend(helix_paths)
        
        if params.show_base_pairs:
            # Add base pair connections
            base_pairs = self._generate_base_pairs(
                sequence,
                params
            )
            elements.extend(base_pairs)
            
        if params.animate_transcription:
            # Add transcription animation
            animation = self._create_transcription_animation(
                sequence,
                params
            )
            elements.extend(animation)
            
        return elements

    # Helper methods remain the same as in original file
    def _grow_branch(self, branch, bounds, params, nutrients=None):
        """Grow a single branch segment with possible subdivisions."""
        new_branches = []
        paths = []
        
        # Base growth direction
        angle = branch['angle']
        
        # Adjust for nutrients if available
        if nutrients is not None:
            gradient = self._nutrient_gradient(
                branch['x'],
                branch['y'],
                nutrients
            )
            angle += params.nutrient_sensitivity * gradient
            
        # Add some randomness
        angle += self.rng.normal(0, 0.1)
        
        # Calculate growth length based on generation
        length = 20 * (0.8 ** branch['generation'])
        
        # New endpoint
        end_x = branch['x'] + length * np.cos(angle)
        end_y = branch['y'] + length * np.sin(angle)
        
        # Check bounds
        if self._is_valid_point(end_x, end_y, bounds):
            # Create path segment
            path = (
                f"M {branch['x']:.2f} {branch['y']:.2f} "
                f"L {end_x:.2f} {end_y:.2f}"
            )
            paths.append(path)
            
            # Possible branching
            if (self.rng.random() < params.branching_prob and
                branch['generation'] < 8):
                
                # Create two branches
                angle_var = params.branch_angle_var * np.pi
                
                for branch_angle in [
                    angle + angle_var,
                    angle - angle_var
                ]:
                    new_branches.append({
                        'x': end_x,
                        'y': end_y,
                        'angle': branch_angle,
                        'generation': branch['generation'] + 1
                    })
                    
            # Continue current branch
            new_branches.append({
                'x': end_x,
                'y': end_y,
                'angle': angle,
                'generation': branch['generation']
            })
            
        return {
            'paths': paths,
            'branches': new_branches
        }

    def _is_valid_point(self, x, y, bounds):
        """Check if point is within bounds."""
        return (bounds[0] <= x <= bounds[2] and
                bounds[1] <= y <= bounds[3])

    def _nutrient_gradient(self, x, y, nutrients):
        """Calculate nutrient gradient at point."""
        height, width = nutrients.shape
        
        # Convert coordinates to nutrient array indices
        i = int(y * height)
        j = int(x * width)
        
        # Calculate gradient using central difference
        if 0 < i < height-1 and 0 < j < width-1:
            dx = nutrients[i, j+1] - nutrients[i, j-1]
            dy = nutrients[i+1, j] - nutrients[i-1, j]
            return np.arctan2(dy, dx)
        return 0

    def _initialize_metabolic_state(self, bio_params):
        """Initialize metabolic state for a growth point."""
        state = {
            'atp': bio_params.atp_availability,
            'metabolic_rate': bio_params.metabolic_rate,
            'enzyme_activity': 1.0
        }
        
        if bio_params.enzyme_levels:
            state['enzyme_levels'] = bio_params.enzyme_levels.copy()
            
        if bio_params.ion_concentrations:
            state['ion_concentrations'] = bio_params.ion_concentrations.copy()
            
        return state

    def generate_chromatin_structure(
        self,
        bounds: Tuple[float, float, float, float],
        params: ChromatinPatternParams
    ) -> Dict[str, Any]:
        """
        Generate chromatin fiber structure visualization.
        
        Args:
            bounds: Drawing boundaries
            params: Chromatin pattern parameters
            
        Returns:
            SVG path element for chromatin structure
        """
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        center_x = bounds[0] + width/2
        center_y = bounds[1] + height/2
        
        # Generate nucleosome positions
        nucleosomes = []
        x = center_x
        y = center_y
        
        # Calculate number of nucleosomes based on compaction
        num_nucleosomes = int(width / (params.nucleosome_spacing * params.compaction_level))
        
        for i in range(num_nucleosomes):
            # Add some natural variation
            angle = 2 * np.pi * i / num_nucleosomes
            radius = params.nucleosome_spacing * params.compaction_level
            
            # Apply chromatin loops if defined
            if params.loop_formations:
                for loop_start, loop_end in params.loop_formations:
                    if loop_start <= i <= loop_end:
                        radius *= 1.5  # Expand radius for loops
                        
            # Position nucleosome
            nx = x + radius * np.cos(angle)
            ny = y + radius * np.sin(angle)
            
            nucleosomes.append((nx, ny))
            
            # Add histone modifications if specified
            if params.histone_modifications:
                for mod_type, positions in params.histone_modifications.items():
                    if i in positions:
                        self._add_histone_mark(nx, ny, mod_type)
                        
        # Generate chromatin fiber path
        path_commands = []
        for i, (nx, ny) in enumerate(nucleosomes):
            if i == 0:
                path_commands.append(f"M {nx:.2f} {ny:.2f}")
            else:
                # Create curved connections between nucleosomes
                prev_x, prev_y = nucleosomes[i-1]
                ctrl_x = (prev_x + nx) / 2
                ctrl_y = (prev_y + ny) / 2
                path_commands.append(
                    f"Q {ctrl_x:.2f} {ctrl_y:.2f} {nx:.2f} {ny:.2f}"
                )
                
        return {
            'type': 'path',
            'd': ' '.join(path_commands),
            'style': (
                'fill:none;stroke:#4a90e2;stroke-width:2;'
                'stroke-linecap:round;filter:url(#shadow)'
            )
        }
        
    def generate_cellular_pattern(
        self,
        bounds: Tuple[float, float, float, float],
        params: CellularPatternParams
    ) -> Dict[str, Any]:
        """
        Generate cellular tissue pattern.
        
        Args:
            bounds: Drawing boundaries
            params: Cellular pattern parameters
            
        Returns:
            SVG path element for cellular pattern
        """
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        
        # Initialize cell positions using Voronoi seeds
        num_cells = int(width * height / 1000)  # Adjust cell density
        cells = []
        
        for _ in range(num_cells):
            x = bounds[0] + self.rng.random() * width
            y = bounds[1] + self.rng.random() * height
            
            # Assign cell type if specified
            cell_type = None
            if params.cell_types:
                cell_type = self.rng.choice(params.cell_types)
                
            cells.append({
                'x': x,
                'y': y,
                'type': cell_type,
                'size': 10 + self.rng.normal(0, 2)  # Variable cell size
            })
            
        # Apply cell-cell interactions
        for _ in range(10):  # Simulation steps
            self._simulate_cell_interactions(cells, params)
            
        # Generate cell boundary paths
        path_commands = []
        for cell in cells:
            # Create rounded cell shape
            angles = np.linspace(0, 2*np.pi, 8)
            vertices = []
            
            for angle in angles:
                # Add membrane fluctuations
                radius = cell['size'] * (1 + 0.1 * self.rng.normal())
                vx = cell['x'] + radius * np.cos(angle)
                vy = cell['y'] + radius * np.sin(angle)
                vertices.append((vx, vy))
                
            # Create cell path
            path_commands.append(f"M {vertices[0][0]:.2f} {vertices[0][1]:.2f}")
            
            for i in range(1, len(vertices)):
                prev = vertices[i-1]
                curr = vertices[i]
                ctrl = (
                    (prev[0] + curr[0])/2 + self.rng.normal(0, 1),
                    (prev[1] + curr[1])/2 + self.rng.normal(0, 1)
                )
                path_commands.append(
                    f"Q {ctrl[0]:.2f} {ctrl[1]:.2f} {curr[0]:.2f} {curr[1]:.2f}"
                )
                
            # Close cell path
            path_commands.append("Z")
            
        return {
            'type': 'path',
            'd': ' '.join(path_commands),
            'style': 'fill:#f0f0f0;stroke:#666;stroke-width:1'
        }
        
    def _simulate_cell_interactions(
        self,
        cells: List[Dict[str, Any]],
        params: CellularPatternParams
    ) -> None:
        """Simulate physical interactions between cells."""
        for i, cell1 in enumerate(cells):
            dx = dy = 0
            
            # Calculate forces from neighboring cells
            for j, cell2 in enumerate(cells):
                if i != j:
                    # Distance between cells
                    rx = cell2['x'] - cell1['x']
                    ry = cell2['y'] - cell1['y']
                    dist = np.sqrt(rx*rx + ry*ry)
                    
                    if dist < (cell1['size'] + cell2['size']):
                        # Repulsion force
                        force = params.adhesion_strength * (
                            1 - dist/(cell1['size'] + cell2['size'])
                        )
                        dx -= force * rx/dist
                        dy -= force * ry/dist
                        
            # Apply tissue polarity if specified
            if params.tissue_polarity:
                polx, poly = params.tissue_polarity
                dx += polx * params.migration_speed
                dy += poly * params.migration_speed
                
            # Update cell position
            cell1['x'] += dx * params.migration_speed
            cell1['y'] += dy * params.migration_speed

    def _add_histone_mark(
        self,
        x: float,
        y: float,
        mark_type: str
    ) -> Dict[str, Any]:
        """
        Add histone modification marker at specified position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            mark_type: Type of histone modification
            
        Returns:
            SVG element for histone mark
        """
        # Define mark styles for different modifications
        mark_styles = {
            'H3K4me3': {
                'color': '#4CAF50',  # Active mark - green
                'shape': 'circle',
                'size': 4
            },
            'H3K27me3': {
                'color': '#F44336',  # Repressive mark - red
                'shape': 'square',
                'size': 4
            },
            'H3K27ac': {
                'color': '#2196F3',  # Active enhancer - blue
                'shape': 'triangle',
                'size': 5
            },
            'H3K9me3': {
                'color': '#9C27B0',  # Heterochromatin - purple
                'shape': 'diamond',
                'size': 4
            }
        }
        
        style = mark_styles.get(mark_type, {
            'color': '#757575',  # Default gray
            'shape': 'circle',
            'size': 3
        })
        
        # Generate mark path based on shape
        path_data = ''
        if style['shape'] == 'circle':
            path_data = (
                f"M {x} {y} m -{style['size']},0 "
                f"a {style['size']},{style['size']} 0 1,0 "
                f"{style['size']*2},0 "
                f"a {style['size']},{style['size']} 0 1,0 "
                f"-{style['size']*2},0"
            )
        elif style['shape'] == 'square':
            s = style['size']
            path_data = (
                f"M {x-s} {y-s} h {s*2} v {s*2} "
                f"h -{s*2} Z"
            )
        elif style['shape'] == 'triangle':
            s = style['size']
            path_data = (
                f"M {x} {y-s} l {s} {s*1.732} "
                f"h -{s*2} Z"
            )
        elif style['shape'] == 'diamond':
            s = style['size']
            path_data = (
                f"M {x} {y-s} l {s} {s} l -{s} {s} "
                f"l -{s} -{s} Z"
            )
            
        return {
            'type': 'path',
            'd': path_data,
            'style': f"fill:{style['color']};stroke:none"
        }

    def _combine_paths(self, paths):
        """Combine multiple path strings."""
        return ' '.join(paths)

@FeatureRegistry.register('bio-neural', ['torch'])
class NeuralBioPattern(BioPatternEngine):
    """Neural network enhanced bio-pattern generation."""
    
    def __init__(self):
        super().__init__()
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        from torch.optim import Adam
        
        self.torch = torch
        self.nn = nn
        self.F = F
        self.Adam = Adam
        self._initialize_neural_components()
    
    def _initialize_neural_components(self):
        """Initialize neural networks for pattern evolution."""
        class PatternEvolutionNet(self.nn.Module):
            def __init__(self, input_size, hidden_size=64):
                super().__init__()
                self.lstm = self.nn.LSTM(input_size, hidden_size, 2, batch_first=True)
                self.growth_mlp = self.nn.Sequential(
                    self.nn.Linear(hidden_size, hidden_size),
                    self.nn.ReLU(),
                    self.nn.Linear(hidden_size, 4)
                )
                self.pattern_mlp = self.nn.Sequential(
                    self.nn.Linear(hidden_size, hidden_size),
                    self.nn.ReLU(),
                    self.nn.Linear(hidden_size, 2)
                )
                
        self.pattern_net = PatternEvolutionNet(
            input_size=8  # Environmental inputs
        ).to('cuda' if self.torch.cuda.is_available() else 'cpu')
        self.optimizer = self.Adam(self.pattern_net.parameters())

    def _evolve_pattern(self, environment, steps=100):
        """Evolve pattern based on environmental conditions."""
        device = next(self.pattern_net.parameters()).device
        env_tensor = self.torch.FloatTensor(environment).to(device)
        
        # Initialize pattern sequence
        sequence = []
        hidden = None
        
        # Generate pattern through time
        for _ in range(steps):
            env_step = env_tensor.unsqueeze(0).unsqueeze(0)
            lstm_out, hidden = self.pattern_net.lstm(env_step, hidden)
            
            # Generate growth parameters
            growth = self.pattern_net.growth_mlp(lstm_out.squeeze(0))
            coords = self.pattern_net.pattern_mlp(lstm_out.squeeze(0))
            
            sequence.append(self.torch.cat([growth, coords], dim=-1))
            
        return self.torch.stack(sequence).cpu().numpy()

def sigmoid(x: float) -> float:
    """Compute sigmoid function."""
    return 1 / (1 + np.exp(-x))
