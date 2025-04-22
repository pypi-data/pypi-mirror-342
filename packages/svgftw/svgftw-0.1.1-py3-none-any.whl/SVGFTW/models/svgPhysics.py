"""
SVG physics simulation features including fluid dynamics and soft body deformation.
Enhanced with CUDA acceleration and optimized collision detection.
"""

from typing import Dict, Any, List, Tuple, Optional, Union
import numpy as np
import re
from ..utils.feature_loader import FeatureRegistry, requires_feature

try:
    import numba
    from numba import cuda
    CUDA_AVAILABLE = True
except ImportError:
    CUDA_AVAILABLE = False

@FeatureRegistry.register('physics-fluid', ['numpy', 'numba'])
@cuda.jit
def _fluid_kernel(
    positions: np.ndarray,
    velocities: np.ndarray,
    forces: np.ndarray,
    boundaries: np.ndarray,
    dt: float
):
    """CUDA kernel for fluid particle simulation."""
    thread_id = cuda.grid(1)
    
    if thread_id >= positions.shape[0]:
        return
        
    # Update particle position based on velocity
    positions[thread_id, 0] += velocities[thread_id, 0] * dt
    positions[thread_id, 1] += velocities[thread_id, 1] * dt
    
    # Apply forces
    velocities[thread_id, 0] += forces[thread_id, 0] * dt
    velocities[thread_id, 1] += forces[thread_id, 1] * dt
      # Boundary collision handling
    for i in range(boundaries.shape[0]):
        # Simple bounce-off behavior
        if (positions[thread_id, 0] < boundaries[i, 0] or
            positions[thread_id, 0] > boundaries[i, 2]):
            velocities[thread_id, 0] *= -0.8  # Damping factor
            
        if (positions[thread_id, 1] < boundaries[i, 1] or
            positions[thread_id, 1] > boundaries[i, 3]):
            velocities[thread_id, 1] *= -0.8  # Damping factor

def _fluid_update_cpu(
    positions: np.ndarray,
    velocities: np.ndarray,
    forces: np.ndarray,
    boundaries: np.ndarray,
    dt: float
) -> Tuple[np.ndarray, np.ndarray]:
    """CPU implementation of fluid simulation for systems without CUDA."""
    # Update positions based on velocity
    positions += velocities * dt[:, np.newaxis]
    
    # Apply forces
    velocities += forces * dt[:, np.newaxis]
    
    # Boundary collision handling
    for i in range(boundaries.shape[0]):
        x_min, y_min, x_max, y_max = boundaries[i]
        
        # X boundary collisions
        x_collisions = (positions[:, 0] < x_min) | (positions[:, 0] > x_max)
        velocities[x_collisions, 0] *= -0.8  # Damping factor
        
        # Y boundary collisions
        y_collisions = (positions[:, 1] < y_min) | (positions[:, 1] > y_max)
        velocities[y_collisions, 1] *= -0.8  # Damping factor
    
    return positions, velocities

