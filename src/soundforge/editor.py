"""
Audio editor module for SoundForge.

Provides audio editing operations: trimming, splitting, concatenation,
fade effects, normalization, and gain adjustment.
All operations use Python's built-in wave module for WAV files.
"""

import os
import wave
from typing import List, Optional

from .exceptions import (
    AudioFileNotFoundError,
    AudioProcessingError,
    InvalidAudioError,
)
from .utils import (
    ProgressBar,
    bytes_to_samples,
    color_text,
    db_to_linear,
    ensure_dir,
    format_duration,
    linear_to_db,
    samples_to_bytes,
)


class AudioEditor:
    """Audio editor for WAV files.

    Provides trim, split, concatenate, fade, normalize, and gain operations.
    All operations work on WAV files using Python's built-in wave module.
    """

    def __init__(self) -> None:
        """Initialize the AudioEditor."""
        pass

    @staticmethod
    def _read_wav(filepath: str) -> tuple:
        """Read a WAV file and return its parameters and sample data.

        Args:
            filepath: Path to the WAV file.

        Returns:
            Tuple of (params, samples_list, raw_data).

        Raises:
            AudioFileNotFoundError: If file does not exist.
            InvalidAudioError: If file is not valid WAV.
        """
        if not os.path.isfile(filepath):
            raise AudioFileNotFoundError(filepath)
        try:
            with wave.open(filepath, "rb") as wf:
                params = wf.getparams()
                n_frames = wf.getnframes()
                raw_data = wf.readframes(n_frames)
            samples = bytes_to_samples(raw_data, params.sampwidth)
            return params, samples, raw_data
        except (wave.Error, EOFError) as e:
            raise InvalidAudioError(filepath, str(e))

    @staticmethod
    def _write_wav(
        filepath: str,
        params: wave._wave_params,
        samples: list,
    ) -> str:
        """Write samples to a WAV file.

        Args:
            filepath: Output file path.
            params: Wave parameters (nchannels, sampwidth, framerate, etc.).
            samples: List of float samples.

        Returns:
            Output file path.
        """
        ensure_dir(filepath)
        raw_data = samples_to_bytes(samples, params.sampwidth)
        with wave.open(filepath, "wb") as wf:
            wf.setnchannels(params.nchannels)
            wf.setsampwidth(params.sampwidth)
            wf.setframerate(params.framerate)
            wf.setcomptype(params.comptype, params.compname)
            wf.writeframes(raw_data)
        return filepath

    def trim(
        self,
        input_path: str,
        output_path: str,
        start_sec: float = 0.0,
        end_sec: Optional[float] = None,
        verbose: bool = False,
    ) -> str:
        """Trim an audio file to a specified time range.

        Args:
            input_path: Path to the input WAV file.
            output_path: Path for the output file.
            start_sec: Start time in seconds.
            end_sec: End time in seconds (None = end of file).
            verbose: If True, print progress info.

        Returns:
            Path to the trimmed file.
        """
        params, samples, _ = self._read_wav(input_path)
        sample_rate = params.framerate
        n_channels = params.nchannels

        total_samples = len(samples)
        total_duration = total_samples / (sample_rate * n_channels)

        # Calculate sample indices
        start_sample = int(start_sec * sample_rate) * n_channels
        if end_sec is None:
            end_sample = total_samples
        else:
            end_sample = int(end_sec * sample_rate) * n_channels

        # Clamp values
        start_sample = max(0, min(start_sample, total_samples))
        end_sample = max(start_sample, min(end_sample, total_samples))

        trimmed = samples[start_sample:end_sample]

        if verbose:
            trim_duration = (end_sample - start_sample) / (sample_rate * n_channels)
            print(f"  Trimmed: {format_duration(start_sec)} -> {format_duration(end_sec or total_duration)}")
            print(f"  Duration: {format_duration(trim_duration)}")

        return self._write_wav(output_path, params, trimmed)

    def split(
        self,
        input_path: str,
        output_dir: str,
        interval_sec: float = 60.0,
        prefix: str = "part",
        verbose: bool = False,
    ) -> List[str]:
        """Split an audio file into equal parts.

        Args:
            input_path: Path to the input WAV file.
            output_dir: Directory for output files.
            interval_sec: Duration of each part in seconds.
            prefix: Filename prefix for output parts.
            verbose: If True, print progress info.

        Returns:
            List of output file paths.
        """
        params, samples, _ = self._read_wav(input_path)
        sample_rate = params.framerate
        n_channels = params.nchannels

        samples_per_part = int(interval_sec * sample_rate) * n_channels
        total_samples = len(samples)

        if samples_per_part <= 0:
            raise AudioProcessingError("split", "Invalid interval")

        output_files = []
        part_num = 0

        progress = ProgressBar(total=total_samples, prefix="  Splitting: ")

        for start in range(0, total_samples, samples_per_part):
            end = min(start + samples_per_part, total_samples)
            part_samples = samples[start:end]
            part_num += 1

            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_dir, f"{prefix}_{part_num:03d}_{base_name}.wav")
            self._write_wav(output_path, params, part_samples)
            output_files.append(output_path)

            if verbose:
                part_duration = (end - start) / (sample_rate * n_channels)
                print(f"  Part {part_num}: {format_duration(part_duration)} -> {output_path}")

            progress.update(end)

        progress.finish()
        return output_files

    def concat(
        self,
        input_paths: List[str],
        output_path: str,
        verbose: bool = False,
    ) -> str:
        """Concatenate multiple audio files into one.

        All files must have the same sample rate, channels, and bit depth.

        Args:
            input_paths: List of input WAV file paths.
            output_path: Path for the output file.
            verbose: If True, print progress info.

        Returns:
            Path to the concatenated file.
        """
        if not input_paths:
            raise AudioProcessingError("concat", "No input files provided")

        # Read first file to get parameters
        first_params, _, _ = self._read_wav(input_paths[0])

        all_samples = []
        for i, path in enumerate(input_paths):
            params, samples, _ = self._read_wav(path)

            # Verify compatible parameters
            if (params.framerate != first_params.framerate or
                    params.nchannels != first_params.nchannels or
                    params.sampwidth != first_params.sampwidth):
                raise AudioProcessingError(
                    "concat",
                    f"File '{os.path.basename(path)}' has incompatible parameters. "
                    f"All files must have the same sample rate, channels, and bit depth.",
                )

            all_samples.extend(samples)
            if verbose:
                print(f"  Added: {os.path.basename(path)}")

        result = self._write_wav(output_path, first_params, all_samples)

        if verbose:
            duration = len(all_samples) / (first_params.framerate * first_params.nchannels)
            print(f"  Concatenated {len(input_paths)} files, total duration: {format_duration(duration)}")

        return result

    def fade_in(
        self,
        input_path: str,
        output_path: str,
        duration_sec: float = 2.0,
        verbose: bool = False,
    ) -> str:
        """Apply fade-in effect to the beginning of an audio file.

        Args:
            input_path: Path to the input WAV file.
            output_path: Path for the output file.
            duration_sec: Fade duration in seconds.
            verbose: If True, print progress info.

        Returns:
            Path to the output file.
        """
        params, samples, _ = self._read_wav(input_path)
        sample_rate = params.framerate
        n_channels = params.nchannels

        fade_samples = int(duration_sec * sample_rate) * n_channels
        fade_samples = min(fade_samples, len(samples))

        for i in range(fade_samples):
            # Linear fade-in
            progress = i / fade_samples
            samples[i] *= progress

        if verbose:
            print(f"  Applied fade-in: {duration_sec}s")

        return self._write_wav(output_path, params, samples)

    def fade_out(
        self,
        input_path: str,
        output_path: str,
        duration_sec: float = 2.0,
        verbose: bool = False,
    ) -> str:
        """Apply fade-out effect to the end of an audio file.

        Args:
            input_path: Path to the input WAV file.
            output_path: Path for the output file.
            duration_sec: Fade duration in seconds.
            verbose: If True, print progress info.

        Returns:
            Path to the output file.
        """
        params, samples, _ = self._read_wav(input_path)
        sample_rate = params.framerate
        n_channels = params.nchannels

        fade_samples = int(duration_sec * sample_rate) * n_channels
        fade_samples = min(fade_samples, len(samples))

        start = len(samples) - fade_samples
        for i in range(fade_samples):
            # Linear fade-out
            progress = 1.0 - (i / fade_samples)
            samples[start + i] *= progress

        if verbose:
            print(f"  Applied fade-out: {duration_sec}s")

        return self._write_wav(output_path, params, samples)

    def normalize(
        self,
        input_path: str,
        output_path: str,
        target_dbfs: float = -3.0,
        verbose: bool = False,
    ) -> str:
        """Normalize audio loudness to a target level.

        Args:
            input_path: Path to the input WAV file.
            output_path: Path for the output file.
            target_dbfs: Target level in dBFS (default: -3.0).
            verbose: If True, print progress info.

        Returns:
            Path to the normalized file.
        """
        params, samples, _ = self._read_wav(input_path)

        # Calculate current peak
        peak = max(abs(s) for s in samples) if samples else 0
        if peak == 0:
            if verbose:
                print("  Warning: Audio is silent, nothing to normalize.")
            return self._write_wav(output_path, params, samples)

        current_db = linear_to_db(peak)
        gain_db = target_dbfs - current_db

        if gain_db >= 0:
            # Apply gain to reach target
            gain_linear = db_to_linear(gain_db)
            for i in range(len(samples)):
                samples[i] *= gain_linear
                # Clamp to prevent clipping
                samples[i] = max(-1.0, min(1.0, samples[i]))
        else:
            # Reduce to target
            gain_linear = db_to_linear(gain_db)
            for i in range(len(samples)):
                samples[i] *= gain_linear

        if verbose:
            new_peak = max(abs(s) for s in samples)
            new_db = linear_to_db(new_peak)
            print(f"  Normalized: {current_db:.1f} dBFS -> {new_db:.1f} dBFS (target: {target_dbfs:.1f} dBFS)")

        return self._write_wav(output_path, params, samples)

    def gain(
        self,
        input_path: str,
        output_path: str,
        db: float,
        verbose: bool = False,
    ) -> str:
        """Adjust audio volume by a specified amount in dB.

        Args:
            input_path: Path to the input WAV file.
            output_path: Path for the output file.
            db: Gain in decibels (positive = louder, negative = quieter).
            verbose: If True, print progress info.

        Returns:
            Path to the output file.
        """
        params, samples, _ = self._read_wav(input_path)

        gain_linear = db_to_linear(db)

        clipped = 0
        for i in range(len(samples)):
            samples[i] *= gain_linear
            if abs(samples[i]) > 1.0:
                samples[i] = max(-1.0, min(1.0, samples[i]))
                clipped += 1

        if verbose:
            clip_pct = (clipped / len(samples) * 100) if samples else 0
            print(f"  Gain: {db:+.1f} dB")
            if clipped > 0:
                print(f"  Warning: {clipped} samples clipped ({clip_pct:.2f}%)")

        return self._write_wav(output_path, params, samples)
