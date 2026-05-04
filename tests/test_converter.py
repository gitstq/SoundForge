"""
Tests for the AudioConverter module.
"""

import os
import struct
import tempfile
import wave

import pytest

from soundforge.converter import AudioConverter
from soundforge.exceptions import AudioFileNotFoundError, FormatNotSupportedError, InvalidAudioError


@pytest.fixture
def sample_wav(tmp_path):
    """Create a sample WAV file for testing."""
    filepath = str(tmp_path / "test.wav")
    sample_rate = 44100
    duration = 1.0  # 1 second
    n_frames = int(sample_rate * duration)
    n_channels = 1
    sample_width = 2

    with wave.open(filepath, "wb") as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)

        # Generate a simple sine wave
        for i in range(n_frames):
            import math
            value = int(32767 * 0.5 * math.sin(2 * math.pi * 440 * i / sample_rate))
            wf.writeframes(struct.pack("<h", value))

    return filepath


@pytest.fixture
def stereo_wav(tmp_path):
    """Create a stereo WAV file for testing."""
    filepath = str(tmp_path / "stereo.wav")
    sample_rate = 44100
    duration = 0.5
    n_frames = int(sample_rate * duration)

    with wave.open(filepath, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)

        import math
        for i in range(n_frames):
            left = int(32767 * 0.5 * math.sin(2 * math.pi * 440 * i / sample_rate))
            right = int(32767 * 0.3 * math.sin(2 * math.pi * 880 * i / sample_rate))
            wf.writeframes(struct.pack("<hh", left, right))

    return filepath


class TestAudioConverter:
    """Tests for AudioConverter class."""

    def test_init(self):
        """Test converter initialization."""
        converter = AudioConverter()
        assert hasattr(converter, "ffmpeg_available")

    def test_convert_wav_to_wav(self, sample_wav, tmp_path):
        """Test WAV to WAV conversion."""
        converter = AudioConverter()
        output = str(tmp_path / "output.wav")
        result = converter.convert(sample_wav, output)
        assert os.path.isfile(result)
        assert os.path.getsize(result) > 0

    def test_convert_wav_to_wav_with_params(self, sample_wav, tmp_path):
        """Test WAV to WAV conversion with custom parameters."""
        converter = AudioConverter()
        output = str(tmp_path / "output_22k.wav")
        result = converter.convert(
            sample_wav, output,
            sample_rate=22050,
            channels=1,
            verbose=True,
        )
        assert os.path.isfile(result)

        # Verify new sample rate
        with wave.open(result, "rb") as wf:
            assert wf.getframerate() == 22050
            assert wf.getnchannels() == 1

    def test_convert_stereo_to_mono(self, stereo_wav, tmp_path):
        """Test stereo to mono conversion."""
        converter = AudioConverter()
        output = str(tmp_path / "mono.wav")
        result = converter.convert(stereo_wav, output, channels=1)
        assert os.path.isfile(result)

        with wave.open(result, "rb") as wf:
            assert wf.getnchannels() == 1

    def test_convert_nonexistent_file(self, tmp_path):
        """Test converting a file that doesn't exist."""
        converter = AudioConverter()
        output = str(tmp_path / "output.wav")
        with pytest.raises(AudioFileNotFoundError):
            converter.convert("/nonexistent/file.wav", output)

    def test_convert_unsupported_format(self, sample_wav, tmp_path):
        """Test converting to an unsupported format."""
        converter = AudioConverter()
        output = str(tmp_path / "output.xyz")
        with pytest.raises(FormatNotSupportedError):
            converter.convert(sample_wav, output)

    def test_get_supported_formats(self):
        """Test getting supported formats list."""
        converter = AudioConverter()
        formats = converter.get_supported_formats()
        assert "wav" in formats
        assert formats["wav"]["native"] is True

    def test_print_supported_formats(self, capsys):
        """Test printing supported formats."""
        converter = AudioConverter()
        converter.print_supported_formats()
        captured = capsys.readouterr()
        assert "WAV" in captured.out


class TestFormatDetection:
    """Tests for format detection via converter."""

    def test_wav_format_detected(self, sample_wav):
        """Test that WAV format is correctly identified."""
        from soundforge.analyzer import AudioAnalyzer
        analyzer = AudioAnalyzer()
        fmt = analyzer.detect_format(sample_wav)
        assert fmt == "wav"
