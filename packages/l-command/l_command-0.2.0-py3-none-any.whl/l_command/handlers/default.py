"""
Default handler for processing regular files.
"""

import os
import subprocess
import sys
from pathlib import Path

from l_command.handlers.base import FileHandler
from l_command.utils import count_lines


class DefaultFileHandler(FileHandler):
    """Default handler for processing regular files."""

    @classmethod
    def can_handle(cls: type["DefaultFileHandler"], path: Path) -> bool:
        """Check if the path is a regular file.

        Args:
            path: The path to check.

        Returns:
            True if the path is a regular file, False otherwise.
        """
        return path.is_file()

    @classmethod
    def handle(cls: type["DefaultFileHandler"], path: Path) -> None:
        """Display file content using cat or less.

        The choice between cat and less is based on the file's line count
        and the terminal's height.

        Args:
            path: The file path to display.
        """
        line_count = count_lines(path)

        try:
            # Get terminal height
            terminal_height = os.get_terminal_size().lines
        except OSError:
            # Fallback if not running in a terminal (e.g., piped)
            terminal_height = float("inf")  # Always use cat

        # Use less if file has more lines than terminal height, otherwise use cat
        command = ["less", "-RFX"] if line_count > terminal_height else ["cat"]

        try:
            subprocess.run([*command, str(path)], check=True)
        except FileNotFoundError:
            # Handle case where cat or less might be missing (highly unlikely)
            print(f"Error: Required command '{command[0]}' not found.", file=sys.stderr)
        except subprocess.CalledProcessError as e:
            # This might happen if cat/less fails for some reason
            print(f"Error displaying file with {command[0]}: {e}", file=sys.stderr)
        except OSError as e:
            print(f"Error accessing file for default display: {e}", file=sys.stderr)

    @classmethod
    def priority(cls: type["DefaultFileHandler"]) -> int:
        """Return the priority of the default handler.

        Returns:
            0 (lowest priority).
        """
        return 0  # Lowest priority
