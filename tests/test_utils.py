"""
Tests for the utility functions.
"""

import math
import os
import tempfile

import pytest

from soundforge.utils import (
    ProgressBar,
    bytes_to_samples,
    calculate_peak,
    calculate_rms,
    color_text,
    db_to_linear,
    ensure_dir,
    format_duration,
    format_sample_rate,
    format_size,
    linear_to_db,
    print_banner,
    progressbar,
    samples_to_bytes,
)


class TestFormatDuration:
    """Tests for format_duration function."""

    def test_zero(self):
        assert format_duration(0) == "00:00.000"

    def test_seconds_only(self):
        result = format_duration(5.5)
        assert "05" in result
        assert "500" in result

    def test_minutes(self):
        result = format_duration(125.0)
        assert "02" in result
        assert "05" in result

    def test_hours(self):
        result = format_duration(3661.5)
        assert "01" in result
        assert "01" in result
        assert "01" in result

    def test_negative(self):
        assert format_duration(-1) == "00:00:00.000"

    def test_fractional(self):
        result = format_duration(1.234)
        assert "01" in result
        assert "234" in result


class TestFormatSize:
    """Tests for format_size function."""

    def test_zero(self):
        assert format_size(0) == "0 B"

    def test_bytes(self):
        assert "B" in format_size(500)

    def test_kilobytes(self):
        result = format_size(2048)
        assert "KB" in result
        assert "2.00" in result

    def test_megabytes(self):
        result = format_size(1048576)
        assert "MB" in result
        assert "1.00" in result

    def test_gigabytes(self):
        result = format_size(1073741824)
        assert "GB" in result

    def test_negative(self):
        assert format_size(-1) == "0 B"


class TestFormatSampleRate:
    """Tests for format_sample_rate function."""

    def test_cd_quality(self):
        assert format_sample_rate(44100) == "44.1 kHz"

    def test_dvd_quality(self):
        assert format_sample_rate(48000) == "48.0 kHz"

    def test_high_rate(self):
        assert format_sample_rate(96000) == "96.0 kHz"


class TestColorText:
    """Tests for color_text function."""

    def test_basic_color(self):
        result = color_text("hello", "red")
        assert "hello" in result

    def test_unknown_color(self):
        result = color_text("hello", "nonexistent")
        assert "hello" in result


class TestDbConversion:
    """Tests for dB <-> linear conversion."""

    def test_db_to_linear_zero(self):
        assert abs(db_to_linear(0) - 1.0) < 1e-9

    def test_db_to_linear_negative(self):
        result = db_to_linear(-6)
        assert 0.4 < result < 0.6

    def test_db_to_linear_positive(self):
        result = db_to_linear(6)
        assert 1.5 < result < 2.5

    def test_linear_to_db_one(self):
        assert abs(linear_to_db(1.0)) < 1e-9

    def test_linear_to_db_zero(self):
        assert linear_to_db(0) == float("-inf")

    def test_roundtrip(self):
        for db in [-20, -10, -6, -3, 0, 3, 6]:
            linear = db_to_linear(db)
            recovered = linear_to_db(linear)
            assert abs(recovered - db) < 0.01


class TestRmsAndPeak:
    """Tests for RMS and peak calculation."""

    def test_rms_silence(self):
        assert calculate_rms([]) == 0.0
        assert calculate_rms([0, 0, 0]) == 0.0

    def test_rms_known_value(self):
        # RMS of [1, -1] should be 1.0
        assert abs(calculate_rms([1.0, -1.0]) - 1.0) < 1e-9

    def test_peak_silence(self):
        assert calculate_peak([]) == 0.0
        assert calculate_peak([0, 0, 0]) == 0.0

    def test_peak_known_value(self):
        assert calculate_peak([0.5, -0.8, 0.3]) == 0.8


class TestSampleConversion:
    """Tests for bytes <-> samples conversion."""

    def test_8bit_roundtrip(self):
        samples = [0.0, 0.5, -0.5, 1.0, -1.0]
        data = samples_to_bytes(samples, 1)
        recovered = bytes_to_samples(data, 1)
        for orig, rec in zip(samples, recovered):
            assert abs(orig - rec) < 0.02

    def test_16bit_roundtrip(self):
        samples = [0.0, 0.5, -0.5, 1.0, -1.0]
        data = samples_to_bytes(samples, 2)
        recovered = bytes_to_samples(data, 2)
        for orig, rec in zip(samples, recovered):
            assert abs(orig - rec) < 0.001

    def test_32bit_roundtrip(self):
        samples = [0.0, 0.5, -0.5, 0.123, -0.456]
        data = samples_to_bytes(samples, 4)
        recovered = bytes_to_samples(data, 4)
        for orig, rec in zip(samples, recovered):
            assert abs(orig - rec) < 0.0001

    def test_empty_samples(self):
        data = samples_to_bytes([], 2)
        assert data == b""
        recovered = bytes_to_samples(data, 2)
        assert recovered == []

    def test_invalid_sample_width(self):
        with pytest.raises(ValueError):
            bytes_to_samples(b"\x00", 5)
        with pytest.raises(ValueError):
            samples_to_bytes([0.0], 5)


class TestEnsureDir:
    """Tests for ensure_dir function."""

    def test_existing_dir(self, tmp_path):
        result = ensure_dir(str(tmp_path / "test.wav"))
        assert result == str(tmp_path / "test.wav")

    def test_creates_dir(self, tmp_path):
        nested = str(tmp_path / "a" / "b" / "c" / "test.wav")
        ensure_dir(nested)
        assert os.path.isdir(os.path.dirname(nested))


class TestProgressBar:
    """Tests for ProgressBar class."""

    def test_basic_progress(self, capsys):
        bar = ProgressBar(total=10, width=20)
        for i in range(10):
            bar.update(i + 1)
        captured = capsys.readouterr()
        assert "100.0%" in captured.out

    def test_finish(self, capsys):
        bar = ProgressBar(total=100, width=20)
        bar.finish()
        captured = capsys.readouterr()
        assert "100.0%" in captured.out


class TestPrintBanner:
    """Tests for print_banner function."""

    def test_banner_prints(self, capsys):
        print_banner()
        captured = capsys.readouterr()
        assert "Lightweight" in captured.out or "Toolbox" in captured.out
