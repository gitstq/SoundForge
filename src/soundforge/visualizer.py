"""
ASCII waveform and spectrum visualizer for SoundForge.

Provides terminal-based audio visualization using only Python standard library.
"""

import math
import wave
from typing import List, Optional, Tuple

from .exceptions import AudioFileNotFoundError, InvalidAudioError
from .utils import color_text


class AudioVisualizer:
    """ASCII-based audio visualizer.

    Generates waveform displays, frequency spectrum plots,
    and level meters directly in the terminal.
    """

    def __init__(self) -> None:
        """Initialize the AudioVisualizer."""
        pass

    def waveform(
        self,
        filepath: str,
        width: int = 80,
        height: int = 20,
        channels: int = 0,
    ) -> str:
        """Generate ASCII waveform visualization.

        Args:
            filepath: Path to the WAV file.
            width: Width of the waveform in characters.
            height: Height of the waveform in characters.
            channels: Number of channels to display (0 = all, 1 = mono mix).

        Returns:
            Multi-line string containing the ASCII waveform.

        Raises:
            AudioFileNotFoundError: If file does not exist.
            InvalidAudioError: If file cannot be read.
        """
        if not filepath or not hasattr(filepath, '__len__'):
            raise InvalidAudioError(str(filepath), "Invalid filepath")

        import os
        if not os.path.isfile(filepath):
            raise AudioFileNotFoundError(filepath)

        try:
            with wave.open(filepath, "rb") as wf:
                n_frames = wf.getnframes()
                sample_rate = wf.getframerate()
                sample_width = wf.getsampwidth()
                n_channels = wf.getnchannels()

                # Read all frames
                raw_data = wf.readframes(n_frames)
        except (wave.Error, EOFError) as e:
            raise InvalidAudioError(filepath, str(e))

        from .utils import bytes_to_samples

        samples = bytes_to_samples(raw_data, sample_width)

        # Mix to mono if requested
        if channels == 1 and n_channels > 1:
            mixed = []
            for i in range(0, len(samples) - n_channels + 1, n_channels):
                avg = sum(samples[i : i + n_channels]) / n_channels
                mixed.append(avg)
            samples = mixed

        # Downsample to fit width
        if len(samples) > width * 2:
            step = len(samples) / width
            downsampled = []
            for i in range(width):
                idx = int(i * step)
                end_idx = min(int((i + 1) * step), len(samples))
                chunk = samples[idx:end_idx]
                if chunk:
                    # Use peak of chunk for better visualization
                    downsampled.append(max(abs(s) for s in chunk))
                else:
                    downsampled.append(0)
        else:
            downsampled = [abs(s) for s in samples]

        # Normalize
        max_val = max(downsampled) if downsampled else 1.0
        if max_val == 0:
            max_val = 1.0
        normalized = [v / max_val for v in downsampled]

        # Build waveform
        mid = height // 2
        lines = []
        for row in range(height):
            line = ""
            for col in range(min(width, len(normalized))):
                val = normalized[col]
                bar_height = int(val * mid)
                if row == mid:
                    line += color_text("-", "dim")
                elif row < mid and (mid - row) <= bar_height:
                    # Upper half - filled
                    intensity = min(255, int((mid - row) / mid * 255))
                    if intensity > 200:
                        line += color_text("|", "bright_red")
                    elif intensity > 140:
                        line += color_text("|", "yellow")
                    else:
                        line += color_text("|", "green")
                elif row > mid and (row - mid) <= bar_height:
                    # Lower half - filled
                    intensity = min(255, int((row - mid) / mid * 255))
                    if intensity > 200:
                        line += color_text("|", "bright_red")
                    elif intensity > 140:
                        line += color_text("|", "yellow")
                    else:
                        line += color_text("|", "green")
                else:
                    line += " "
            lines.append(line)

        # Add info header
        duration = n_frames / sample_rate if sample_rate > 0 else 0
        header = (
            f"  Waveform: {filepath}\n"
            f"  Duration: {duration:.2f}s | "
            f"Sample Rate: {sample_rate}Hz | "
            f"Channels: {n_channels} | "
            f"Bits: {sample_width * 8}\n"
        )
        return header + "\n".join(lines)

    def spectrum(
        self,
        filepath: str,
        width: int = 80,
        height: int = 20,
    ) -> str:
        """Generate ASCII frequency spectrum visualization using DFT.

        Uses a simple Discrete Fourier Transform on a chunk of audio data
        to generate a frequency spectrum display.

        Args:
            filepath: Path to the WAV file.
            width: Width of the spectrum in characters.
            height: Height of the spectrum in characters.

        Returns:
            Multi-line string containing the ASCII spectrum.

        Raises:
            AudioFileNotFoundError: If file does not exist.
            InvalidAudioError: If file cannot be read.
        """
        import os
        if not os.path.isfile(filepath):
            raise AudioFileNotFoundError(filepath)

        try:
            with wave.open(filepath, "rb") as wf:
                n_frames = wf.getnframes()
                sample_rate = wf.getframerate()
                sample_width = wf.getsampwidth()
                n_channels = wf.getnchannels()

                # Read a chunk (up to 8192 samples for DFT)
                chunk_size = min(n_frames, 8192)
                raw_data = wf.readframes(chunk_size)
        except (wave.Error, EOFError) as e:
            raise InvalidAudioError(filepath, str(e))

        from .utils import bytes_to_samples

        samples = bytes_to_samples(raw_data, sample_width)

        # Mix to mono
        if n_channels > 1:
            mixed = []
            for i in range(0, len(samples) - n_channels + 1, n_channels):
                avg = sum(samples[i : i + n_channels]) / n_channels
                mixed.append(avg)
            samples = mixed

        # Apply simple window function (Hann)
        windowed = []
        n = len(samples)
        for i in range(n):
            w = 0.5 * (1 - math.cos(2 * math.pi * i / n))
            windowed.append(samples[i] * w)

        # Compute DFT magnitudes (only first half - positive frequencies)
        num_bins = min(width, n // 2)
        magnitudes = []
        for k in range(num_bins):
            real = 0.0
            imag = 0.0
            for i in range(n):
                angle = 2 * math.pi * k * i / n
                real += windowed[i] * math.cos(angle)
                imag -= windowed[i] * math.sin(angle)
            mag = math.sqrt(real * real + imag * imag) / n
            magnitudes.append(mag)

        # Convert to dB scale
        max_mag = max(magnitudes) if magnitudes else 1.0
        if max_mag == 0:
            max_mag = 1.0
        db_values = []
        for m in magnitudes:
            if m > 0:
                db = 20 * math.log10(m / max_mag)
            else:
                db = -60
            db_values.append(max(-60, db))

        # Build spectrum display (bars from bottom)
        lines = []
        for row in range(height - 1, -1, -1):
            line = ""
            threshold = -60 + (60 * row / height)
            for col in range(len(db_values)):
                if db_values[col] >= threshold:
                    # Color based on level
                    level = (db_values[col] + 60) / 60
                    if level > 0.8:
                        line += color_text("#", "bright_red")
                    elif level > 0.6:
                        line += color_text("#", "red")
                    elif level > 0.4:
                        line += color_text("#", "yellow")
                    elif level > 0.2:
                        line += color_text("#", "green")
                    else:
                        line += color_text("#", "dim")
                else:
                    line += " "
            lines.append(line)

        # Frequency labels
        freq_per_bin = sample_rate / (2 * num_bins)
        freq_labels = []
        for i in range(0, num_bins, max(1, num_bins // 8)):
            freq = i * freq_per_bin
            if freq >= 1000:
                freq_labels.append(f"{freq / 1000:.1f}k")
            else:
                freq_labels.append(f"{freq:.0f}")

        freq_line = " " * 2
        step = max(1, num_bins // len(freq_labels))
        for i, label in enumerate(freq_labels):
            pos = i * step
            if pos < width:
                freq_line += f"{label:^{step}}"

        header = (
            f"  Spectrum: {filepath}\n"
            f"  Sample Rate: {sample_rate}Hz | "
            f"FFT Size: {n} | "
            f"Bins: {num_bins}\n"
        )
        return header + "\n".join(lines) + "\n" + freq_line

    def level_meter(self, samples: List[float], width: int = 50) -> str:
        """Generate a level meter bar from audio samples.

        Args:
            samples: List of float sample values (-1.0 to 1.0).
            width: Width of the level meter.

        Returns:
            String containing the level meter.
        """
        if not samples:
            return " " * width

        peak = max(abs(s) for s in samples)
        db = 20 * math.log10(peak) if peak > 0 else -60
        normalized = max(0, min(1, (db + 60) / 60))
        filled = int(normalized * width)

        bar = ""
        for i in range(width):
            if i < filled:
                ratio = i / width
                if ratio > 0.9:
                    bar += color_text("#", "bright_red")
                elif ratio > 0.75:
                    bar += color_text("#", "red")
                elif ratio > 0.5:
                    bar += color_text("#", "yellow")
                else:
                    bar += color_text("#", "green")
            else:
                bar += " "

        return f"[{bar}] {db:.1f} dB"

    def print_waveform(self, filepath: str, width: int = 80, height: int = 20) -> None:
        """Print waveform visualization to terminal.

        Args:
            filepath: Path to the WAV file.
            width: Width of the waveform.
            height: Height of the waveform.
        """
        print(self.waveform(filepath, width, height))

    def print_spectrum(self, filepath: str, width: int = 80, height: int = 20) -> None:
        """Print spectrum visualization to terminal.

        Args:
            filepath: Path to the WAV file.
            width: Width of the spectrum.
            height: Height of the spectrum.
        """
        print(self.spectrum(filepath, width, height))
