#!/usr/bin/env python3
"""
Safe duplicate file/folder cleaner.
DRY-RUN by default. Use --delete to actually remove files.
"""

import os
import sys
import hashlib
import argparse
from collections import defaultdict
from pathlib import Path


def md5(filepath):
    """Return MD5 hash of file contents."""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def find_duplicate_files(root, exclude_git=True):
    """Find files with identical content. Returns dict: hash -> [paths]."""
    hashes = defaultdict(list)
    root = Path(root).resolve()

    for filepath in root.rglob("*"):
        if not filepath.is_file():
            continue
        if exclude_git and ".git" in filepath.parts:
            continue
        try:
            file_hash = md5(filepath)
            hashes[file_hash].append(filepath)
        except (PermissionError, OSError):
            continue

    # Return only groups with 2+ files
    return {h: paths for h, paths in hashes.items() if len(paths) > 1}


def find_duplicate_folders(root, exclude_git=True):
    """Find folders with identical names in different locations."""
    names = defaultdict(list)
    root = Path(root).resolve()

    for dirpath in root.rglob("*/"):
        if exclude_git and ".git" in dirpath.parts:
            continue
        names[dirpath.name].append(dirpath)

    return {name: paths for name, paths in names.items() if len(paths) > 1}


def find_duplicate_readmes(root, exclude_git=True):
    """Find all README* files except root README.md."""
    root = Path(root).resolve()
    readmes = []

    for filepath in root.rglob("README*"):
        if not filepath.is_file():
            continue
        if exclude_git and ".git" in filepath.parts:
            continue
        if filepath.name.lower() != "readme.md" or filepath.parent != root:
            readmes.append(filepath)

    return readmes


def main():
    parser = argparse.ArgumentParser(description="Find and optionally delete duplicate files/folders")
    parser.add_argument("--path", default=".", help="Root directory to scan (default: current)")
    parser.add_argument("--delete", action="store_true", help="ACTUALLY DELETE files (default is dry-run)")
    parser.add_argument("--folders", action="store_true", help="Also scan for duplicate folder names")
    parser.add_argument("--readmes", action="store_true", help="Also scan for duplicate READMEs")
    args = parser.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f"❌ Path not found: {root}")
        sys.exit(1)

    mode = "🔴 DELETE MODE" if args.delete else "🟡 DRY-RUN MODE (use --delete to remove)"
    print(f"\n{'='*60}")
    print(f"  Duplicate Cleaner — {mode}")
    print(f"  Scanning: {root.resolve()}")
    print(f"{'='*60}\n")

    # ===== Duplicate Files =====
    dup_files = find_duplicate_files(root)
    if dup_files:
        print(f"📁 DUPLICATE FILES FOUND: {len(dup_files)} groups")
        for h, paths in dup_files.items():
            print(f"\n  Hash: {h}")
            print(f"  Keep: {paths[0]}")
            for p in paths[1:]:
                print(f"  {'DELETE' if args.delete else 'WOULD DELETE'}: {p}")
                if args.delete:
                    try:
                        os.remove(p)
                        print(f"    ✅ Deleted")
                    except Exception as e:
                        print(f"    ❌ Error: {e}")
    else:
        print("✅ No duplicate files found.")

    # ===== Duplicate Folders =====
    if args.folders:
        dup_folders = find_duplicate_folders(root)
        if dup_folders:
            print(f"\n📂 DUPLICATE FOLDER NAMES FOUND: {len(dup_folders)} groups")
            for name, paths in dup_folders.items():
                print(f"\n  Name: {name}")
                print(f"  Keep: {paths[0]}")
                for p in paths[1:]:
                    print(f"  {'DELETE' if args.delete else 'WOULD DELETE'}: {p}")
                    if args.delete:
                        try:
                            import shutil
                            shutil.rmtree(p)
                            print(f"    ✅ Deleted")
                        except Exception as e:
                            print(f"    ❌ Error: {e}")
        else:
            print("\n✅ No duplicate folder names found.")

    # ===== Duplicate READMEs =====
    if args.readmes:
        dup_readmes = find_duplicate_readmes(root)
        if dup_readmes:
            print(f"\n📄 DUPLICATE READMEs FOUND: {len(dup_readmes)}")
            for p in dup_readmes:
                print(f"  {'DELETE' if args.delete else 'WOULD DELETE'}: {p}")
                if args.delete:
                    try:
                        os.remove(p)
                        print(f"    ✅ Deleted")
                    except Exception as e:
                        print(f"    ❌ Error: {e}")
        else:
            print("\n✅ No duplicate READMEs found.")

    print(f"\n{'='*60}")
    if not args.delete:
        print("  💡 Run with --delete to actually remove files")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
