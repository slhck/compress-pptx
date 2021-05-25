import subprocess
import shlex
from pathlib import Path
import os
import sys


def which(program):
    """
    Find a program in PATH and return path
    From: http://stackoverflow.com/q/377017/
    """

    def is_exe(fpath):
        found = os.path.isfile(fpath) and os.access(fpath, os.X_OK)
        if not found and sys.platform == "win32":
            fpath = fpath + ".exe"
            found = os.path.isfile(fpath) and os.access(fpath, os.X_OK)
        return found

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = os.path.expandvars(os.path.expanduser(path)).strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def file_size(file) -> int:
    return Path(file).stat().st_size


def human_readable_size(size, decimal_places=2):
    """
    https://stackoverflow.com/a/43690506/435093
    """
    for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
        if size < 1024.0 or unit == "PiB":
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def run_command(cmd, dry_run=False, verbose=False):
    """
    Run a command directly
    """
    if dry_run or verbose:
        print(" ".join([shlex.quote(str(c)) for c in cmd]))
        if dry_run:
            return None, None

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        return stdout.decode("utf-8"), stderr.decode("utf-8")
    else:
        raise RuntimeError(
            "error running command {}: ".format(" ".join(cmd)) + stderr.decode("utf-8")
        )


def convert_size_to_bytes(size_str):
    """Convert human filesizes to bytes.
    Based on: https://stackoverflow.com/a/51253225/435093
    """
    multipliers = {
        "kilobyte": 1000,
        "megabyte": 1000 ** 2,
        "gigabyte": 1000 ** 3,
        "k": 1000,
        "kb": 1000,
        "m": 1000 ** 2,
        "mb": 1000 ** 2,
        "g": 1000 ** 3,
        "gb": 1000 ** 3,
        "kibibyte": 1024,
        "mebibyte": 1024 ** 2,
        "gibibyte": 1024 ** 3,
        "kib": 1024,
        "mib": 1024 ** 2,
        "gib": 1024 ** 3,
    }

    for suffix in multipliers:
        size_str = size_str.lower().strip().strip("s")
        if size_str.lower().endswith(suffix):
            return int(float(size_str[0 : -len(suffix)]) * multipliers[suffix])
    else:
        if size_str.endswith("b"):
            size_str = size_str[0:-1]
        elif size_str.endswith("byte"):
            size_str = size_str[0:-4]
    return int(size_str)