class FluidSimulation:
    """Handle fluid dynamics simulation for SVG elements."""
    """Handle fluid dynamics simulation for SVG elements."""
    
    def __init__(self):
        """Initialize fluid simulation system."""
        self.cuda_enabled = False
        self.num_particles = 1000
        self.particles = None
        self.try_enable_cuda()
        
    def try_enable_cuda(self) -> bool:
        """Try to enable CUDA acceleration if available."""
        if CUDA_AVAILABLE:
            self.cuda_enabled = True
            return True
        return False
        
    def _check_requirements(self) -> None:
        """Verify CUDA requirements are met."""
        if not CUDA_AVAILABLE and self.cuda_enabled:
            raise ImportError(
                "Fluid simulation with CUDA requires numba. "
                "Install with: pip install numba"
            )
            
    def init_particles(
        self, 
        bounds: Tuple[float, float, float, float]
    ) -> None:
        """
        Initialize fluid particles within boundaries.
        
        Args:
            bounds: (x_min, y_min, x_max, y_max) of fluid container
        """
        self.particles = {
            'positions': np.random.uniform(
                low=[bounds[0], bounds[1]],
                high=[bounds[2], bounds[3]],
                size=(self.num_particles, 2)
            ).astype(np.float32),
            'velocities': np.zeros(
                (self.num_particles, 2),
                dtype=np.float32
            ),
            'forces': np.zeros(
                (self.num_particles, 2),
                dtype=np.float32
            )
        }
        
    def update(
        self,
        dt: float,
        boundaries: List[Tuple[float, float, float, float]]
    ) -> np.ndarray:
        """
        Update fluid simulation state.
        
        Args:
            dt: Time step
            boundaries: List of (x_min, y_min, x_max, y_max) boundaries
            
        Returns:
            Updated particle positions
        """
        if self.particles is None:
            raise RuntimeError("Must call init_particles first")
            
        # Convert boundaries to numpy array
        boundaries_array = np.array(boundaries, dtype=np.float32)
        
        if self.cuda_enabled:
            return self._update_cuda(dt, boundaries_array)
        else:
            return self._update_cpu(dt, boundaries_array)
    
    def _update_cuda(self, dt: float, boundaries_array: np.ndarray) -> np.ndarray:
        """Update simulation using CUDA acceleration."""
        if not CUDA_AVAILABLE:
            raise ImportError("CUDA is not available but CUDA mode is enabled")
            
        # Prepare CUDA arrays
        d_positions = cuda.to_device(self.particles['positions'])
        d_velocities = cuda.to_device(self.particles['velocities'])
        d_forces = cuda.to_device(self.particles['forces'])
        d_boundaries = cuda.to_device(boundaries_array)
        
        # Configure CUDA grid
        threads_per_block = 256
        blocks = (self.num_particles + threads_per_block - 1) 
        blocks = blocks // threads_per_block
        
        # Run simulation kernel
        _fluid_kernel[blocks, threads_per_block](
            d_positions,
            d_velocities,
            d_forces,
            d_boundaries,
            dt
        )
        
        # Update particle state
        self.particles['positions'] = d_positions.copy_to_host()
        self.particles['velocities'] = d_velocities.copy_to_host()
        
        return self.particles['positions']
        
    def _update_cpu(self, dt: float, boundaries_array: np.ndarray) -> np.ndarray:
        """Update simulation using CPU implementation."""
        # Create a dt array for vectorized operations
        dt_array = np.full(self.num_particles, dt, dtype=np.float32)
        
        # Update positions and velocities
        positions, velocities = _fluid_update_cpu(
            self.particles['positions'],
            self.particles['velocities'],
            self.particles['forces'],
            boundaries_array,
            dt_array
        )
        
        # Update particle state
        self.particles['positions'] = positions
        self.particles['velocities'] = velocities
        
        return self.particles['positions']
        
    def apply_force(self, force_vector: Tuple[float, float], 
                   position: Optional[Tuple[float, float]] = None,
                   radius: float = 50.0) -> None:
        """
        Apply force to fluid particles.
        
        Args:
            force_vector: (force_x, force_y) to apply
            position: Optional center point of force application
            radius: Radius of effect if position is provided
        """
        if self.particles is None:
            raise RuntimeError("Must call init_particles first")
            
        if position is None:
            # Apply to all particles
            self.particles['forces'][:, 0] += force_vector[0]
            self.particles['forces'][:, 1] += force_vector[1]
        else:
            # Apply to particles within radius
            positions = self.particles['positions']
            dx = positions[:, 0] - position[0]
            dy = positions[:, 1] - position[1]
            distances = np.sqrt(dx**2 + dy**2)
            
            # Create a mask for particles within radius
            mask = distances < radius
            
            # Calculate force falloff based on distance
            falloff = 1 - (distances[mask] / radius)
            
            # Apply forces with falloff
            self.particles['forces'][mask, 0] += force_vector[0] * falloff
            self.particles['forces'][mask, 1] += force_vector[1] * falloff

def _deform_update_cpu(
    vertices: np.ndarray,
    rest_positions: np.ndarray,
    forces: np.ndarray,
    stiffness: float,
    damping: float,
    dt: float
) -> Tuple[np.ndarray, np.ndarray]:
    """CPU implementation of soft body deformation for systems without CUDA."""
    # Calculate spring force to rest position
    dx = vertices[:, 0] - rest_positions[:, 0]
    dy = vertices[:, 1] - rest_positions[:, 1]
    
    # Apply Hooke's law
    force_x = -stiffness * dx
    force_y = -stiffness * dy
    
    # Add damping
    force_x -= damping * forces[:, 0]
    force_y -= damping * forces[:, 1]
    
    # Update forces
    forces[:, 0] = force_x
    forces[:, 1] = force_y
    
    # Update positions
    vertices[:, 0] += forces[:, 0] * dt
    vertices[:, 1] += forces[:, 1] * dt
    
    return vertices, forces

