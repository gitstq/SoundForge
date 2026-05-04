"""
Audio analyzer module for SoundForge.

Provides audio file analysis, metadata extraction, format detection,
and loudness calculation using only Python standard library.
"""

import os
import struct
import wave
from typing import Any, Dict, Optional, Tuple

from .exceptions import AudioFileNotFoundError, InvalidAudioError
from .utils import (
    calculate_peak,
    calculate_rms,
    color_text,
    format_duration,
    format_sample_rate,
    format_size,
    linear_to_db,
)


# Magic bytes for common audio formats
_MAGIC_BYTES: Dict[str, bytes] = {
    "wav": b"RIFF",
    "flac": b"fLaC",
    "ogg": b"OggS",
    "mp3_id3": b"ID3",
    "mp3_sync": b"\xff\xfb",
    "mp3_sync2": b"\xff\xf3",
    "mp3_sync3": b"\xff\xf2",
    "aac": b"\xff\xf1",
    "aac2": b"\xff\xf9",
    "aiff": b"FORM",
    "m4a": b"\x00\x00\x00\x20\x66\x74\x79\x70",
}


class AudioAnalyzer:
    """Audio file analyzer using Python standard library.

    Supports WAV natively and can detect format from magic bytes
    for other audio file types.
    """

    def __init__(self) -> None:
        """Initialize the AudioAnalyzer."""
        pass

    @staticmethod
    def detect_format(filepath: str) -> str:
        """Detect audio format from file header magic bytes.

        Args:
            filepath: Path to the audio file.

        Returns:
            Format string (e.g., 'wav', 'mp3', 'flac', 'ogg', 'aac', 'unknown').

        Raises:
            AudioFileNotFoundError: If file does not exist.
        """
        if not os.path.isfile(filepath):
            raise AudioFileNotFoundError(filepath)

        try:
            with open(filepath, "rb") as f:
                header = f.read(12)
        except IOError as e:
            raise InvalidAudioError(filepath, str(e))

        if len(header) < 4:
            raise InvalidAudioError(filepath, "File too small to identify")

        # Check WAV (RIFF....WAVE)
        if header[:4] == b"RIFF" and header[8:12] == b"WAVE":
            return "wav"

        # Check FLAC
        if header[:4] == b"fLaC":
            return "flac"

        # Check OGG
        if header[:4] == b"OggS":
            return "ogg"

        # Check MP3 (ID3 tag or sync word)
        if header[:3] == b"ID3":
            return "mp3"
        if header[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"):
            return "mp3"

        # Check AAC
        if header[:2] in (b"\xff\xf1", b"\xff\xf9"):
            return "aac"

        # Check AIFF
        if header[:4] == b"FORM":
            return "aiff"

        # Check M4A/AAC container
        if len(header) >= 8 and header[:4] == b"\x00\x00\x00" and header[4:8] == b"ftyp":
            return "m4a"

        # Fallback: check file extension
        ext = os.path.splitext(filepath)[1].lower().lstrip(".")
        if ext in ("wav", "mp3", "flac", "ogg", "aac", "m4a", "aiff", "wma"):
            return ext

        return "unknown"

    def get_info(self, filepath: str) -> Dict[str, Any]:
        """Get comprehensive audio file information.

        Args:
            filepath: Path to the audio file.

        Returns:
            Dictionary containing audio metadata.

        Raises:
            AudioFileNotFoundError: If file does not exist.
            InvalidAudioError: If file is not a valid audio file.
        """
        if not os.path.isfile(filepath):
            raise AudioFileNotFoundError(filepath)

        file_size = os.path.getsize(filepath)
        fmt = self.detect_format(filepath)
        info: Dict[str, Any] = {
            "filepath": filepath,
            "filename": os.path.basename(filepath),
            "format": fmt,
            "file_size": file_size,
            "file_size_str": format_size(file_size),
        }

        if fmt == "wav":
            wav_info = self._get_wav_info(filepath)
            info.update(wav_info)
        else:
            # For non-WAV formats, we can only provide basic info
            # unless ffmpeg is available
            info["duration"] = None
            info["sample_rate"] = None
            info["channels"] = None
            info["bit_depth"] = None
            info["bitrate"] = None

            # Try to get more info via ffmpeg
            ffmpeg_info = self._get_ffmpeg_info(filepath)
            if ffmpeg_info:
                info.update(ffmpeg_info)

        return info

    @staticmethod
    def _get_wav_info(filepath: str) -> Dict[str, Any]:
        """Extract detailed WAV file information.

        Args:
            filepath: Path to the WAV file.

        Returns:
            Dictionary with WAV-specific metadata.
        """
        try:
            with wave.open(filepath, "rb") as wf:
                n_frames = wf.getnframes()
                sample_rate = wf.getframerate()
                channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                duration = n_frames / sample_rate if sample_rate > 0 else 0
                bitrate = sample_rate * channels * sample_width * 8

                return {
                    "duration": duration,
                    "duration_str": format_duration(duration),
                    "sample_rate": sample_rate,
                    "sample_rate_str": format_sample_rate(sample_rate),
                    "channels": channels,
                    "channels_str": "Mono" if channels == 1 else f"Stereo ({channels}ch)" if channels == 2 else f"{channels} channels",
                    "bit_depth": sample_width * 8,
                    "bitrate": bitrate,
                    "bitrate_str": f"{bitrate / 1000:.0f} kbps",
                    "n_frames": n_frames,
                    "compression": wf.getcomptype() or "PCM (uncompressed)",
                }
        except (wave.Error, EOFError) as e:
            raise InvalidAudioError(filepath, str(e))

    @staticmethod
    def _get_ffmpeg_info(filepath: str) -> Optional[Dict[str, Any]]:
        """Try to get audio info using ffmpeg.

        Args:
            filepath: Path to the audio file.

        Returns:
            Dictionary with audio metadata, or None if ffmpeg is unavailable.
        """
        import subprocess
        import json as json_module

        from .utils import get_ffmpeg_path

        ffmpeg_path = get_ffmpeg_path()
        if not ffmpeg_path:
            return None

        ffprobe_path = shutil_which_ffprobe(ffmpeg_path)
        if not ffprobe_path:
            return None

        try:
            result = subprocess.run(
                [
                    ffprobe_path,
                    "-v", "quiet",
                    "-print_format", "json",
                    "-show_format",
                    "-show_streams",
                    filepath,
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                return None

            data = json_module.loads(result.stdout)
            info: Dict[str, Any] = {}

            # Get format info
            fmt = data.get("format", {})
            if fmt.get("duration"):
                duration = float(fmt["duration"])
                info["duration"] = duration
                info["duration_str"] = format_duration(duration)
            if fmt.get("bit_rate"):
                bitrate = int(fmt["bit_rate"])
                info["bitrate"] = bitrate
                info["bitrate_str"] = f"{bitrate / 1000:.0f} kbps"

            # Get stream info
            streams = data.get("streams", [])
            for stream in streams:
                if stream.get("codec_type") == "audio":
                    if stream.get("sample_rate"):
                        sr = int(stream["sample_rate"])
                        info["sample_rate"] = sr
                        info["sample_rate_str"] = format_sample_rate(sr)
                    if stream.get("channels"):
                        ch = int(stream["channels"])
                        info["channels"] = ch
                        info["channels_str"] = "Mono" if ch == 1 else f"Stereo ({ch}ch)" if ch == 2 else f"{ch} channels"
                    if stream.get("bits_per_sample"):
                        info["bit_depth"] = int(stream["bits_per_sample"])
                    break

            return info if info else None

        except (subprocess.TimeoutExpired, json_module.JSONDecodeError, KeyError, ValueError):
            return None

    def calculate_loudness(self, filepath: str) -> Dict[str, float]:
        """Calculate loudness metrics for an audio file.

        Args:
            filepath: Path to the audio file (WAV format).

        Returns:
            Dictionary with loudness metrics (rms_db, peak_db, rms_linear, peak_linear).

        Raises:
            AudioFileNotFoundError: If file does not exist.
            InvalidAudioError: If file cannot be read.
        """
        if not os.path.isfile(filepath):
            raise AudioFileNotFoundError(filepath)

        fmt = self.detect_format(filepath)
        if fmt != "wav":
            return {
                "rms_db": float("-inf"),
                "peak_db": float("-inf"),
                "rms_linear": 0.0,
                "peak_linear": 0.0,
            }

        try:
            with wave.open(filepath, "rb") as wf:
                n_frames = wf.getnframes()
                sample_width = wf.getsampwidth()
                channels = wf.getnchannels()

                # Read all frames
                raw_data = wf.readframes(n_frames)

                # Convert to samples
                from .utils import bytes_to_samples

                samples = bytes_to_samples(raw_data, sample_width)

                # If stereo, take left channel only for simplicity
                if channels > 1:
                    samples = samples[::channels]

                rms = calculate_rms(samples)
                peak = calculate_peak(samples)

                return {
                    "rms_db": linear_to_db(rms) if rms > 0 else float("-inf"),
                    "peak_db": linear_to_db(peak) if peak > 0 else float("-inf"),
                    "rms_linear": rms,
                    "peak_linear": peak,
                }
        except (wave.Error, EOFError) as e:
            raise InvalidAudioError(filepath, str(e))

    def print_info(self, filepath: str, verbose: bool = False) -> None:
        """Pretty-print audio file information with colors.

        Args:
            filepath: Path to the audio file.
            verbose: If True, print additional details.
        """
        info = self.get_info(filepath)
        loudness = self.calculate_loudness(filepath)

        # Header
        print()
        print(color_text("=" * 60, "cyan"))
        print(color_text(f"  Audio File: {info['filename']}", "bold"))
        print(color_text("=" * 60, "cyan"))

        # Format and size
        print(f"  Format:       {color_text(info['format'].upper(), 'yellow')}")
        print(f"  File Size:    {info['file_size_str']}")

        # Duration
        if info.get("duration") is not None:
            print(f"  Duration:     {info['duration_str']}")
        else:
            print(f"  Duration:     {color_text('N/A (install ffmpeg for details)', 'dim')}")

        # Sample rate
        if info.get("sample_rate") is not None:
            print(f"  Sample Rate:  {info['sample_rate_str']}")
        else:
            print(f"  Sample Rate:  {color_text('N/A', 'dim')}")

        # Channels
        if info.get("channels") is not None:
            print(f"  Channels:     {info['channels_str']}")
        else:
            print(f"  Channels:     {color_text('N/A', 'dim')}")

        # Bit depth
        if info.get("bit_depth") is not None:
            print(f"  Bit Depth:    {info['bit_depth']} bit")
        else:
            print(f"  Bit Depth:    {color_text('N/A', 'dim')}")

        # Bitrate
        if info.get("bitrate") is not None:
            print(f"  Bitrate:      {info['bitrate_str']}")
        else:
            print(f"  Bitrate:      {color_text('N/A', 'dim')}")

        # Compression
        if info.get("compression"):
            print(f"  Compression:  {info['compression']}")

        # Loudness
        print()
        print(color_text("  Loudness:", "bold"))
        rms_db = loudness["rms_db"]
        peak_db = loudness["peak_db"]
        rms_color = "green" if -20 < rms_db < -6 else "yellow" if -30 < rms_db <= -20 else "red"
        peak_color = "green" if peak_db > -6 else "yellow" if peak_db > -12 else "red"
        print(f"  RMS Level:    {color_text(f'{rms_db:.1f} dB', rms_color)}")
        print(f"  Peak Level:   {color_text(f'{peak_db:.1f} dB', peak_color)}")

        # Verbose info
        if verbose:
            print()
            print(color_text("  Details:", "bold"))
            print(f"  File Path:    {info['filepath']}")
            if info.get("n_frames"):
                print(f"  Total Frames: {info['n_frames']:,}")

        print(color_text("=" * 60, "cyan"))
        print()


def shutil_which_ffprobe(ffmpeg_path: str) -> Optional[str]:
    """Try to find ffprobe based on ffmpeg path.

    Args:
        ffmpeg_path: Path to the ffmpeg executable.

    Returns:
        Path to ffprobe if found, None otherwise.
    """
    import shutil

    # Try same directory as ffmpeg
    ffmpeg_dir = os.path.dirname(ffmpeg_path)
    ffprobe_guess = os.path.join(ffmpeg_dir, "ffprobe") if ffmpeg_dir else "ffprobe"
    if shutil.which(ffprobe_guess):
        return ffprobe_guess
    if shutil.which("ffprobe"):
        return "ffprobe"
    return None
