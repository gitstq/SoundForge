# Contributing to SoundForge

Thank you for your interest in contributing to SoundForge! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- (Optional) ffmpeg for non-WAV format conversion

### Setup
```bash
git clone https://github.com/yourusername/soundforge.git
cd soundforge
pip install -e .
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
- Follow PEP 8
- Use type hints on all function signatures
- Add docstrings to all public functions and classes
- Maximum line length: 100 characters

### Project Structure
```
soundforge/
├── src/soundforge/     # Source code
│   ├── cli.py          # CLI entry point
│   ├── converter.py    # Format conversion
│   ├── editor.py       # Audio editing
│   ├── analyzer.py     # Audio analysis
│   ├── visualizer.py   # Waveform visualization
│   ├── batch.py        # Batch processing
│   ├── recorder.py     # Audio recording
│   ├── utils.py        # Shared utilities
│   └── exceptions.py   # Custom exceptions
└── tests/              # Test files
```

## Making Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`python -m pytest tests/`)
6. Commit with a descriptive message
7. Push to your fork (`git push origin feature/your-feature`)
8. Open a Pull Request

## Commit Messages
- Use imperative mood in subject line (e.g., "Add feature" not "Added feature")
- Keep subject line under 72 characters
- Reference issue numbers when applicable

## Reporting Issues

When reporting bugs, please include:
- Python version
- Operating system
- SoundForge version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/tracebacks

## Feature Requests

Feature requests are welcome! Please describe:
- The use case
- Expected behavior
- Any examples or references

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
