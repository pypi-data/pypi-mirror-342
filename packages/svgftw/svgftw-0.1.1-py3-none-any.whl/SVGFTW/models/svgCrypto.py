"""
SVG cryptographic features including steganography, blockchain watermarking,
DNA-based cryptography, and post-quantum cryptography.
"""

from typing import Dict, Any, Optional, Union, List, Tuple
import numpy as np
from pathlib import Path
import json
import hashlib
from itertools import product
try:
    import pqcrypto
    from pqcrypto.sign import dilithium2
    PQ_CRYPTO_AVAILABLE = True
except ImportError:
    PQ_CRYPTO_AVAILABLE = False

# DNA Encoding Constants
DNA_BASES = ['A', 'T', 'C', 'G']
CODON_LENGTH = 3
CODONS = [''.join(p) for p in product(DNA_BASES, repeat=CODON_LENGTH)]

class VectorSteganography:
    """Handle steganographic operations in SVG paths."""
    
    def __init__(self):
        """Initialize steganography system."""
        self.embedded_data = {}
        self.lattice_dims = 256
        
        # Initialize DNA encoding mappings
        self._initialize_dna_mappings()
        
    def _initialize_dna_mappings(self) -> None:
        """Initialize DNA base and codon mappings."""
        # Create codon to binary mappings (6-bit encoding)
        self.codon_to_bits = {
            codon: format(i, '06b')
            for i, codon in enumerate(CODONS)
        }
        self.bits_to_codon = {v: k for k, v in self.codon_to_bits.items()}
        
        # Create base pair to coordinate offset mappings
        self.base_to_offset = {
            'A': (0.001, 0.001),   # Small positive offsets
            'T': (-0.001, -0.001), # Small negative offsets
            'C': (0.001, -0.001),  # Mixed offsets
            'G': (-0.001, 0.001)   # Mixed offsets
        }
        
    def embed_dna_sequence(
        self,
        path_data: str,
        dna_sequence: str,
        error_correction: bool = True
    ) -> str:
        """
        Embed DNA sequence into path coordinates using codon patterns.
        
        Args:
            path_data: Original SVG path data
            dna_sequence: DNA sequence to embed
            error_correction: Enable error correction
            
        Returns:
            Modified path data with embedded DNA
        """
        # Validate DNA sequence
        if not all(base in DNA_BASES for base in dna_sequence.upper()):
            raise ValueError("Invalid DNA sequence")
            
        # Add error correction if enabled
        if error_correction:
            dna_sequence = self._add_dna_error_correction(dna_sequence)
            
        # Convert to codons
        codons = [
            dna_sequence[i:i+CODON_LENGTH]
            for i in range(0, len(dna_sequence), CODON_LENGTH)
        ]
        
        # Embed in path coordinates
        segments = self._parse_path(path_data)
        modified_segments = []
        codon_index = 0
        
        for segment in segments:
            if codon_index >= len(codons):
                modified_segments.append(segment)
                continue
                
            # Embed codon in control points
            codon = codons[codon_index]
            modified_points = []
            
            for i, point in enumerate(segment['points']):
                if i < len(codon):
                    # Apply base pair offset
                    offset = self.base_to_offset[codon[i]]
                    modified_points.append(point + offset[0])
                    modified_points.append(point + offset[1])
                else:
                    modified_points.extend([point, point])
                    
            segment['points'] = modified_points
            modified_segments.append(segment)
            codon_index += 1
            
        return self._segments_to_path(modified_segments)
        
    def extract_dna_sequence(
        self,
        path_data: str,
        error_correction: bool = True
    ) -> str:
        """
        Extract DNA sequence from path coordinates.
        
        Args:
            path_data: SVG path data with embedded DNA
            error_correction: Enable error correction
            
        Returns:
            Extracted DNA sequence
        """
        segments = self._parse_path(path_data)
        extracted_bases = []
        
        for segment in segments:
            points = segment['points']
            if len(points) < 2:
                continue
                
            # Process point pairs for base extraction
            for i in range(0, len(points) - 1, 2):
                p1, p2 = points[i:i+2]
                dx = p2 - p1
                
                # Determine base from offset pattern
                base = self._offset_to_base(dx)
                if base:
                    extracted_bases.append(base)
                    
        # Combine bases into sequence
        dna_sequence = ''.join(extracted_bases)
        
        # Apply error correction if enabled
        if error_correction:
            dna_sequence = self._correct_dna_errors(dna_sequence)
            
        return dna_sequence
        
    def _add_dna_error_correction(self, sequence: str) -> str:
        """Add error correction to DNA sequence."""
        # Simple parity-based error correction
        corrected = []
        
        for codon in [sequence[i:i+3] for i in range(0, len(sequence), 3)]:
            # Add parity base
            bases_sum = sum(DNA_BASES.index(b) for b in codon)
            parity = DNA_BASES[bases_sum % 4]
            corrected.extend([codon, parity])
            
        return ''.join(corrected)
        
    def _correct_dna_errors(self, sequence: str) -> str:
        """Correct errors in DNA sequence using parity."""
        corrected = []
        
        # Process sequence in codon+parity groups
        for i in range(0, len(sequence), 4):
            group = sequence[i:i+4]
            if len(group) < 4:
                break
                
            codon = group[:3]
            parity = group[3]
            
            # Verify parity
            bases_sum = sum(DNA_BASES.index(b) for b in codon)
            expected_parity = DNA_BASES[bases_sum % 4]
            
            if parity != expected_parity:
                # Attempt error correction
                codon = self._repair_codon(codon, expected_parity)
                
            corrected.append(codon)
            
        return ''.join(corrected)
        
    def _repair_codon(self, codon: str, parity: str) -> str:
        """Attempt to repair corrupted codon."""
        for i in range(3):
            for base in DNA_BASES:
                test_codon = codon[:i] + base + codon[i+1:]
                bases_sum = sum(DNA_BASES.index(b) for b in test_codon)
                if DNA_BASES[bases_sum % 4] == parity:
                    return test_codon
        return codon
        
    def _offset_to_base(self, offset: Tuple[float, float]) -> Optional[str]:
        """Convert coordinate offset to DNA base."""
        # Find closest matching offset pattern
        min_dist = float('inf')
        best_base = None
        
        for base, pattern in self.base_to_offset.items():
            dist = np.sqrt(
                (offset[0] - pattern[0])**2 +
                (offset[1] - pattern[1])**2
            )
            if dist < min_dist:
                min_dist = dist
                best_base = base
                
        # Return base only if offset matches pattern closely
        return best_base if min_dist < 0.002 else None

    def embed_data(
        self, 
        path_data: str, 
        payload: Union[str, bytes],
        impact_threshold: float = 0.1
    ) -> str:
        """
        Embed data in path curvature using lattice-based techniques.
        
        Args:
            path_data: Original SVG path data
            payload: Data to embed
            impact_threshold: Max allowed visual impact (0-1)
            
        Returns:
            Modified path data with embedded information
        """
        # Convert payload to bytes if needed
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
            
        # Parse path into segments
        segments = self._parse_path(path_data)
        
        # Embed data across curve control points
        modified_segments = []
        payload_bits = ''.join(format(b, '08b') for b in payload)
        bit_index = 0
        
        for segment in segments:
            if bit_index >= len(payload_bits):
                modified_segments.append(segment)
                continue
                
            if segment['type'] in {'C', 'Q', 'S', 'T'}:
                # Modify control points to embed data
                control_points = segment['points']
                modified_points = self._embed_in_control_points(
                    control_points,
                    payload_bits[bit_index:bit_index + 8],
                    impact_threshold
                )
                bit_index += 8
                
                segment['points'] = modified_points
                
            modified_segments.append(segment)
            
        return self._segments_to_path(modified_segments)
        
    def extract_data(self, path_data: str) -> bytes:
        """
        Extract embedded data from path curvature.
        
        Args:
            path_data: SVG path data with embedded information
            
        Returns:
            Extracted payload as bytes
        """
        segments = self._parse_path(path_data)
        payload_bits = []
        
        for segment in segments:
            if segment['type'] in {'C', 'Q', 'S', 'T'}:
                control_points = segment['points']
                extracted_bits = self._extract_from_control_points(
                    control_points
                )
                payload_bits.extend(extracted_bits)
                
        # Convert bits to bytes
        payload_bytes = []
        for i in range(0, len(payload_bits), 8):
            if i + 8 <= len(payload_bits):
                byte = int(''.join(payload_bits[i:i+8]), 2)
                payload_bytes.append(byte)
                
        return bytes(payload_bytes)
        
    def _embed_in_control_points(
        self,
        points: list,
        bits: str,
        impact_threshold: float
    ) -> list:
        """Embed data bits in curve control points."""
        modified_points = points.copy()
        
        for i, bit in enumerate(bits):
            if i >= len(points):
                break
                
            # Modify least significant digits while preserving curve shape
            point = modified_points[i]
            modified_point = self._modify_point(
                point,
                int(bit),
                impact_threshold
            )
            modified_points[i] = modified_point
            
        return modified_points
        
    def _extract_from_control_points(self, points: list) -> list:
        """Extract data bits from curve control points."""
        bits = []
        
        for point in points:
            # Extract bit from point coordinates
            bit = self._extract_bit(point)
            bits.append(str(bit))
            
        return bits
        
    def _modify_point(
        self,
        point: float,
        bit: int,
        impact_threshold: float
    ) -> float:
        """Modify coordinate value to embed a bit."""
        # Use lattice-based embedding for security
        lattice_point = round(point * self.lattice_dims)
        parity = lattice_point % 2
        
        if parity != bit:
            # Find closest lattice point with correct parity
            if lattice_point % 2 == 0:
                candidates = [lattice_point + 1, lattice_point - 1]
            else:
                candidates = [lattice_point + 1, lattice_point - 1]
                
            # Choose modification with minimal visual impact
            deltas = [abs(c/self.lattice_dims - point) for c in candidates]
            if min(deltas) <= impact_threshold:
                best_candidate = candidates[deltas.index(min(deltas))]
                return best_candidate / self.lattice_dims
                
        return point
        
    def _extract_bit(self, point: float) -> int:
        """Extract embedded bit from coordinate value."""
        lattice_point = round(point * self.lattice_dims)
        return lattice_point % 2
        
    def _parse_path(self, path_data: str) -> list:
        """Parse SVG path into segments with points."""
        segments = []
        tokens = path_data.split()
        current_segment = None
        
        for token in tokens:
            if token[0].isalpha():
                if current_segment:
                    segments.append(current_segment)
                current_segment = {
                    'type': token,
                    'points': []
                }
            else:
                try:
                    value = float(token)
                    current_segment['points'].append(value)
                except ValueError:
                    continue
                    
        if current_segment:
            segments.append(current_segment)
            
        return segments
        
    def _segments_to_path(self, segments: list) -> str:
        """Convert segments back to path string."""
        path_parts = []
        
        for segment in segments:
            path_parts.append(segment['type'])
            points = [f"{p:.3f}" for p in segment['points']]
            path_parts.extend(points)
            
        return ' '.join(path_parts)


