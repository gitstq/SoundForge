"""
Shared utilities for SoundForge.

Provides formatting helpers, ANSI color output, ffmpeg detection,
and other common utilities used across modules.
"""

import math
import os
import shutil
import subprocess
import sys
import time
from typing import Optional


# ---------------------------------------------------------------------------
# ANSI Color Support
# ---------------------------------------------------------------------------

# ANSI escape code mapping
_COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "underline": "\033[4m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_white": "\033[97m",
}

# Check if colors should be disabled (e.g., piping to file or NO_COLOR env)
_NO_COLOR = os.environ.get("NO_COLOR", "") != "" or not sys.stdout.isatty()


def color_text(text: str, color: str) -> str:
    """Wrap text with ANSI color codes.

    Args:
        text: The text to colorize.
        color: Color name from _COLORS dict (e.g., 'red', 'green', 'bold').

    Returns:
        Colorized text string, or plain text if colors are disabled.
    """
    if _NO_COLOR:
        return text
    code = _COLORS.get(color, "")
    reset = _COLORS.get("reset", "")
    return f"{code}{text}{reset}"


def style_text(text: str, *styles: str) -> str:
    """Apply multiple styles to text.

    Args:
        text: The text to style.
        *styles: Style names to apply (e.g., 'bold', 'red').

    Returns:
        Styled text string.
    """
    if _NO_COLOR:
        return text
    codes = "".join(_COLORS.get(s, "") for s in styles)
    reset = _COLORS.get("reset", "")
    return f"{codes}{text}{reset}"


# ---------------------------------------------------------------------------
# Formatting Utilities
# ---------------------------------------------------------------------------

def format_duration(seconds: float) -> str:
    """Format seconds to HH:MM:SS.mmm string.

    Args:
        seconds: Duration in seconds (can be float).

    Returns:
        Formatted duration string.
    """
    if seconds < 0:
        return "00:00:00.000"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    return f"{minutes:02d}:{secs:06.3f}"


def format_size(num_bytes: int) -> str:
    """Format bytes to human-readable size string.

    Args:
        num_bytes: Number of bytes.

    Returns:
        Human-readable size string (e.g., '1.5 MB').
    """
    if num_bytes < 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    if num_bytes == 0:
        return "0 B"
    exponent = min(int(math.log(num_bytes) / math.log(1024)), len(units) - 1)
    size = num_bytes / (1024 ** exponent)
    return f"{size:.2f} {units[exponent]}"


def format_sample_rate(rate: int) -> str:
    """Format sample rate with kHz suffix.

    Args:
        rate: Sample rate in Hz.

    Returns:
        Formatted string (e.g., '44.1 kHz').
    """
    return f"{rate / 1000:.1f} kHz"


# ---------------------------------------------------------------------------
# Progress Bar
# ---------------------------------------------------------------------------

class ProgressBar:
    """A simple terminal progress bar.

    Args:
        total: Total items or bytes.
        width: Width of the progress bar in characters.
        prefix: Text to show before the bar.
        suffix: Text to show after the bar.
        fill_char: Character used to fill the progress bar.
        empty_char: Character used for empty portion.
    """

    def __init__(
        self,
        total: int = 100,
        width: int = 50,
        prefix: str = "",
        suffix: str = "",
        fill_char: str = "=",
        empty_char: str = "-",
    ) -> None:
        self.total = total
        self.width = width
        self.prefix = prefix
        self.suffix = suffix
        self.fill_char = fill_char
        self.empty_char = empty_char
        self._current = 0
        self._start_time = time.time()

    def update(self, current: Optional[int] = None) -> None:
        """Update the progress bar display.

        Args:
            current: Current progress value. If None, increments by 1.
        """
        if current is not None:
            self._current = current
        else:
            self._current += 1

        if self.total <= 0:
            return

        progress = min(self._current / self.total, 1.0)
        filled = int(self.width * progress)
        bar = self.fill_char * filled + self.empty_char * (self.width - filled)
        percent = progress * 100

        # Calculate elapsed time and ETA
        elapsed = time.time() - self._start_time
        if progress > 0:
            eta = elapsed / progress - elapsed
            eta_str = format_duration(eta)
        else:
            eta_str = "--:--"

        line = f"\r{self.prefix}|{bar}| {percent:5.1f}% {self.suffix} ETA: {eta_str}"
        sys.stdout.write(line)
        sys.stdout.flush()

        if progress >= 1.0:
            sys.stdout.write("\n")
            sys.stdout.flush()

    def finish(self) -> None:
        """Force the progress bar to complete."""
        self.update(self.total)


def progressbar(current: int, total: int, width: int = 50, prefix: str = "") -> None:
    """Simple one-shot progress bar (convenience function).

    Args:
        current: Current progress value.
        total: Total value.
        width: Bar width in characters.
        prefix: Optional prefix text.
    """
    if total <= 0:
        return
    progress = min(current / total, 1.0)
    filled = int(width * progress)
    bar = "=" * filled + "-" * (width - filled)
    percent = progress * 100
    sys.stdout.write(f"\r{prefix}|{bar}| {percent:5.1f}%")
    sys.stdout.flush()
    if progress >= 1.0:
        sys.stdout.write("\n")
        sys.stdout.flush()


# ---------------------------------------------------------------------------
# File & System Utilities
# ---------------------------------------------------------------------------

def ensure_dir(filepath: str) -> str:
    """Ensure the directory for a file path exists.

    Args:
        filepath: Path to a file.

    Returns:
        The same filepath (for chaining).
    """
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    return filepath


def check_ffmpeg() -> bool:
    """Check if ffmpeg is available on the system.

    Returns:
        True if ffmpeg is found in PATH, False otherwise.
    """
    return shutil.which("ffmpeg") is not None