@cuda.jit
def _deform_kernel(
    vertices: np.ndarray,
    rest_positions: np.ndarray,
    forces: np.ndarray,
    stiffness: float,
    damping: float,
    dt: float
):
    """CUDA kernel for soft body deformation."""
    thread_id = cuda.grid(1)
    
    if thread_id >= vertices.shape[0]:
        return
        
    # Calculate spring force to rest position
    dx = vertices[thread_id, 0] - rest_positions[thread_id, 0]
    dy = vertices[thread_id, 1] - rest_positions[thread_id, 1]
    
    # Apply Hooke's law
    force_x = -stiffness * dx
    force_y = -stiffness * dy
    
    # Add damping
    force_x -= damping * forces[thread_id, 0]
    force_y -= damping * forces[thread_id, 1]
    
    # Update forces
    forces[thread_id, 0] = force_x
    forces[thread_id, 1] = force_y
    
    # Update positions
    vertices[thread_id, 0] += forces[thread_id, 0] * dt
    vertices[thread_id, 1] += forces[thread_id, 1] * dt

@FeatureRegistry.register('physics-soft', ['numpy'])
class SoftBodyDeformation:
    """Handle soft body physics for SVG elements."""
    
    def __init__(self):
        """Initialize soft body deformation system."""
        self.cuda_enabled = False
        self.stiffness = 1.0
        self.damping = 0.5
        self.try_enable_cuda()
    
    def try_enable_cuda(self) -> bool:
        """Try to enable CUDA acceleration if available."""
        if CUDA_AVAILABLE:
            self.cuda_enabled = True
            return True
        return False
        
    def _check_requirements(self) -> None:
        """Verify CUDA requirements are met."""
        if not CUDA_AVAILABLE and self.cuda_enabled:
            raise ImportError(
                "Soft body deformation with CUDA requires numba. "
                "Install with: pip install numba"
            )
            
    def deform_path(
        self,
        path_data: str,
        force_field: Optional[np.ndarray] = None,
        dt: float = 0.016
    ) -> str:
        """
        Apply soft body deformation to SVG path.
        
        Args:
            path_data: Original SVG path data
            force_field: External forces to apply
            dt: Time step
            
        Returns:
            Deformed path data
        """
        # Parse path into vertices
        vertices, commands = self._path_to_vertices(path_data)
        rest_positions = vertices.copy()
        
        # Initialize forces
        forces = np.zeros_like(vertices)
        if force_field is not None:
            forces += force_field
            
        if self.cuda_enabled:
            deformed = self._deform_cuda(vertices, rest_positions, forces, dt)
        else:
            deformed = self._deform_cpu(vertices, rest_positions, forces, dt)
        
        # Convert back to path data
        return self._vertices_to_path(deformed, commands)
    
    def _deform_cuda(
        self, 
        vertices: np.ndarray, 
        rest_positions: np.ndarray, 
        forces: np.ndarray, 
        dt: float
    ) -> np.ndarray:
        """Apply deformation using CUDA acceleration."""
        if not CUDA_AVAILABLE:
            raise ImportError("CUDA is not available but CUDA mode is enabled")
            
        # Prepare CUDA arrays
        d_vertices = cuda.to_device(vertices)
        d_rest = cuda.to_device(rest_positions)
        d_forces = cuda.to_device(forces)
        
        # Configure CUDA grid
        threads_per_block = 256
        blocks = (vertices.shape[0] + threads_per_block - 1)
        blocks = blocks // threads_per_block
        
        # Run deformation kernel
        _deform_kernel[blocks, threads_per_block](
            d_vertices,
            d_rest,
            d_forces,
            self.stiffness,
            self.damping,
            dt
        )
        
        # Get deformed vertices
        return d_vertices.copy_to_host()
        
    def _deform_cpu(
        self, 
        vertices: np.ndarray, 
        rest_positions: np.ndarray, 
        forces: np.ndarray, 
        dt: float
    ) -> np.ndarray:
        """Apply deformation using CPU implementation."""
        vertices, _ = _deform_update_cpu(
            vertices,
            rest_positions,
            forces,
            self.stiffness,
            self.damping,
            dt
        )
        return vertices
        
    def _path_to_vertices(self, path_data: str) -> Tuple[np.ndarray, List[str]]:
        """
        Convert SVG path data to vertex array.
        
        Returns:
            Tuple of (vertices, commands)
        """
        # Regular expression to parse path commands and coordinates
        # Captures command letters and numbers (including decimals)
        pattern = r'([MLHVCSQTAZmlhvcsqtaz])|([-+]?[0-9]*\.?[0-9]+)'
        tokens = re.findall(pattern, path_data)
        
        vertices = []
        commands = []
        current_cmd = None
        current_point = [0.0, 0.0]  # Current position
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # If token is a command letter
            if token[0] and not token[1]:
                current_cmd = token[0]
                commands.append(current_cmd)
                i += 1
                continue
                
            # Otherwise it's a coordinate
            if current_cmd in 'MLT':
                # Absolute move/line/smooth quad to - needs 2 coordinates
                if i + 1 < len(tokens) and tokens[i+1][1]:  # Make sure next token is a number
                    x = float(tokens[i][1])
                    y = float(tokens[i+1][1])
                    vertices.append([x, y])
                    current_point = [x, y]
                    i += 2
                else:
                    i += 1
            elif current_cmd in 'mlts':
                # Relative move/line/smooth quad to - needs 2 coordinates
                if i + 1 < len(tokens) and tokens[i+1][1]:
                    x = current_point[0] + float(tokens[i][1])
                    y = current_point[1] + float(tokens[i+1][1])
                    vertices.append([x, y])
                    current_point = [x, y]
                    i += 2
                else:
                    i += 1
            elif current_cmd in 'H':
                # Horizontal line - absolute x
                x = float(tokens[i][1])
                vertices.append([x, current_point[1]])
                current_point = [x, current_point[1]]
                i += 1
            elif current_cmd in 'h':
                # Horizontal line - relative x
                x = current_point[0] + float(tokens[i][1])
                vertices.append([x, current_point[1]])
                current_point = [x, current_point[1]]
                i += 1
            elif current_cmd in 'V':
                # Vertical line - absolute y
                y = float(tokens[i][1])
                vertices.append([current_point[0], y])
                current_point = [current_point[0], y]
                i += 1
            elif current_cmd in 'v':
                # Vertical line - relative y
                y = current_point[1] + float(tokens[i][1])
                vertices.append([current_point[0], y])
                current_point = [current_point[0], y]
                i += 1
            elif current_cmd in 'CSQ':
                # Cubic bezier, quadratic bezier - multiple points
                # For physics, we'll sample points along the curve
                # This is simplified - we just store control points
                points_needed = 6 if current_cmd == 'C' else 4  # Cubic: 3 points * 2 coords, Quad: 2 points * 2 coords
                coords = []
                
                for j in range(points_needed):
                    if i < len(tokens) and tokens[i][1]:
                        coords.append(float(tokens[i][1]))
                        i += 1
                    else:
                        break
                        
                # Add all control points to vertices for now
                # A real implementation would sample the curve
                for j in range(0, len(coords), 2):
                    if j+1 < len(coords):
                        vertices.append([coords[j], coords[j+1]])
                        
                if coords and len(coords) >= 2:
                    current_point = [coords[-2], coords[-1]]
            elif current_cmd in 'csq':
                # Relative versions - same logic but relative to current point
                i += 1  # Skip for simplicity - would need to convert to absolute
            elif current_cmd in 'A':
                # Elliptical arc - complex, simplified for now
                i += 7  # Arc command has 7 parameters
            elif current_cmd in 'a':
                # Relative elliptical arc
                i += 7  # Arc command has 7 parameters
            elif current_cmd in 'ZZ':
                # Close path - connect back to first point
                if vertices:
                    vertices.append(vertices[0])  # Add first point again
                i += 1
            else:
                # Skip unknown command
                i += 1
                
        # Convert to numpy array
        if vertices:
            return np.array(vertices, dtype=np.float32), commands
        return np.zeros((0, 2), dtype=np.float32), commands
        
    def _vertices_to_path(self, vertices: np.ndarray, commands: List[str]) -> str:
        """Convert vertex array back to SVG path data with preserved commands."""
        if len(vertices) == 0:
            return ""
            
        path_parts = []
        vertex_index = 0
        
        # First command is always Move
        path_parts.append(f"M {vertices[0][0]:.3f},{vertices[0][1]:.3f}")
        vertex_index += 1
        
        # Process remaining commands
        for cmd in commands[1:]:
            if cmd in 'ML':
                if vertex_index < len(vertices):
                    path_parts.append(f"{cmd} {vertices[vertex_index][0]:.3f},{vertices[vertex_index][1]:.3f}")
                    vertex_index += 1
            elif cmd in 'H' and vertex_index < len(vertices):
                path_parts.append(f"{cmd} {vertices[vertex_index][0]:.3f}")
                vertex_index += 1
            elif cmd in 'V' and vertex_index < len(vertices):
                path_parts.append(f"{cmd} {vertices[vertex_index][1]:.3f}")
                vertex_index += 1
            elif cmd in 'C' and vertex_index + 2 < len(vertices):
                path_parts.append(
                    f"{cmd} {vertices[vertex_index][0]:.3f},{vertices[vertex_index][1]:.3f} "
                    f"{vertices[vertex_index+1][0]:.3f},{vertices[vertex_index+1][1]:.3f} "
                    f"{vertices[vertex_index+2][0]:.3f},{vertices[vertex_index+2][1]:.3f}"
                )
                vertex_index += 3
            elif cmd in 'SQ' and vertex_index + 1 < len(vertices):
                path_parts.append(
                    f"{cmd} {vertices[vertex_index][0]:.3f},{vertices[vertex_index][1]:.3f} "
                    f"{vertices[vertex_index+1][0]:.3f},{vertices[vertex_index+1][1]:.3f}"
                )
                vertex_index += 2
            elif cmd == 'Z':
                path_parts.append("Z")
            else:
                # Skip command if we don't have enough vertices
                continue
                
        return " ".join(path_parts)
        
    def enable_cuda(self) -> None:
        """Enable CUDA acceleration."""
        self._check_requirements()
        self.cuda_enabled = True
        
    def disable_cuda(self) -> None:
        """Disable CUDA acceleration and use CPU implementation."""
        self.cuda_enabled = False

