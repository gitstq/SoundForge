"""
Audio format converter module for SoundForge.

Supports WAV processing using Python's built-in wave module.
Non-WAV format conversion uses ffmpeg as an optional backend.
"""

import os
import wave
from typing import Optional, Tuple

from .exceptions import (
    AudioFileNotFoundError,
    AudioProcessingError,
    FFmpegNotFoundError,
    FormatNotSupportedError,
    InvalidAudioError,
)
from .utils import (
    ProgressBar,
    bytes_to_samples,
    check_ffmpeg,
    color_text,
    ensure_dir,
    run_ffmpeg,
    samples_to_bytes,
)


# Supported formats and their ffmpeg codec mapping
_FORMAT_CODECS = {
    "mp3": {"codec": "libmp3lame", "extension": ".mp3"},
    "flac": {"codec": "flac", "extension": ".flac"},
    "ogg": {"codec": "libvorbis", "extension": ".ogg"},
    "aac": {"codec": "aac", "extension": ".aac"},
    "m4a": {"codec": "aac", "extension": ".m4a"},
    "wma": {"codec": "wmav2", "extension": ".wma"},
    "opus": {"codec": "libopus", "extension": ".opus"},
}

# Quality presets for different formats
_QUALITY_PRESETS = {
    "mp3": {
        "low": ["-b:a", "128k"],
        "medium": ["-b:a", "192k"],
        "high": ["-b:a", "256k"],
        "very_high": ["-b:a", "320k"],
    },
    "flac": {
        "low": ["-compression_level", "8"],
        "medium": ["-compression_level", "5"],
        "high": ["-compression_level", "3"],
        "very_high": ["-compression_level", "0"],
    },
    "ogg": {
        "low": ["-b:a", "128k"],
        "medium": ["-b:a", "192k"],
        "high": ["-b:a", "256k"],
        "very_high": ["-b:a", "320k"],
    },
    "aac": {
        "low": ["-b:a", "128k"],
        "medium": ["-b:a", "192k"],
        "high": ["-b:a", "256k"],
        "very_high": ["-b:a", "320k"],
    },
}


