"""Compare two directory trees without modifying them."""

import argparse
import hashlib
import os
from pathlib import Path
import sys


def inventory(root):
    files = {}
    def fail(error):
        raise error

    for directory, _, names in os.walk(root, onerror=fail, followlinks=False):
        for name in names:
            path = Path(directory) / name
            if not path.is_symlink() and path.is_file():
                files[path.relative_to(root).as_posix()] = path
    return files


def digest(path):
    sha256 = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)
    return sha256.digest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("copy", type=Path)
    parser.add_argument("--sha256", action="store_true", help="Also compare file contents")
    args = parser.parse_args()
    for root in (args.source, args.copy):
        if root.is_symlink() or not root.is_dir():
            parser.error(f"Expected a directory, not a symlink: {root}")

    try:
        source, copy = inventory(args.source), inventory(args.copy)
        missing = sorted(source.keys() - copy.keys())
        extra = sorted(copy.keys() - source.keys())
        changed = []
        for name in sorted(source.keys() & copy.keys()):
            first, second = source[name], copy[name]
            if first.stat().st_size != second.stat().st_size:
                changed.append(name)
            elif args.sha256 and digest(first) != digest(second):
                changed.append(name)
    except OSError as error:
        print(f"Could not complete the comparison: {error}", file=sys.stderr)
        return 2

    for label, names in (("MISSING", missing), ("EXTRA", extra), ("DIFFERENT", changed)):
        for name in names:
            print(f"{label}  {name!r}")
    print(f"Source: {len(source)} files. Copy: {len(copy)} files.")
    if missing or extra or changed:
        return 1
    print("Files match by path and " + ("SHA-256." if args.sha256 else "size."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
