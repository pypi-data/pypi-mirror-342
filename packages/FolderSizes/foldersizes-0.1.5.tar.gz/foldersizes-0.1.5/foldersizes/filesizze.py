#!/usr/bin/env python3
import os
import click

__version__ = "0.1.5"


@click.command()
@click.version_option(__version__, '-v', '--version', message='%(prog)s version %(version)s')
@click.argument(
    "path",
    type=click.Path(exists=True),
    default=".",
    required=False,
)
@click.option(
    "-h", "--human",
    is_flag=True,
    help="Print sizes in human‑readable form (e.g. 1.23GB)"
)
@click.option(
    "-s", "--sort",
    is_flag=True,
    help="Sort entries by size, largest first"
)
@click.option(
    "--files", "--all",
    is_flag=True,
    default=False,
    help="Also include files in the listing (not just subdirectories)"
)
def dirsizes(path, human, sort, files):
    """
    Show sizes of subdirectories (and optionally files) under PATH.
    If no path is provided, the current directory is used.
    """
    # If no path is provided, use the current directory
    if path == ".":
        click.echo("No path provided, using current directory")
    
    click.echo(f"Calculating sizes in: {path}")
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

def get_size(path):
    """Recursively calculate the size of a directory"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def human_readable(size):
    """Convert a size in bytes to a human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

if __name__ == "__main__":
    dirsizes()