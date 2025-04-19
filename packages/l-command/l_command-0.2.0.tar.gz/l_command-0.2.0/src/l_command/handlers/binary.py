"""
Handler for processing binary files.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

from l_command.handlers.base import FileHandler

# Limit the size of binary files we attempt to process to avoid performance issues
MAX_BINARY_SIZE_BYTES = 10 * 1024 * 1024  # 10MB


class BinaryHandler(FileHandler):
    """Handler for binary files."""

    @staticmethod
    def _is_binary_content(file_path: Path) -> bool:
        """
        Fallback check if file command is not available or fails.
        Tries to detect binary content by checking for null bytes
        or a high proportion of non-printable characters in the first 1KB.
        """
        try:
            with file_path.open("rb") as f:
                sample = f.read(1024)
            # Simple check for null byte
            if b"\\x00" in sample:
                return True
            # Check for non-printable characters (excluding common whitespace)
            text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x7F)))
            non_text_ratio = sum(1 for byte in sample if byte not in text_chars) / len(sample)
            # Arbitrary threshold, might need tuning
            return non_text_ratio > 0.3
        except OSError:
            return False
        except ZeroDivisionError:  # Handle empty file case
            return False

    @staticmethod
    def can_handle(path: Path) -> bool:
        """Determine if the file is likely binary and should be handled."""
        if not path.is_file():
            return False

        try:
            if path.stat().st_size > MAX_BINARY_SIZE_BYTES:
                return False
            # Optimization: Handle empty files as non-binary
            if path.stat().st_size == 0:
                return False
        except OSError:
            # If we can't get stats, assume we shouldn't handle it
            return False

        # Prefer using the 'file' command if available
        if shutil.which("file"):
            try:
                result = subprocess.run(
                    ["file", "--mime-encoding", "-b", str(path)],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=1,  # Add a timeout to prevent hangs
                )
                encoding = result.stdout.strip()
                # Treat 'binary' or 'unknown-*' as binary
                if encoding == "binary" or encoding.startswith("unknown-"):
                    return True
                # Sometimes 'us-ascii' or 'utf-8' might be reported for binaries
                # containing mostly text-like data, so fall through to content check.
                if encoding in ["us-ascii", "utf-8", "iso-8859-1"]:
                    # Use content check as a secondary measure for potentially text-like binaries
                    return BinaryHandler._is_binary_content(path)
                # If file reports a specific non-text encoding, treat as binary
                return encoding not in ["us-ascii", "utf-8", "iso-8859-1"]

            except subprocess.CalledProcessError:
                # file command failed, fallback to content check
                return BinaryHandler._is_binary_content(path)
            except subprocess.TimeoutExpired:
                # file command timed out, fallback to content check
                print(f"Warning: 'file' command timed out for {path}", file=sys.stderr)
                return BinaryHandler._is_binary_content(path)
            except Exception as e:
                print(f"Warning: 'file' command check failed for {path}: {e}", file=sys.stderr)
                # Fallback if 'file' command has other issues
                return BinaryHandler._is_binary_content(path)
        else:
            # Fallback to content check if 'file' command is not available
            return BinaryHandler._is_binary_content(path)

    @staticmethod
    def handle(path: Path) -> None:
        """Display the contents of a binary file using hexdump."""
        if not shutil.which("hexdump"):
            print(
                "Error: 'hexdump' command not found. Cannot display binary file.",
                file=sys.stderr,
            )
            # Consider adding a fallback to 'strings' or basic message here later?
            return

        try:
            # Get terminal height
            terminal_height = os.get_terminal_size().lines
        except OSError:
            # Fallback if not running in a terminal (e.g., piped)
            terminal_height = float("inf")  # Always use direct output

        command = ["hexdump", "-C", str(path)]

        try:
            # First subprocess call to count lines
            # Use Popen to handle potentially large output without loading all into memory
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            line_count = 0
            # Read line by line to count without storing the whole output
            try:
                for _ in process.stdout:  # type: ignore
                    line_count += 1
            except Exception as e:
                # Handle potential decoding errors if output isn't standard text,
                # although hexdump should be fine
                print(f"Warning: Error reading hexdump output: {e}", file=sys.stderr)
            finally:
                process.stdout.close()  # type: ignore
                process.wait()  # Wait for the process to finish

            # Second subprocess call to display content
            if line_count > terminal_height and shutil.which("less"):
                hexdump_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                try:
                    subprocess.run(["less", "-R"], stdin=hexdump_process.stdout, check=True)
                except subprocess.CalledProcessError as less_err:
                    # less might exit with non-zero if user quits with 'q' before EOF.
                    # This is not an error for us. Typically, quitting less results in retcode 0 or
                    # sometimes 130 (SIGINT) if Ctrl+C is used. If stderr is empty, assume it was a normal quit.
                    if less_err.stderr:
                        print(f"Error running less: {less_err.stderr.decode(errors='ignore')}", file=sys.stderr)

                hexdump_process.stdout.close()  # type: ignore
                hexdump_retcode = hexdump_process.wait()
                # Check if hexdump itself had an error
                if hexdump_retcode != 0:
                    error_output = hexdump_process.stderr.read().decode(errors="ignore")  # type: ignore
                    print(
                        f"hexdump process exited with code {hexdump_retcode}. Error: {error_output}",
                        file=sys.stderr,
                    )
            else:
                # Output directly if it fits or less is not available
                subprocess.run(command, check=True)

        except subprocess.CalledProcessError as e:
            print(f"Error running hexdump: {e}", file=sys.stderr)
        except OSError as e:
            print(f"Error accessing binary file or running subprocess: {e}", file=sys.stderr)
        except Exception as e:  # Catch unexpected errors
            print(f"An unexpected error occurred: {e}", file=sys.stderr)

    @staticmethod
    def priority() -> int:
        """Return the priority of this handler."""
        # Lower priority than JSON (90) and Archive (80), higher than default (0)
        return 60
