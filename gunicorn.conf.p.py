"""
Gunicorn configuration.

Defines a hook to clean up the temporary directory when Gunicorn shuts down.
"""

import os
import shutil
import tempfile


TEMP_DIR = os.path.join(tempfile.gettempdir(), "temp_reports")


def on_exit(server):
    """
    Hook executed when Gunicorn shuts down.

    Cleans the temporary directory by deleting all its contents.
    """
    try:
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
            print(f"[Gunicorn] Master process cleaned up {TEMP_DIR}")
    except Exception as error:  # pylint: disable=broad-except
        print(f"[Gunicorn] Cleanup error: {error}")
