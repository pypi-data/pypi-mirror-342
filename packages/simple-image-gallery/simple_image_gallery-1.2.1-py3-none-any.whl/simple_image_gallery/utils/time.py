from datetime import datetime
from pathlib import Path


def format_ctime(path: Path, time_format: str) -> str:
    """
    Formats the creation time of a file as a string.

    Args:
        path: file path
        time_format: time format string
    Returns:
        str: formatted creation time
    """
    ctime = path.stat().st_ctime
    date = datetime.fromtimestamp(ctime)
    return date.strftime(time_format)