def get_ffmpeg_path() -> Optional[str]:
    """Get the path to ffmpeg executable.

    Returns:
        Path to ffmpeg if found, None otherwise.
    """
    return shutil.which("ffmpeg")


def run_ffmpeg(args: list, input_file: str = "", output_file: str = "") -> subprocess.CompletedProcess:
    """Run an ffmpeg command.

    Args:
        args: List of ffmpeg arguments (without the 'ffmpeg' command itself).
        input_file: Optional input file path (adds -i flag).
        output_file: Optional output file path (appended to args).

    Returns:
        CompletedProcess instance.

    Raises:
        FFmpegNotFoundError: If ffmpeg is not installed.
        AudioProcessingError: If ffmpeg command fails.
    """
    from .exceptions import FFmpegNotFoundError, AudioProcessingError

    ffmpeg_path = get_ffmpeg_path()
    if not ffmpeg_path:
        raise FFmpegNotFoundError()

    cmd = [ffmpeg_path, "-y"]  # -y to overwrite output
    if input_file:
        cmd.extend(["-i", input_file])
    cmd.extend(args)
    if output_file:
        cmd.append(output_file)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )
        if result.returncode != 0:
            raise AudioProcessingError(
                operation="ffmpeg",
                reason=result.stderr.strip()[-200:] if result.stderr else "Unknown error",
            )
        return result
    except subprocess.TimeoutExpired:
        raise AudioProcessingError(
            operation="ffmpeg",
            reason="Operation timed out (300s limit)",
        )


# ---------------------------------------------------------------------------
# Audio Utilities
# ---------------------------------------------------------------------------

def db_to_linear(db: float) -> float:
    """Convert decibels to linear amplitude scale.

    Args:
        db: Value in decibels.

    Returns:
        Linear amplitude value.
    """
    return 10.0 ** (db / 20.0)


def linear_to_db(linear: float) -> float:
    """Convert linear amplitude to decibels.

    Args:
        linear: Linear amplitude value.

    Returns:
        Value in decibels.
    """
    if linear <= 0:
        return -float("inf")
    return 20.0 * math.log10(linear)


def calculate_rms(samples: list) -> float:
    """Calculate the Root Mean Square of audio samples.

    Args:
        samples: List of audio sample values (float, -1.0 to 1.0).

    Returns:
        RMS value.
    """
    if not samples:
        return 0.0
    return math.sqrt(sum(s * s for s in samples) / len(samples))


def calculate_peak(samples: list) -> float:
    """Calculate the peak amplitude of audio samples.

    Args:
        samples: List of audio sample values (float, -1.0 to 1.0).

    Returns:
        Peak absolute amplitude value.
    """
    if not samples:
        return 0.0
    return max(abs(s) for s in samples)


# ---------------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------------

_BANNER = r"""
    ____              __  __
   / __ \__  ______  / /_/ /_  ____  ____  _____
  / /_/ / / / / __ \/ __/ __ \/ __ \/ __ \/ ___/
 / _, _/ /_/ / / / / /_/ / / / /_/ / / / (__  )
/_/ |_|\__,_/_/ /_/\__/_/ /_/\____/_/ /_/____/

  Lightweight Terminal Audio Processing Toolbox
  Version {version}
"""

def print_banner() -> None:
    """Print the SoundForge ASCII art banner."""
    print(color_text(_BANNER.format(version=__import__("soundforge").__version__), "cyan"))


# ---------------------------------------------------------------------------
# Sample format conversion
# ---------------------------------------------------------------------------

def bytes_to_samples(data: bytes, sample_width: int) -> list:
    """Convert raw bytes to a list of float samples (-1.0 to 1.0).

    Args:
        data: Raw audio bytes.
        sample_width: Bytes per sample (1, 2, 3, or 4).

    Returns:
        List of float sample values normalized to [-1.0, 1.0].
    """
    import struct

    samples = []
    if sample_width == 1:
        # 8-bit unsigned
        for b in data:
            samples.append((b - 128) / 128.0)
    elif sample_width == 2:
        # 16-bit signed
        fmt = f"<{len(data) // 2}h"
        for val in struct.unpack(fmt, data):
            samples.append(val / 32768.0)
    elif sample_width == 3:
        # 24-bit signed
        for i in range(0, len(data), 3):
            b = data[i : i + 3]
            val = int.from_bytes(b, byteorder="little", signed=True)
            samples.append(val / 8388608.0)
    elif sample_width == 4:
        # 32-bit signed
        fmt = f"<{len(data) // 4}i"
        for val in struct.unpack(fmt, data):
            samples.append(val / 2147483648.0)
    else:
        raise ValueError(f"Unsupported sample width: {sample_width}")
    return samples


def samples_to_bytes(samples: list, sample_width: int) -> bytes:
    """Convert a list of float samples to raw bytes.

    Args:
        samples: List of float sample values (-1.0 to 1.0).
        sample_width: Bytes per sample (1, 2, or 4).

    Returns:
        Raw audio bytes.
    """
    import struct

    if sample_width == 1:
        # 8-bit unsigned
        result = bytearray()
        for s in samples:
            val = max(0, min(255, int(s * 128 + 128)))
            result.append(val)
        return bytes(result)
    elif sample_width == 2:
        # 16-bit signed
        values = []
        for s in samples:
            val = max(-32768, min(32767, int(s * 32767)))
            values.append(val)
        return struct.pack(f"<{len(values)}h", *values)
    elif sample_width == 4:
        # 32-bit signed
        values = []
        for s in samples:
            val = max(-2147483648, min(2147483647, int(s * 2147483647)))
            values.append(val)
        return struct.pack(f"<{len(values)}i", *values)
    else:
        raise ValueError(f"Unsupported sample width: {sample_width}")
