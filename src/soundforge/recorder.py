"""
Audio recording module for SoundForge.

Provides terminal-based audio recording with real-time level metering.
Uses sounddevice as an optional dependency.
"""

import os
import sys
import time
import wave
from typing import Optional

from .exceptions import RecordingError
from .utils import color_text, ensure_dir, format_duration


class AudioRecorder:
    """Terminal-based audio recorder.

    Records audio from the default input device and saves to WAV format.
    Requires the 'sounddevice' package as an optional dependency.
    """

    def __init__(self) -> None:
        """Initialize the AudioRecorder."""
        self._sd = None
        self._recording = False

    def _check_sounddevice(self) -> bool:
        """Check if sounddevice is available.

        Returns:
            True if sounddevice is importable, False otherwise.
        """
        if self._sd is not None:
            return True
        try:
            import sounddevice as sd
            self._sd = sd
            return True
        except ImportError:
            return False

    def record(
        self,
        output_path: str,
        duration: float = 10.0,
        sample_rate: int = 44100,
        channels: int = 1,
        verbose: bool = True,
    ) -> str:
        """Record audio from the default input device.

        Args:
            output_path: Path to save the recorded WAV file.
            duration: Recording duration in seconds.
            sample_rate: Sample rate in Hz.
            channels: Number of audio channels (1=mono, 2=stereo).
            verbose: If True, show real-time level meter.

        Returns:
            Path to the recorded WAV file.

        Raises:
            RecordingError: If recording fails or sounddevice is not installed.
        """
        if not self._check_sounddevice():
            raise RecordingError(
                "sounddevice package is required for recording. "
                "Install it with: pip install sounddevice"
            )

        ensure_dir(output_path)

        sd = self._sd  # type: ignore

        if verbose:
            print()
            print(color_text("  Recording Controls:", "bold"))
            print(f"  Duration:   {format_duration(duration)}")
            print(f"  Sample Rate: {sample_rate} Hz")
            print(f"  Channels:    {'Mono' if channels == 1 else 'Stereo'}")
            print()
            print(color_text("  Press Ctrl+C to stop recording early.", "yellow"))
            print()

        recorded_frames = []

        def callback(indata, frames, time_info, status):
            """Audio stream callback."""
            if status:
                if verbose:
                    print(f"\r  Warning: {status}", end="", flush=True)
            recorded_frames.append(indata.copy())

            # Real-time level meter
            if verbose:
                import numpy as np
                peak = float(np.max(np.abs(indata)))
                if peak > 0:
                    db = 20.0 * __import__('math').log10(peak)
                else:
                    db = -60.0
                bar_width = 40
                normalized = max(0, min(1, (db + 60) / 60))
                filled = int(normalized * bar_width)
                bar = "=" * filled + "-" * (bar_width - filled)
                elapsed = len(recorded_frames) * frames / sample_rate
                sys.stdout.write(
                    f"\r  [{bar}] {db:5.1f} dB  |  "
                    f"{format_duration(elapsed)} / {format_duration(duration)}"
                )
                sys.stdout.flush()

        try:
            self._recording = True

            with sd.InputStream(
                samplerate=sample_rate,
                channels=channels,
                callback=callback,
                dtype="float32",
            ):
                # Record for specified duration
                time.sleep(duration)

            self._recording = False

            if verbose:
                print()

            # Combine recorded frames
            import numpy as np
            if recorded_frames:
                audio_data = np.concatenate(recorded_frames, axis=0)
            else:
                audio_data = np.array([], dtype="float32")

            # Convert float32 samples to int16 for WAV
            audio_int16 = (audio_data * 32767).astype("int16")

            # Save to WAV
            with wave.open(output_path, "wb") as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(sample_rate)
                wf.writeframes(audio_int16.tobytes())

            if verbose:
                actual_duration = len(audio_data) / sample_rate
                print(color_text(f"  Saved: {output_path}", "green"))
                print(f"  Duration: {format_duration(actual_duration)}")
                print()

            return output_path

        except KeyboardInterrupt:
            self._recording = False
            if verbose:
                print("\n")
                print(color_text("  Recording stopped by user.", "yellow"))

            # Save whatever was recorded
            if recorded_frames:
                import numpy as np
                audio_data = np.concatenate(recorded_frames, axis=0)
                audio_int16 = (audio_data * 32767).astype("int16")

                with wave.open(output_path, "wb") as wf:
                    wf.setnchannels(channels)
                    wf.setsampwidth(2)
                    wf.setframerate(sample_rate)
                    wf.writeframes(audio_int16.tobytes())

                actual_duration = len(audio_data) / sample_rate
                print(color_text(f"  Saved partial recording: {output_path}", "green"))
                print(f"  Duration: {format_duration(actual_duration)}")
                print()

            return output_path

        except Exception as e:
            self._recording = False
            raise RecordingError(str(e))

    @property
    def is_recording(self) -> bool:
        """Check if currently recording.

        Returns:
            True if recording is in progress.
        """
        return self._recording

    def list_devices(self) -> None:
        """List available audio input/output devices."""
        if not self._check_sounddevice():
            print(color_text("  sounddevice is required. Install with: pip install sounddevice", "yellow"))
            return

        sd = self._sd  # type: ignore
        devices = sd.query_devices()

        print()
        print(color_text("  Audio Devices:", "bold"))
        print()

        for i, dev in enumerate(devices):
            name = dev["name"]
            max_in = dev["max_input_channels"]
            max_out = dev["max_output_channels"]
            sr = dev["default_samplerate"]

            flags = []
            if max_in > 0:
                flags.append(color_text("IN", "green"))
            if max_out > 0:
                flags.append(color_text("OUT", "blue"))

            flag_str = " ".join(flags) if flags else color_text("-", "dim")
            print(f"  [{i}] {name}")
            print(f"      {flag_str}  SR: {sr:.0f}Hz  InCh: {max_in}  OutCh: {max_out}")

        print()
