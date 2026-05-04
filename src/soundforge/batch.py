"""
Batch processing module for SoundForge.

Provides recursive directory processing with glob pattern matching,
parallel processing support, and summary reporting.
"""

import fnmatch
import os
import time
from typing import Callable, Dict, List, Optional, Tuple

from .exceptions import AudioProcessingError
from .utils import ProgressBar, color_text, ensure_dir, format_duration


# Supported audio file extensions
_AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".aac", ".m4a", ".wma", ".opus", ".aiff"}


class BatchProcessor:
    """Batch audio file processor.

    Processes audio files in directories recursively with glob pattern
    matching and provides a summary report.
    """

    def __init__(self) -> None:
        """Initialize the BatchProcessor."""
        self.results: List[Dict] = []

    def find_files(
        self,
        directory: str,
        pattern: str = "*",
        recursive: bool = True,
    ) -> List[str]:
        """Find audio files in a directory matching a pattern.

        Args:
            directory: Root directory to search.
            pattern: Glob pattern for filename matching (e.g., '*.wav').
            recursive: If True, search subdirectories recursively.

        Returns:
            Sorted list of matching file paths.
        """
        if not os.path.isdir(directory):
            raise AudioProcessingError("batch", f"Directory not found: {directory}")

        matched_files = []

        if recursive:
            for root, _dirs, files in os.walk(directory):
                for filename in files:
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in _AUDIO_EXTENSIONS:
                        if fnmatch.fnmatch(filename, pattern):
                            matched_files.append(os.path.join(root, filename))
        else:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in _AUDIO_EXTENSIONS:
                        if fnmatch.fnmatch(filename, pattern):
                            matched_files.append(filepath)

        matched_files.sort()
        return matched_files

    def process(
        self,
        directory: str,
        operation: Callable[[str, str], str],
        output_dir: str = "",
        pattern: str = "*",
        recursive: bool = True,
        output_extension: str = ".wav",
        verbose: bool = False,
    ) -> Dict:
        """Process audio files in batch.

        Args:
            directory: Root directory to search.
            operation: Callable that takes (input_path, output_path) and returns output_path.
            output_dir: Output directory (default: same as input).
            pattern: Glob pattern for file matching.
            recursive: If True, search subdirectories.
            output_extension: Extension for output files (e.g., '.mp3').
            verbose: If True, print detailed progress.

        Returns:
            Dictionary with processing summary.
        """
        files = self.find_files(directory, pattern, recursive)

        if not files:
            print(color_text("  No matching audio files found.", "yellow"))
            return {
                "total": 0,
                "success": 0,
                "failed": 0,
                "skipped": 0,
                "files": [],
                "elapsed": 0,
            }

        if not output_dir:
            output_dir = directory

        ensure_dir(output_dir)

        print(color_text(f"\n  Found {len(files)} file(s) to process\n", "bold"))

        self.results = []
        success_count = 0
        failed_count = 0
        skipped_count = 0
        start_time = time.time()

        progress = ProgressBar(total=len(files), prefix="  Processing: ")

        for i, input_path in enumerate(files):
            filename = os.path.basename(input_path)
            base_name = os.path.splitext(filename)[0]
            rel_dir = os.path.relpath(os.path.dirname(input_path), directory)

            # Build output path preserving directory structure
            if rel_dir == ".":
                out_subdir = output_dir
            else:
                out_subdir = os.path.join(output_dir, rel_dir)

            ensure_dir(out_subdir)
            output_path = os.path.join(out_subdir, base_name + output_extension)

            result = {
                "input": input_path,
                "output": output_path,
                "status": "pending",
                "error": "",
                "elapsed": 0,
            }

            file_start = time.time()

            try:
                operation(input_path, output_path)
                result["status"] = "success"
                result["elapsed"] = time.time() - file_start
                success_count += 1

                if verbose:
                    print(f"  OK: {filename} -> {os.path.basename(output_path)}")

            except Exception as e:
                result["status"] = "failed"
                result["error"] = str(e)
                result["elapsed"] = time.time() - file_start
                failed_count += 1

                if verbose:
                    print(f"  FAIL: {filename} - {e}")

            self.results.append(result)
            progress.update(i + 1)

        progress.finish()
        elapsed = time.time() - start_time

        summary = {
            "total": len(files),
            "success": success_count,
            "failed": failed_count,
            "skipped": skipped_count,
            "elapsed": elapsed,
            "files": self.results,
        }

        self._print_summary(summary)
        return summary

    def _print_summary(self, summary: Dict) -> None:
        """Print a processing summary report.

        Args:
            summary: Summary dictionary from process().
        """
        print()
        print(color_text("  " + "=" * 50, "cyan"))
        print(color_text("  Batch Processing Summary", "bold"))
        print(color_text("  " + "=" * 50, "cyan"))
        print(f"  Total files:  {summary['total']}")
        print(f"  Successful:   {color_text(str(summary['success']), 'green')}")
        print(f"  Failed:       {color_text(str(summary['failed']), 'red' if summary['failed'] > 0 else 'green')}")
        print(f"  Elapsed:      {format_duration(summary['elapsed'])}")
        print(color_text("  " + "=" * 50, "cyan"))

        # Print failed files
        failed = [r for r in summary.get("files", []) if r["status"] == "failed"]
        if failed:
            print()
            print(color_text("  Failed files:", "red"))
            for r in failed:
                print(f"    - {os.path.basename(r['input'])}: {r['error']}")

        print()