class RigidBody:
    """Representation of a rigid body in the physics simulation."""
    
    def __init__(
        self, 
        svg_id: str,
        bounds: Tuple[float, float, float, float],
        mass: float = 1.0,
        restitution: float = 0.8
    ):
        """
        Initialize a rigid body.
        
        Args:
            svg_id: ID of the SVG element
            bounds: (x_min, y_min, x_max, y_max) bounding box
            mass: Mass of the rigid body
            restitution: Bounce coefficient (0-1)
        """
        self.svg_id = svg_id
        self.bounds = bounds
        self.mass = mass
        self.restitution = restitution
        self.velocity = np.zeros(2, dtype=np.float32)
        self.position = np.array([
            (bounds[0] + bounds[2]) / 2,  # center x
            (bounds[1] + bounds[3]) / 2   # center y
        ], dtype=np.float32)
        self.forces = np.zeros(2, dtype=np.float32)
        
    def apply_force(self, force: Tuple[float, float]) -> None:
        """Apply force to rigid body."""
        self.forces[0] += force[0]
        self.forces[1] += force[1]
        
    def update(self, dt: float) -> None:
        """Update rigid body state."""
        # Apply forces based on F = ma
        acceleration = self.forces / self.mass
        self.velocity += acceleration * dt
        
        # Update position
        self.position += self.velocity * dt
        
        # Update bounds based on new position
        width = self.bounds[2] - self.bounds[0]
        height = self.bounds[3] - self.bounds[1]
        self.bounds = (
            self.position[0] - width / 2,
            self.position[1] - height / 2,
            self.position[0] + width / 2,
            self.position[1] + height / 2
        )
        
        # Reset forces
        self.forces.fill(0.0)
        
    def check_collision(self, other: 'RigidBody') -> bool:
        """Check collision with another rigid body."""
        return not (
            self.bounds[2] < other.bounds[0] or  # self is to the left
            self.bounds[0] > other.bounds[2] or  # self is to the right
            self.bounds[3] < other.bounds[1] or  # self is above
            self.bounds[1] > other.bounds[3]     # self is below
        )
        
    def resolve_collision(self, other: 'RigidBody') -> None:
        """Resolve collision with another rigid body."""
        # Calculate collision normal
        dx = other.position[0] - self.position[0]
        dy = other.position[1] - self.position[1]
        distance = np.sqrt(dx*dx + dy*dy)
        
        if distance == 0:
            # Avoid division by zero
            normal = np.array([1.0, 0.0])
        else:
            normal = np.array([dx / distance, dy / distance])
            
        # Relative velocity
        rv = other.velocity - self.velocity
        
        # Relative velocity along normal
        vel_along_normal = np.dot(rv, normal)
        
        # Do not resolve if velocities are separating
        if vel_along_normal > 0:
            return
            
        # Calculate impulse scalar
        restitution = min(self.restitution, other.restitution)
        
        # Calculate impulse scalar
        j = -(1 + restitution) * vel_along_normal
        j /= 1/self.mass + 1/other.mass
        
        # Apply impulse
        impulse = j * normal
        
        # Update velocities
        self.velocity -= impulse / self.mass
        other.velocity += impulse / other.mass

