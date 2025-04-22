"""
SVGFTW: Advanced SVG manipulation library with quantum, AI, and bio-algorithm features.
"""

from .core import SVG
from .utilities import convert_units, optimize_path
from .utils.feature_loader import FeatureRegistry

# Initialize lazy-loaded feature proxies
def _get_proxy(feature_name):
    """Get a proxy for a feature."""
    from .utils.feature_loader import LazyLoadProxy
    return LazyLoadProxy(feature_name)

# Core features always available
__all__ = ['SVG', 'convert_units', 'optimize_path']

# Optional features
_optional_features = {
    'ai': {
        'AIVectorStylerBasic': 'ai-basic',
        'AIVectorStyler': 'ai-full',
    },
    'quantum': {
        'QuantumLayoutOptimizer': 'quantum',
    },
    'bio': {
        'BioPatternEngine': 'bio-basic',
        'NeuralBioPattern': 'bio-neural',
    }
}

# Register available features
for module, features in _optional_features.items():
    for class_name, feature_name in features.items():
        if FeatureRegistry.is_available(feature_name):
            globals()[class_name] = _get_proxy(feature_name)
            __all__.append(class_name)

def get_available_features():
    """Get list of available optional features."""
    available = {}
    for module, features in _optional_features.items():
        available[module] = {
            class_name: FeatureRegistry.is_available(feature_name)
            for class_name, feature_name in features.items()
        }
    return available

__version__ = '0.1.0'
