#!/usr/bin/env python3
import os
import click

def get_size(path):
    """Recursively total up file sizes under `path`."""
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                total += os.path.getsize(fp)
            except OSError:
                pass
    return total

def human_readable(size, precision=2):
    """Convert a byte count into a human‑readable string."""
    for unit in ('B','KB','MB','GB','TB','PB'):
        if size < 1024.0:
            return f"{size:.{precision}f}{unit}"
        size /= 1024.0
    return f"{size:.{precision}f}EB"

@click.command()
@click.argument(
    "path",
    type=click.Path(exists=True),
    default=".",
    required=False,
)
@click.option(
    "-H", "--human",
    is_flag=True,
    help="Print sizes in human‑readable form (e.g. 1.23GB)."
)
@click.option(
    "-s", "--sort",
    is_flag=True,
    help="Sort entries by size, largest first."
)
@click.option(
    "--files/--no-files",
    default=False,
    help="Also include files in the listing (not just subdirectories)."
)
def dirsizes(path, human, sort, files):
    """
    Show sizes of subdirectories (and optionally files) under PATH.
    If no path is provided, the current directory is used.
    """
    # If no path is provided, use the current directory
    if path == ".":
        click.echo("No path provided, using current directory.")

    entries = []
    for entry in os.scandir(path):
        if entry.is_dir() or (files and entry.is_file()):
            size = get_size(entry.path) if entry.is_dir() else os.path.getsize(entry.path)
            entries.append((entry.name, size))

    if sort:
        entries.sort(key=lambda x: x[1], reverse=True)

    for name, size in entries:
        size_str = human_readable(size) if human else f"{size/1024/1024:.2f} MB"
        click.echo(f"{name:40}  {size_str}")

if __name__ == "__main__":
    dirsizes()