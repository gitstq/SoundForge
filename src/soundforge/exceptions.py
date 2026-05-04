"""
Custom exceptions for SoundForge.

Provides a hierarchy of meaningful exceptions for audio processing errors.
"""


class SoundForgeError(Exception):
    """Base exception for all SoundForge errors."""

    def __init__(self, message: str = "", suggestion: str = "") -> None:
        self.message = message
        self.suggestion = suggestion
        full_msg = message
        if suggestion:
            full_msg += f"\n  Suggestion: {suggestion}"
        super().__init__(full_msg)


class FormatNotSupportedError(SoundForgeError):
    """Raised when an audio format is not supported."""

    def __init__(self, format_name: str = "") -> None:
        msg = f"Format '{format_name}' is not supported." if format_name else "Format is not supported."
        suggestion = (
            "Supported formats: WAV (built-in), MP3/FLAC/OGG/AAC (requires ffmpeg). "
            "Install ffmpeg: https://ffmpeg.org/download.html"
        )
        super().__init__(msg, suggestion)


class AudioFileNotFoundError(SoundForgeError):
    """Raised when an audio file cannot be found."""

    def __init__(self, filepath: str = "") -> None:
        msg = f"Audio file not found: '{filepath}'" if filepath else "Audio file not found."
        suggestion = "Check that the file path is correct and the file exists."
        super().__init__(msg, suggestion)


class FFmpegNotFoundError(SoundForgeError):
    """Raised when ffmpeg is required but not found on the system."""

    def __init__(self) -> None:
        msg = "ffmpeg is not installed or not found in PATH."
        suggestion = (
            "Install ffmpeg to enable MP3/FLAC/OGG/AAC conversion. "
            "Visit: https://ffmpeg.org/download.html "
            "Or use WAV format which is supported without ffmpeg."
        )
        super().__init__(msg, suggestion)


class InvalidAudioError(SoundForgeError):
    """Raised when an audio file is corrupted or invalid."""

    def __init__(self, filepath: str = "", reason: str = "") -> None:
        msg = f"Invalid audio file: '{filepath}'"
        if reason:
            msg += f" ({reason})"
        suggestion = (
            "The file may be corrupted or not a valid audio file. "
            "Try re-encoding the file or using a different format."
        )
        super().__init__(msg, suggestion)


class AudioProcessingError(SoundForgeError):
    """Raised when an audio processing operation fails."""

    def __init__(self, operation: str = "", reason: str = "") -> None:
        msg = f"Audio processing failed: {operation}"
        if reason:
            msg += f" - {reason}"
        suggestion = "Check input file integrity and parameters."
        super().__init__(msg, suggestion)


class RecordingError(SoundForgeError):
    """Raised when audio recording fails."""

    def __init__(self, reason: str = "") -> None:
        msg = f"Recording failed: {reason}" if reason else "Recording failed."
        suggestion = (
            "Ensure a microphone is connected and the recording library is installed. "
            "Install with: pip install sounddevice"
        )
        super().__init__(msg, suggestion)
