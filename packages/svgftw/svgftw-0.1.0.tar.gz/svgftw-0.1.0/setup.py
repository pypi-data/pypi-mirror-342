from setuptools import setup, find_packages

# Read the README for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="svgftw",
    version="0.1.0",
    author="SVGFTW Team",
    author_email="info@svgftw.org",
    description="Advanced SVG manipulation with quantum, AI, and bio-algorithm features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/svgftw/svgftw",
    project_urls={
        "Bug Tracker": "https://github.com/svgftw/svgftw/issues",
        "Documentation": "https://svgftw.readthedocs.io/",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Quantum Computing",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    ],
    package_dir={"": "svgftwlib/src"},
    packages=find_packages(where="svgftwlib/src"),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "lxml>=4.9.0",
        "pillow>=9.0.0",
    ],
    extras_require={
        # AI features split into more granular options
        'ai-basic': [
            'onnxruntime>=1.8.0',
        ],
        'ai-full': [
            'onnxruntime>=1.8.0',
            'torch>=1.9.0',
        ],
        'ai-cuda': [
            'onnxruntime>=1.8.0',
            'torch>=1.9.0',
            'numba>=0.55.0',
        ],
        
        # Quantum computing features
        'quantum': [
            'qiskit>=0.34.2',
        ],
        
        # Bio-algorithm features
        'bio': [
            'scikit-bio>=0.5.7',
        ],
        
        # Feature bundles
        'minimal': [
            'onnxruntime>=1.8.0',  # Basic AI support
        ],
        'recommended': [
            'onnxruntime>=1.8.0',
            'torch>=1.9.0',
            'qiskit>=0.34.2',
        ],
        'complete': [
            'onnxruntime>=1.8.0',
            'torch>=1.9.0',
            'qiskit>=0.34.2',
            'scikit-bio>=0.5.7',
            'numba>=0.55.0',
        ],
        
        # Development dependencies
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.3.0',
            'mypy>=0.950',
        ],
    },
    entry_points={
        'console_scripts': [
            'svgftw=svgftw.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
