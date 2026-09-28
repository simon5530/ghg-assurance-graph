#!/usr/bin/env python3
"""Copy only intended Git publication scope; inspect historical blobs without leaking content."""

import argparse
import re
import shutil
import subprocess
from pathlib import Path


def git(*args):
    return subprocess.check_output(["git", *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    args.destination.mkdir(parents=True, exist_ok=False)
    paths = set(git("ls-files", "-z").decode().split("\0"))
    paths.update(git("ls-files", "--others", "--exclude-standard", "-z").decode().split("\0"))
    patterns = [rb"/U[s]ers/", rb"/h[o]me/[a-z]", rb"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"]
    findings = []
    count = 0
    for name in sorted(paths - {""}):
        path = Path(name)
        if not path.is_file():
            continue
        if path.is_symlink():
            raise SystemExit("symlink in publication scope")
        data = path.read_bytes()
        if path.suffix.lower() == ".pdf":
            findings.append(name + ": source PDF not permitted")
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            findings.append(name + ": binary requires manual review")
        if any(re.search(p, data) for p in patterns):
            findings.append(name + ": potential private material; inspect locally")
        dest = args.destination / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
        count += 1
    objects = git("rev-list", "--objects", "--all").decode().splitlines()
    blobs = 0
    for line in objects:
        oid = line.split()[0]
        if git("cat-file", "-t", oid).strip() != b"blob":
            continue
        blobs += 1
        data = git("cat-file", "blob", oid)
        if any(re.search(p, data) for p in patterns):
            findings.append(oid + ": historical private-material candidate")
    print(f"Inspected {count} publication files and {blobs} historical blobs")
    for finding in findings:
        print(finding)
    if findings:
        raise SystemExit(1)
    print("Targeted semantic scan clear; not a substitute for human diff/license review")


if __name__ == "__main__":
    main()