@FeatureRegistry.register('physics-force', ['numpy'])
class ForceField:
    """Force field that can be applied to physics objects."""
    
    def __init__(
        self, 
        center: Tuple[float, float],
        radius: float,
        strength: float,
        type: str = "radial"  # Options: "radial", "directional"
    ):
        """
        Initialize force field.
        
        Args:
            center: (x, y) center of the field
            radius: Radius of effect
            strength: Force strength (negative for attractive)
            type: "radial" or "directional"
        """
        self.center = np.array(center)
        self.radius = radius
        self.strength = strength
        self.type = type
        self.direction = np.array([1.0, 0.0])  # Default direction
        
    def set_direction(self, direction: Tuple[float, float]) -> None:
        """Set direction vector for directional fields."""
        magnitude = np.sqrt(direction[0]**2 + direction[1]**2)
        if magnitude > 0:
            self.direction = np.array([
                direction[0] / magnitude,
                direction[1] / magnitude
            ])
            
    def get_force_at(self, position: np.ndarray) -> np.ndarray:
        """Get force vector at position."""
        # Calculate distance to center
        delta = position - self.center
        distance = np.sqrt(np.sum(delta**2))
        
        # No force beyond radius
        if distance > self.radius:
            return np.zeros(2)
            
        # Calculate force based on type
        if self.type == "radial":
            # Force falls off with square of distance
            direction = delta / (distance + 1e-6)  # Avoid division by zero
            falloff = 1.0 - (distance / self.radius)
            return direction * self.strength * falloff
        elif self.type == "directional":
            # Constant force in the specified direction
            falloff = 1.0 - (distance / self.radius)
            return self.direction * self.strength * falloff
        else:
            return np.zeros(2)

