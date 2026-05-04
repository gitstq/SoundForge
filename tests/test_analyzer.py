"""
Tests for the AudioAnalyzer module.
"""

import os
import struct
import tempfile
import wave

import pytest

from soundforge.analyzer import AudioAnalyzer
from soundforge.exceptions import AudioFileNotFoundError, InvalidAudioError


@pytest.fixture
def sample_wav(tmp_path):
    """Create a sample WAV file for testing."""
    filepath = str(tmp_path / "test.wav")
    sample_rate = 44100
    duration = 1.0
    n_frames = int(sample_rate * duration)

    with wave.open(filepath, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)

        import math
        for i in range(n_frames):
            value = int(32767 * 0.5 * math.sin(2 * math.pi * 440 * i / sample_rate))
            wf.writeframes(struct.pack("<h", value))

    return filepath


@pytest.fixture
def silent_wav(tmp_path):
    """Create a silent WAV file for testing."""
    filepath = str(tmp_path / "silent.wav")
    sample_rate = 22050
    n_frames = sample_rate  # 1 second

    with wave.open(filepath, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b"\x00\x00" * n_frames)

    return filepath


@pytest.fixture
def stereo_wav(tmp_path):
    """Create a stereo WAV file for testing."""
    filepath = str(tmp_path / "stereo.wav")
    sample_rate = 44100
    n_frames = 22050

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


class TestAudioAnalyzer:
    """Tests for AudioAnalyzer class."""

    def test_detect_format_wav(self, sample_wav):
        """Test WAV format detection."""
        analyzer = AudioAnalyzer()
        assert analyzer.detect_format(sample_wav) == "wav"

    def test_detect_format_nonexistent(self):
        """Test format detection for nonexistent file."""
        analyzer = AudioAnalyzer()
        with pytest.raises(AudioFileNotFoundError):
            analyzer.detect_format("/nonexistent/file.wav")

    def test_detect_format_invalid(self, tmp_path):
        """Test format detection for invalid file."""
        filepath = str(tmp_path / "not_audio.txt")
        with open(filepath, "w") as f:
            f.write("This is not audio data")

        analyzer = AudioAnalyzer()
        # Should fall back to extension-based detection
        fmt = analyzer.detect_format(filepath)
        assert fmt == "txt" or fmt == "unknown"

    def test_get_info(self, sample_wav):
        """Test getting audio info."""
        analyzer = AudioAnalyzer()
        info = analyzer.get_info(sample_wav)

        assert info["format"] == "wav"
        assert info["duration"] is not None
        assert info["duration"] >= 0.9  # ~1 second
        assert info["sample_rate"] == 44100
        assert info["channels"] == 1
        assert info["bit_depth"] == 16
        assert info["file_size"] > 0

    def test_get_info_stereo(self, stereo_wav):
        """Test getting info for stereo file."""
        analyzer = AudioAnalyzer()
        info = analyzer.get_info(stereo_wav)
        assert info["channels"] == 2

    def test_get_info_nonexistent(self):
        """Test getting info for nonexistent file."""
        analyzer = AudioAnalyzer()
        with pytest.raises(AudioFileNotFoundError):
            analyzer.get_info("/nonexistent/file.wav")

    def test_calculate_loudness(self, sample_wav):
        """Test loudness calculation."""
        analyzer = AudioAnalyzer()
        loudness = analyzer.calculate_loudness(sample_wav)

        assert "rms_db" in loudness
        assert "peak_db" in loudness
        assert "rms_linear" in loudness
        assert "peak_linear" in loudness
        assert loudness["rms_linear"] > 0
        assert loudness["peak_linear"] > 0
        assert loudness["rms_db"] > -60
        assert loudness["peak_db"] > -60

    def test_calculate_loudness_silent(self, silent_wav):
        """Test loudness calculation for silent file."""
        analyzer = AudioAnalyzer()
        loudness = analyzer.calculate_loudness(silent_wav)

        assert loudness["rms_linear"] == 0.0
        assert loudness["peak_linear"] == 0.0

    def test_print_info(self, sample_wav, capsys):
        """Test print_info output."""
        analyzer = AudioAnalyzer()
        analyzer.print_info(sample_wav)
        captured = capsys.readouterr()
        assert "WAV" in captured.out
        assert "44100" in captured.out or "44.1" in captured.out

    def test_print_info_verbose(self, sample_wav, capsys):
        """Test print_info with verbose flag."""
        analyzer = AudioAnalyzer()
        analyzer.print_info(sample_wav, verbose=True)
        captured = capsys.readouterr()
        assert "Details" in captured.out