class BlockchainWatermark:
    """Handle blockchain-based watermarking for SVG provenance."""
    
    def __init__(self):
        """Initialize blockchain watermarking system."""
        self.transform_precision = 6
        
    def embed_metadata(
        self,
        element: Dict[str, Any],
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Embed NFT/blockchain metadata in SVG element transforms.
        
        Args:
            element: SVG element dictionary
            metadata: Blockchain metadata to embed
            
        Returns:
            Modified element with embedded metadata
        """
        # Generate deterministic hash from metadata
        metadata_hash = self._hash_metadata(metadata)
        
        # Convert hash to transform parameters
        transform_matrix = self._hash_to_transform(metadata_hash)
        
        # Apply subtle transform that encodes the hash
        element = self._apply_transform(element, transform_matrix)
        
        # Store verification data
        element['data-blockchain-proof'] = metadata_hash
        
        return element
        
    def verify_metadata(
        self,
        element: Dict[str, Any],
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Verify blockchain metadata matches element transforms.
        
        Args:
            element: SVG element with embedded metadata
            metadata: Metadata to verify
            
        Returns:
            True if verification succeeds
        """
        if 'data-blockchain-proof' not in element:
            return False
            
        stored_hash = element['data-blockchain-proof']
        verify_hash = self._hash_metadata(metadata)
        
        return stored_hash == verify_hash
        
    def _hash_metadata(self, metadata: Dict[str, Any]) -> str:
        """Generate deterministic hash from metadata."""
        # Sort keys for consistency
        ordered_data = json.dumps(metadata, sort_keys=True)
        return hashlib.sha256(
            ordered_data.encode('utf-8')
        ).hexdigest()
        
    def _hash_to_transform(self, hash_value: str) -> list:
        """Convert hash to transform matrix values."""
        # Use hash to generate subtle transform parameters
        hash_bytes = bytes.fromhex(hash_value)
        matrix = []
        
        for i in range(0, 12, 2):
            if i >= len(hash_bytes):
                break
            # Generate small transform values from hash bytes
            value = (
                (hash_bytes[i] * 256 + hash_bytes[i+1])
                / 65535  # Normalize to [0,1]
                * 0.001  # Scale to small values
                + 1      # Center around 1 for minimal visual impact
            )
            matrix.append(round(value, self.transform_precision))
            
        return matrix
        
    def _apply_transform(
        self,
        element: Dict[str, Any],
        matrix: list
    ) -> Dict[str, Any]:
        """Apply transform matrix to element."""
        if len(matrix) < 6:
            return element
            
        # Create transform string
        transform = (
            f"matrix({matrix[0]},{matrix[1]},{matrix[2]},"
            f"{matrix[3]},{matrix[4]},{matrix[5]})"
        )
        
        # Combine with existing transforms if any
        if 'transform' in element:
            transform = f"{element['transform']} {transform}"
            
        element['transform'] = transform
        return element


class PostQuantumOptimizer:
    """
    Handle post-quantum cryptographic operations for SVG security.
    """
    
    def __init__(self):
        """Initialize post-quantum optimization system."""
        self._check_requirements()
        self.signature_key = None
        
    def _check_requirements(self) -> None:
        """Verify post-quantum crypto requirements are met."""
        if not PQ_CRYPTO_AVAILABLE:
            raise ImportError(
                "Post-quantum features require pqcrypto. "
                "Install with: pip install pqcrypto"
            )
            
    def generate_keys(self) -> None:
        """Generate post-quantum signing keys."""
        self.public_key, self.secret_key = dilithium2.generate_keypair()
        
    def secure_path_simplification(
        self,
        path_data: str,
        preserve_features: Optional[list] = None
    ) -> str:
        """
        Optimize path while maintaining cryptographic features.
        
        Args:
            path_data: Original path data
            preserve_features: List of features to preserve
            
        Returns:
            Optimized path data
        """
        segments = self._parse_path(path_data)
        optimized = []
        
        for segment in segments:
            if preserve_features and self._has_crypto_features(
                segment,
                preserve_features
            ):
                # Preserve segments with crypto features
                optimized.append(segment)
            else:
                # Optimize other segments
                optimized.append(
                    self._optimize_segment(segment)
                )
                
        return self._segments_to_path(optimized)
        
    def quantum_safe_compression(
        self,
        svg_data: str,
        min_ratio: float = 0.9
    ) -> str:
        """
        Compress SVG while maintaining quantum resistance.
        
        Args:
            svg_data: Original SVG content
            min_ratio: Minimum compression ratio
            
        Returns:
            Compressed SVG content
        """
        # TODO: Implement quantum-resistant compression
        # This is a placeholder that maintains the original data
        return svg_data
        
    def _has_crypto_features(
        self,
        segment: Dict[str, Any],
        features: list
    ) -> bool:
        """Check if segment contains cryptographic features."""
        # Example feature detection - extend based on needs
        if 'steganography' in features:
            # Check for embedded data patterns
            return self._detect_steganography(segment)
            
        if 'watermark' in features:
            # Check for blockchain watermarks
            return 'data-blockchain-proof' in segment
            
        return False
        
    def _detect_steganography(
        self,
        segment: Dict[str, Any]
    ) -> bool:
        """Detect presence of steganographic data."""
        if segment['type'] not in {'C', 'Q', 'S', 'T'}:
            return False
            
        # Check control points for steganographic patterns
        points = segment['points']
        for point in points:
            if self._is_lattice_point(point):
                return True
                
        return False
        
    def _is_lattice_point(self, value: float) -> bool:
        """Check if value appears to be on data embedding lattice."""
        # This is a simplified check - extend based on actual embedding method
        lattice_dims = 256
        lattice_point = round(value * lattice_dims)
        reconstruction = lattice_point / lattice_dims
        return abs(value - reconstruction) < 1e-6