@FeatureRegistry.register('physics', ['numpy'])
class PhysicsManager:
    """
    Main manager class that connects SVG physics components.
    
    This class integrates fluid dynamics, soft body deformation,
    and rigid body physics to provide a complete physics system
    for SVG elements.
    """
    
    def __init__(self, gravity: Tuple[float, float] = (0, 9.8)):
        """
        Initialize physics manager.
        
        Args:
            gravity: (x, y) gravity vector
        """
        self.gravity = np.array(gravity, dtype=np.float32)
        self.fluid_sim = FluidSimulation()
        self.soft_body_sim = SoftBodyDeformation()
        self.rigid_bodies = {}  # Dict[str, RigidBody]
        self.force_fields = []  # List[ForceField]
        self.collider_groups = {}  # Dict[str, List[str]]
        self.svg_paths = {}  # Dict[str, str]
        
    def create_rigid_body(
        self, 
        svg_id: str,
        bounds: Tuple[float, float, float, float],
        mass: float = 1.0,
        restitution: float = 0.8
    ) -> RigidBody:
        """
        Create a rigid body for an SVG element.
        
        Args:
            svg_id: ID of the SVG element
            bounds: (x_min, y_min, x_max, y_max) bounding box
            mass: Mass of the rigid body
            restitution: Bounce coefficient (0-1)
            
        Returns:
            Created RigidBody instance
        """
        body = RigidBody(svg_id, bounds, mass, restitution)
        self.rigid_bodies[svg_id] = body
        return body
        
    def add_force_field(
        self, 
        center: Tuple[float, float],
        radius: float,
        strength: float,
        field_type: str = "radial"
    ) -> ForceField:
        """
        Add a force field to the simulation.
        
        Args:
            center: (x, y) center of the field
            radius: Radius of effect
            strength: Force strength (negative for attraction)
            field_type: "radial" or "directional"
            
        Returns:
            Created ForceField instance
        """
        field = ForceField(center, radius, strength, field_type)
        self.force_fields.append(field)
        return field
        
    def start_fluid_simulation(
        self,
        bounds: Tuple[float, float, float, float],
        num_particles: int = 1000
    ) -> None:
        """
        Start fluid simulation within bounds.
        
        Args:
            bounds: (x_min, y_min, x_max, y_max) of fluid container
            num_particles: Number of fluid particles
        """
        self.fluid_sim.num_particles = num_particles
        self.fluid_sim.init_particles(bounds)
        
    def register_svg_path(self, svg_id: str, path_data: str) -> None:
        """
        Register an SVG path for deformation.
        
        Args:
            svg_id: ID of the SVG element
            path_data: Original SVG path data
        """
        self.svg_paths[svg_id] = path_data
        
    def deform_path(
        self,
        svg_id: str,
        force_field: Optional[np.ndarray] = None
    ) -> str:
        """
        Apply soft body deformation to a registered SVG path.
        
        Args:
            svg_id: ID of the SVG element
            force_field: Optional external force field
            
        Returns:
            Deformed path data
        """
        if svg_id not in self.svg_paths:
            raise ValueError(f"Path with ID {svg_id} not registered")
            
        return self.soft_body_sim.deform_path(
            self.svg_paths[svg_id],
            force_field
        )
        
    def update(self, dt: float) -> Dict[str, Any]:
        """
        Update physics simulation state.
        
        Args:
            dt: Time step
            
        Returns:
            Dict with updated physics state
        """
        results = {}
        
        # Update rigid bodies
        for body_id, body in self.rigid_bodies.items():
            # Apply gravity
            body.apply_force((
                self.gravity[0] * body.mass,
                self.gravity[1] * body.mass
            ))
            
            # Apply force fields
            pos = body.position
            for field in self.force_fields:
                force = field.get_force_at(pos)
                body.apply_force((force[0], force[1]))
                
            # Update body state
            body.update(dt)
            
            # Store updated transform
            results[body_id] = {
                'transform': f"translate({body.position[0]},{body.position[1]})",
                'position': (body.position[0], body.position[1]),
                'velocity': (body.velocity[0], body.velocity[1])
            }
            
        # Check for collisions
        for id1, body1 in self.rigid_bodies.items():
            for id2, body2 in self.rigid_bodies.items():
                if id1 != id2 and body1.check_collision(body2):
                    body1.resolve_collision(body2)
                    
        # Update fluid simulation if initialized
        if hasattr(self.fluid_sim, 'particles') and self.fluid_sim.particles is not None:
            # Create boundary list from rigid bodies
            boundaries = [
                (body.bounds[0], body.bounds[1], body.bounds[2], body.bounds[3])
                for body in self.rigid_bodies.values()
            ]
            
            # Run fluid update
            fluid_positions = self.fluid_sim.update(dt, boundaries)
            results['fluid'] = {
                'positions': fluid_positions
            }
            
        # Deform registered paths
        deformed_paths = {}
        for svg_id, path_data in self.svg_paths.items():
            # Create simplified force field based on nearby forces
            # This is a simplified approach - a more accurate approach would
            # use the actual force field calculations
            force_field = np.zeros((100, 2), dtype=np.float32)
            for i, field in enumerate(self.force_fields):
                if i < len(force_field):
                    force_field[i] = field.get_force_at(np.array([0, 0]))
                    
            deformed_paths[svg_id] = self.deform_path(svg_id, force_field)
            
        results['deformed_paths'] = deformed_paths
        
        return results
        
    def enable_cuda(self) -> bool:
        """
        Enable CUDA acceleration.
        
        Returns:
            True if CUDA was successfully enabled
        """
        fluid_result = self.fluid_sim.try_enable_cuda()
        soft_body_result = self.soft_body_sim.try_enable_cuda()
        return fluid_result and soft_body_result
        
    def disable_cuda(self) -> None:
        """Disable CUDA acceleration and use CPU implementation."""
        self.fluid_sim.cuda_enabled = False
        self.soft_body_sim.cuda_enabled = False
