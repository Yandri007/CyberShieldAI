#!/usr/bin/env python
"""Command-line entry point for local Django management commands."""

import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cybershield.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django could not be imported. Activate the project virtual environment "
            "and install the packages from requirements.txt."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
