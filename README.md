# Copy Audit

Compare two local directory trees before retiring the source of a backup or migration. Copy Audit reports missing, extra and changed files by relative path. It reads files locally and never modifies either tree.

Requires Python 3.9 or newer. No third-party dependencies.

```sh
python3 copy_audit.py /path/to/original /path/to/copy
python3 copy_audit.py /path/to/original /path/to/copy --sha256
```

The default compares names and byte sizes. Use SHA-256 when you need to detect changes that preserve the file size. For a cloud drive, make the files available locally and wait for syncing to finish before running the comparison. Run against stable directories. Symbolic links and empty directories are outside the comparison.

Exit codes: 0 for a match, 1 for differences, and 2 for an invalid directory or a read failure. Use this as one check before deleting any source files.

Issues and pull requests are welcome. Use synthetic files in bug reports.