class AudioConverter:
    """Audio format converter.

    Supports WAV natively and other formats via ffmpeg.
    """

    def __init__(self) -> None:
        """Initialize the AudioConverter."""
        self._ffmpeg_available = check_ffmpeg()

    @property
    def ffmpeg_available(self) -> bool:
        """Check if ffmpeg is available."""
        return self._ffmpeg_available

    def convert(
        self,
        input_path: str,
        output_path: str,
        quality: str = "medium",
        sample_rate: Optional[int] = None,
        channels: Optional[int] = None,
        verbose: bool = False,
    ) -> str:
        """Convert an audio file to a different format.

        Args:
            input_path: Path to the input audio file.
            output_path: Path for the output file.
            quality: Quality preset ('low', 'medium', 'high', 'very_high').
            sample_rate: Target sample rate (None = keep original).
            channels: Target channel count (None = keep original).
            verbose: If True, print detailed progress.

        Returns:
            Path to the converted file.

        Raises:
            AudioFileNotFoundError: If input file does not exist.
            FormatNotSupportedError: If output format is not supported.
            FFmpegNotFoundError: If ffmpeg is needed but not installed.
            AudioProcessingError: If conversion fails.
        """
        if not os.path.isfile(input_path):
            raise AudioFileNotFoundError(input_path)

        # Determine output format
        output_ext = os.path.splitext(output_path)[1].lower().lstrip(".")
        if not output_ext:
            raise FormatNotSupportedError("(no extension)")

        ensure_dir(output_path)

        # WAV to WAV conversion (native)
        if output_ext == "wav":
            return self._convert_wav_native(
                input_path, output_path, sample_rate, channels, verbose
            )

        # Non-WAV conversion requires ffmpeg
        if not self._ffmpeg_available:
            raise FFmpegNotFoundError()

        if output_ext not in _FORMAT_CODECS:
            raise FormatNotSupportedError(output_ext)

        return self._convert_ffmpeg(
            input_path, output_path, output_ext, quality, sample_rate, channels, verbose
        )

    def _convert_wav_native(
        self,
        input_path: str,
        output_path: str,
        sample_rate: Optional[int],
        channels: Optional[int],
        verbose: bool,
    ) -> str:
        """Convert to WAV using Python's wave module.

        Args:
            input_path: Input file path.
            output_path: Output file path.
            sample_rate: Target sample rate.
            channels: Target channel count.
            verbose: Verbose output.

        Returns:
            Output file path.
        """
        try:
            with wave.open(input_path, "rb") as wf_in:
                params = wf_in.getparams()
                n_frames = wf_in.getnframes()
                raw_data = wf_in.readframes(n_frames)

            # Adjust parameters
            sampwidth = params.sampwidth
            if sample_rate is None:
                frate = params.framerate
            else:
                frate = sample_rate
            if channels is None:
                nch = params.nchannels
            else:
                nch = channels

            # Convert samples for potential resampling
            from .utils import bytes_to_samples, samples_to_bytes

            samples = bytes_to_samples(raw_data, params.sampwidth)

            # Channel conversion
            if nch != params.nchannels and params.nchannels > 1:
                if nch == 1:
                    # Mix to mono
                    mixed = []
                    for i in range(0, len(samples) - params.nchannels + 1, params.nchannels):
                        avg = sum(samples[i : i + params.nchannels]) / params.nchannels
                        mixed.append(avg)
                    samples = mixed
                elif nch == 2 and params.nchannels == 1:
                    # Duplicate to stereo
                    new_samples = []
                    for s in samples:
                        new_samples.extend([s, s])
                    samples = new_samples

            # Simple resampling if needed
            if sample_rate is not None and sample_rate != params.framerate:
                ratio = params.framerate / sample_rate
                new_len = int(len(samples) / ratio)
                resampled = []
                for i in range(new_len):
                    idx = int(i * ratio)
                    if idx < len(samples):
                        resampled.append(samples[idx])
                samples = resampled
                frate = sample_rate

            raw_out = samples_to_bytes(samples, sampwidth)

            with wave.open(output_path, "wb") as wf_out:
                wf_out.setnchannels(nch)
                wf_out.setsampwidth(sampwidth)
                wf_out.setframerate(frate)
                wf_out.writeframes(raw_out)

            if verbose:
                print(f"  Converted: {input_path} -> {output_path}")

            return output_path

        except (wave.Error, EOFError) as e:
            raise InvalidAudioError(input_path, str(e))

    def _convert_ffmpeg(
        self,
        input_path: str,
        output_path: str,
        output_format: str,
        quality: str,
        sample_rate: Optional[int],
        channels: Optional[int],
        verbose: bool,
    ) -> str:
        """Convert audio using ffmpeg.

        Args:
            input_path: Input file path.
            output_path: Output file path.
            output_format: Target format string.
            quality: Quality preset.
            sample_rate: Target sample rate.
            channels: Target channel count.
            verbose: Verbose output.

        Returns:
            Output file path.
        """
        fmt_info = _FORMAT_CODECS[output_format]
        codec = fmt_info["codec"]

        # Build ffmpeg arguments
        args = []

        # Quality settings
        quality_args = _QUALITY_PRESETS.get(output_format, {}).get(quality, [])
        args.extend(quality_args)

        # Codec
        args.extend(["-c:a", codec])

        # Sample rate
        if sample_rate:
            args.extend(["-ar", str(sample_rate)])

        # Channels
        if channels:
            args.extend(["-ac", str(channels)])

        if verbose:
            args.append("-vinfo")

        run_ffmpeg(args, input_file=input_path, output_file=output_path)

        if verbose:
            print(f"  Converted: {input_path} -> {output_path}")

        return output_path

    def get_supported_formats(self) -> dict:
        """Get list of supported output formats.

        Returns:
            Dictionary mapping format names to info dicts.
        """
        formats = {"wav": {"codec": "PCM (built-in)", "extension": ".wav", "native": True}}
        if self._ffmpeg_available:
            formats.update(_FORMAT_CODECS)
        return formats

    def print_supported_formats(self) -> None:
        """Print supported formats to terminal."""
        formats = self.get_supported_formats()
        print()
        print(color_text("  Supported Output Formats:", "bold"))
        print()
        for name, info in sorted(formats.items()):
            native = info.get("native", False)
            codec = info["codec"]
            ext = info["extension"]
            if native:
                tag = color_text("[built-in]", "green")
            else:
                tag = color_text("[ffmpeg]", "yellow")
            print(f"    {name.upper():8s}  {ext:8s}  {codec:20s}  {tag}")
        print()
