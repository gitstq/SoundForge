"""
SoundForge CLI - Main entry point.

Provides the command-line interface for all audio processing operations.
Uses argparse for subcommand routing with comprehensive help text.
"""

import argparse
import os
import sys

from . import __version__


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add common arguments to a subcommand parser.

    Args:
        parser: ArgumentParser to add arguments to.
    """
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress all output except errors")


def build_parser() -> argparse.ArgumentParser:
    """Build the main argument parser with all subcommands.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="soundforge",
        description="SoundForge - Lightweight Terminal Audio Processing CLI Toolbox",
        epilog="Examples:\n"
               "  soundforge info audio.wav\n"
               "  soundforge convert audio.wav output.mp3\n"
               "  soundforge trim audio.wav --start 10 --end 30 -o trimmed.wav\n"
               "  soundforge normalize audio.wav -o normalized.wav\n"
               "  soundforge visualize audio.wav\n"
               "  soundforge batch convert /music/*.wav -f mp3 -o /converted/\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ------------------------------------------------------------------
    # convert
    # ------------------------------------------------------------------
    p_convert = subparsers.add_parser(
        "convert",
        help="Convert audio file format",
        description="Convert an audio file to a different format. "
                    "WAV is supported natively; MP3/FLAC/OGG/AAC require ffmpeg.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_convert.add_argument("input", help="Input audio file path")
    p_convert.add_argument("output", nargs="?", help="Output file path (default: auto-generated)")
    p_convert.add_argument("-f", "--format", dest="fmt", help="Output format (wav/mp3/flac/ogg/aac)")
    p_convert.add_argument("-o", "--output-dir", help="Output directory")
    p_convert.add_argument("--quality", choices=["low", "medium", "high", "very_high"],
                           default="medium", help="Encoding quality (default: medium)")
    p_convert.add_argument("--sample-rate", type=int, help="Target sample rate in Hz")
    p_convert.add_argument("--channels", type=int, help="Target channel count")
    p_convert.add_argument("--formats", action="store_true", help="List supported formats")
    _add_common_args(p_convert)

    # ------------------------------------------------------------------
    # trim
    # ------------------------------------------------------------------
    p_trim = subparsers.add_parser(
        "trim",
        help="Trim audio file",
        description="Extract a portion of an audio file.",
    )
    p_trim.add_argument("input", help="Input audio file path")
    p_trim.add_argument("-o", "--output", required=True, help="Output file path")
    p_trim.add_argument("-s", "--start", type=float, default=0.0, help="Start time in seconds")
    p_trim.add_argument("-e", "--end", type=float, default=None, help="End time in seconds")
    _add_common_args(p_trim)

    # ------------------------------------------------------------------
    # split
    # ------------------------------------------------------------------
    p_split = subparsers.add_parser(
        "split",
        help="Split audio file into parts",
        description="Split an audio file into equal-length parts.",
    )
    p_split.add_argument("input", help="Input audio file path")
    p_split.add_argument("-o", "--output-dir", required=True, help="Output directory")
    p_split.add_argument("-i", "--interval", type=float, default=60.0,
                         help="Duration of each part in seconds (default: 60)")
    p_split.add_argument("--prefix", default="part", help="Filename prefix for parts")
    _add_common_args(p_split)

    # ------------------------------------------------------------------
    # concat
    # ------------------------------------------------------------------
    p_concat = subparsers.add_parser(
        "concat",
        help="Concatenate audio files",
        description="Join multiple audio files into one. "
                    "All files must have the same sample rate, channels, and bit depth.",
    )
    p_concat.add_argument("inputs", nargs="+", help="Input audio file paths")
    p_concat.add_argument("-o", "--output", required=True, help="Output file path")
    _add_common_args(p_concat)

    # ------------------------------------------------------------------
    # info
    # ------------------------------------------------------------------
    p_info = subparsers.add_parser(
        "info",
        help="Display audio file information",
        description="Show detailed metadata and loudness analysis for an audio file.",
    )
    p_info.add_argument("input", help="Input audio file path")
    _add_common_args(p_info)

    # ------------------------------------------------------------------
    # visualize
    # ------------------------------------------------------------------
    p_vis = subparsers.add_parser(
        "visualize",
        help="Visualize audio waveform or spectrum",
        description="Display ASCII waveform or frequency spectrum in the terminal.",
    )
    p_vis.add_argument("input", help="Input audio file path")
    p_vis.add_argument("-t", "--type", choices=["waveform", "spectrum"], default="waveform",
                       help="Visualization type (default: waveform)")
    p_vis.add_argument("-W", "--width", type=int, default=80, help="Width in characters (default: 80)")
    p_vis.add_argument("-H", "--height", type=int, default=20, help="Height in characters (default: 20)")
    _add_common_args(p_vis)

    # ------------------------------------------------------------------
    # normalize
    # ------------------------------------------------------------------
    p_norm = subparsers.add_parser(
        "normalize",
        help="Normalize audio loudness",
        description="Normalize audio to a target loudness level.",
    )
    p_norm.add_argument("input", help="Input audio file path")
    p_norm.add_argument("-o", "--output", required=True, help="Output file path")
    p_norm.add_argument("--target", type=float, default=-3.0,
                        help="Target level in dBFS (default: -3.0)")
    _add_common_args(p_norm)

    # ------------------------------------------------------------------
    # gain
    # ------------------------------------------------------------------
    p_gain = subparsers.add_parser(
        "gain",
        help="Adjust audio volume",
        description="Adjust audio volume by a specified amount in dB.",
    )
    p_gain.add_argument("input", help="Input audio file path")
    p_gain.add_argument("-o", "--output", required=True, help="Output file path")
    p_gain.add_argument("-d", "--db", type=float, required=True, help="Gain in dB (e.g., +6 or -3)")
    _add_common_args(p_gain)

    # ------------------------------------------------------------------
    # fade
    # ------------------------------------------------------------------
    p_fade = subparsers.add_parser(
        "fade",
        help="Apply fade in/out effect",
        description="Apply fade-in or fade-out effect to an audio file.",
    )
    p_fade.add_argument("input", help="Input audio file path")
    p_fade.add_argument("-o", "--output", required=True, help="Output file path")
    p_fade.add_argument("-t", "--type", choices=["in", "out", "both"], default="both",
                        help="Fade type (default: both)")
    p_fade.add_argument("-d", "--duration", type=float, default=2.0,
                        help="Fade duration in seconds (default: 2.0)")
    _add_common_args(p_fade)

    # ------------------------------------------------------------------
    # batch
    # ------------------------------------------------------------------
    p_batch = subparsers.add_parser(
        "batch",
        help="Batch process audio files",
        description="Process multiple audio files in a directory.",
    )
    p_batch.add_argument("operation", choices=["convert", "normalize", "info"],
                         help="Operation to perform")
    p_batch.add_argument("directory", help="Directory containing audio files")
    p_batch.add_argument("-p", "--pattern", default="*", help="File glob pattern (default: *)")
    p_batch.add_argument("-o", "--output-dir", help="Output directory")
    p_batch.add_argument("-f", "--format", dest="fmt", help="Output format for conversion")
    p_batch.add_argument("--quality", choices=["low", "medium", "high", "very_high"],
                         default="medium", help="Encoding quality")
    p_batch.add_argument("--no-recursive", action="store_true",
                         help="Do not search subdirectories")
    _add_common_args(p_batch)

    # ------------------------------------------------------------------
    # record
    # ------------------------------------------------------------------
    p_rec = subparsers.add_parser(
        "record",
        help="Record audio from microphone",
        description="Record audio from the default input device. "
                    "Requires: pip install sounddevice",
    )
    p_rec.add_argument("-o", "--output", default="recording.wav", help="Output file path")
    p_rec.add_argument("-d", "--duration", type=float, default=10.0,
                       help="Recording duration in seconds (default: 10)")
    p_rec.add_argument("--sample-rate", type=int, default=44100, help="Sample rate (default: 44100)")
    p_rec.add_argument("--channels", type=int, default=1, help="Number of channels (default: 1)")
    p_rec.add_argument("--devices", action="store_true", help="List available audio devices")
    _add_common_args(p_rec)

    return parser


def main(argv: list = None) -> int:
    """Main CLI entry point.

    Args:
        argv: Command-line arguments (default: sys.argv[1:]).

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    # No command specified - show help
    if not args.command:
        parser.print_help()
        return 0

    try:
        return _dispatch_command(args)
    except KeyboardInterrupt:
        print()
        from .utils import color_text
        print(color_text("  Operation cancelled by user.", "yellow"))
        return 130
    except Exception as e:
        from .utils import color_text
        print()
        print(color_text(f"  Error: {e}", "red"))
        return 1


def _dispatch_command(args: argparse.Namespace) -> int:
    """Dispatch to the appropriate command handler.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code.
    """
    from .utils import color_text, print_banner

    verbose = getattr(args, "verbose", False)
    quiet = getattr(args, "quiet", False)

    if not quiet and args.command not in ("info", "visualize"):
        print_banner()

    # ------------------------------------------------------------------
    # convert
    # ------------------------------------------------------------------
    if args.command == "convert":
        from .converter import AudioConverter

        converter = AudioConverter()

        if args.formats:
            converter.print_supported_formats()
            return 0

        if not hasattr(args, "input") or not args.input:
            print(color_text("  Error: Input file is required.", "red"))
            return 1

        # Determine output path
        output = args.output
        if not output and args.output_dir:
            # If -o is used as output path (not a directory), treat it as output
            if os.path.splitext(args.output_dir)[1]:
                output = args.output_dir
                args.output_dir = ""
        if not output:
            if args.fmt:
                base = os.path.splitext(args.input)[0]
                output = base + "." + args.fmt
            else:
                print(color_text("  Error: Specify output path or format with -f.", "red"))
                return 1

        if args.output_dir:
            filename = os.path.basename(output)
            output = os.path.join(args.output_dir, filename)

        result = converter.convert(
            args.input,
            output,
            quality=args.quality,
            sample_rate=args.sample_rate,
            channels=args.channels,
            verbose=verbose,
        )
        if not quiet:
            print(color_text(f"  Done: {result}", "green"))
        return 0

    # ------------------------------------------------------------------
    # trim
    # ------------------------------------------------------------------
    elif args.command == "trim":
        from .editor import AudioEditor

        editor = AudioEditor()
        result = editor.trim(
            args.input,
            args.output,
            start_sec=args.start,
            end_sec=args.end,
            verbose=verbose,
        )
        if not quiet:
            print(color_text(f"  Done: {result}", "green"))
        return 0

    # ------------------------------------------------------------------
    # split
    # ------------------------------------------------------------------
    elif args.command == "split":
        from .editor import AudioEditor

        editor = AudioEditor()
        results = editor.split(
            args.input,
            args.output_dir,
            interval_sec=args.interval,
            prefix=args.prefix,
            verbose=verbose,
        )
        if not quiet:
            print(color_text(f"  Done: Split into {len(results)} parts", "green"))
        return 0

    # ------------------------------------------------------------------
    # concat
    # ------------------------------------------------------------------
    elif args.command == "concat":
        from .editor import AudioEditor

        editor = AudioEditor()
        result = editor.concat(
            args.inputs,
            args.output,
            verbose=verbose,
        )
        if not quiet:
            print(color_text(f"  Done: {result}", "green"))
        return 0

    # ------------------------------------------------------------------
    # info
    # ------------------------------------------------------------------
    elif args.command == "info":
        from .analyzer import AudioAnalyzer

        analyzer = AudioAnalyzer()
        analyzer.print_info(args.input, verbose=verbose)
        return 0

    # ------------------------------------------------------------------
    # visualize
    # ------------------------------------------------------------------
    elif args.command == "visualize":
        from .visualizer import AudioVisualizer

        viz = AudioVisualizer()
        if args.type == "waveform":
            viz.print_waveform(args.input, width=args.width, height=args.height)
        else:
            viz.print_spectrum(args.input, width=args.width, height=args.height)
        return 0

    # ------------------------------------------------------------------
    # normalize
    # ------------------------------------------------------------------
    elif args.command == "normalize":
        from .editor import AudioEditor

        editor = AudioEditor()
        result = editor.normalize(
            args.input,
            args.output,
            target_dbfs=args.target,
            verbose=verbose,
        )
        if not quiet:
            print(color_text(f"  Done: {result}", "green"))
        return 0

    # ------------------------------------------------------------------
    # gain
    # ------------------------------------------------------------------
    elif args.command == "gain":
        from .editor import AudioEditor

        editor = AudioEditor()
        result = editor.gain(
            args.input,
            args.output,
            db=args.db,
            verbose=verbose,
        )
        if not quiet:
            print(color_text(f"  Done: {result}", "green"))
        return 0

    # ------------------------------------------------------------------
    # fade
    # ------------------------------------------------------------------
    elif args.command == "fade":
        from .editor import AudioEditor

        editor = AudioEditor()

        if args.type in ("in", "both"):
            editor.fade_in(args.input, args.output, duration_sec=args.duration, verbose=verbose)
        if args.type in ("out", "both"):
            editor.fade_out(args.output, args.output, duration_sec=args.duration, verbose=verbose)

        if not quiet:
            print(color_text(f"  Done: {args.output}", "green"))
        return 0

    # ------------------------------------------------------------------
    # batch
    # ------------------------------------------------------------------
    elif args.command == "batch":
        from .batch import BatchProcessor
        from .converter import AudioConverter
        from .editor import AudioEditor
        from .analyzer import AudioAnalyzer

        processor = BatchProcessor()
        output_dir = args.output_dir or args.directory
        recursive = not args.no_recursive

        if args.operation == "convert":
            if not args.fmt:
                print(color_text("  Error: Specify output format with -f for batch convert.", "red"))
                return 1

            converter = AudioConverter()

            def convert_op(inp: str, out: str) -> str:
                return converter.convert(
                    inp, out, quality=args.quality,
                    verbose=False,
                )

            ext = "." + args.fmt
            summary = processor.process(
                args.directory,
                convert_op,
                output_dir=output_dir,
                pattern=args.pattern,
                recursive=recursive,
                output_extension=ext,
                verbose=verbose,
            )

        elif args.operation == "normalize":
            editor = AudioEditor()

            def norm_op(inp: str, out: str) -> str:
                return editor.normalize(inp, out, verbose=False)

            summary = processor.process(
                args.directory,
                norm_op,
                output_dir=output_dir,
                pattern=args.pattern,
                recursive=recursive,
                output_extension=".wav",
                verbose=verbose,
            )

        elif args.operation == "info":
            analyzer = AudioAnalyzer()
            files = processor.find_files(args.directory, args.pattern, recursive)

            if not files:
                print(color_text("  No matching audio files found.", "yellow"))
                return 0

            for f in files:
                try:
                    analyzer.print_info(f, verbose=verbose)
                except Exception as e:
                    print(color_text(f"  Error reading {f}: {e}", "red"))

            return 0

        else:
            print(color_text(f"  Unknown batch operation: {args.operation}", "red"))
            return 1

        return 0 if summary["failed"] == 0 else 1

    # ------------------------------------------------------------------
    # record
    # ------------------------------------------------------------------
    elif args.command == "record":
        from .recorder import AudioRecorder

        recorder = AudioRecorder()

        if args.devices:
            recorder.list_devices()
            return 0

        result = recorder.record(
            args.output,
            duration=args.duration,
            sample_rate=args.sample_rate,
            channels=args.channels,
            verbose=not quiet,
        )
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
