import csv
import shutil
import time
from pathlib import Path
from hash_all import hash_all

def backup(source_dir, backup_dir):
    manifest = hash_all(source_dir)
    timestamp = current_time()
    write_manifest(backup_dir, timestamp, manifest)
    copy_files(source_dir, backup_dir, manifest)
    return manifest

"""
When writing the manifest, we check that the backup directory exists, create
it if it does not, and then save the manifest as CSV
"""

def write_manifest(backup_dir, timestamp, manifest):
    backup_dir = Path(backup_dir)
    if not backup_dir.exists():
        backup_dir.mkdir()

    manifest_file = Path(backup_dir, f"{timestamp}.csv")
    with open(manifest_file, "w") as raw:
        writer = csv.writer(raw)
        writer.writerow(["filename", "hash"])
        writer.writerows(manifest)

"""
We then copy those files that haven’t already been saved:
"""

def copy_files(source_dir, backup_dir, manifest):
    for (filename, hash_code) in manifest:
        source_path = Path(source_dir, filename)
        backup_path = Path(backup_dir, f"{hash_code}.bck")
        if not backup_path.exists():
            shutil.copy(source_path, backup_path)

def current_time():
    return f"{time.time()}".split(".")[0]

import sys
from pprint import pprint

if __name__ == '__main__':
    args = sys.argv[1:]
    source_dir = args[0]
    backup_dir = args[1]

    manifest = backup(source_dir, backup_dir)
    pprint(manifest)
