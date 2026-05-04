"""Setup script for SoundForge."""

from setuptools import setup, find_packages

setup(
    name="soundforge",
    version="0.1.0",
    description="Lightweight Terminal Audio Processing CLI Toolbox",
    long_description="",
    long_description_content_type="text/markdown",
    author="SoundForge Contributors",
    license="MIT",
    python_requires=">=3.8",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "soundforge=soundforge.cli:main",
        ],
    },
    extras_require={
        "recording": ["sounddevice>=0.4.0"],
        "dev": ["pytest>=7.0", "pytest-cov>=4.0"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Utilities",
        "Environment :: Console",
    ],
)
