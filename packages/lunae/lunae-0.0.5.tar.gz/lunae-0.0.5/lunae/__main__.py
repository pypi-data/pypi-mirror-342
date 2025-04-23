"""
This module serves as the entry point for the REPL (Read-Eval-Print Loop).
"""

import sys

from lunae.repl import REPL


def main():
    """
    Starts the REPL and exits with the appropriate status code.

    Returns:
        int: The exit status code.
    """
    REPL().start()
    return 0


if __name__ == "__main__":
    sys.exit(main())
