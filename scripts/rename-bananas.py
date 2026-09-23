#!/usr/bin/env python3
"""
Rename daily banana photos from camera timestamps to project convention.

Usage:
    python rename_bananas.py <day_directory> <day_number> [--bananas N]

Example:
    python rename_bananas.py ~/fresh-banana/day-01 1
    python rename_bananas.py ~/fresh-banana/day-01 1 --bananas 16

Expects the directory to contain exactly (bananas * 4) jpg files.
Files are sorted by name (which sorts by timestamp), then renamed:
    b01_d01_1.jpg  b01_d01_2.jpg  b01_d01_3.jpg  b01_d01_4.jpg
    b02_d01_1.jpg  ...
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Rename banana photos to project convention.")
    parser.add_argument("day_dir", type=str, help="Path to the day's photo directory")
    parser.add_argument("day_num", type=int, help="Day number (1, 2, 3, ...)")
    parser.add_argument("--bananas", type=int, default=16, help="Number of bananas (default: 16)")
    parser.add_argument("--shots", type=int, default=4, help="Shots per banana (default: 4)")
    parser.add_argument("--dry-run", action="store_true", help="Show renames without executing")
    args = parser.parse_args()

    day_dir = Path(args.day_dir).expanduser().resolve()
    if not day_dir.is_dir():
        print(f"Error: {day_dir} is not a directory")
        sys.exit(1)

    expected = args.bananas * args.shots
    jpg_files = sorted(day_dir.glob("*.jpg"))

    if len(jpg_files) != expected:
        print(f"Error: expected {expected} jpg files ({args.bananas} bananas x {args.shots} shots)")
        print(f"Found {len(jpg_files)}")
        sys.exit(1)

    renames = []
    for i, old_path in enumerate(jpg_files):
        banana_num = (i // args.shots) + 1
        shot_num = (i % args.shots) + 1
        new_name = f"b{banana_num:02d}_d{args.day_num:02d}_{shot_num}.jpg"
        new_path = day_dir / new_name
        renames.append((old_path, new_path))

    for old_path, new_path in renames:
        if new_path.exists() and new_path != old_path:
            print(f"Error: {new_path.name} already exists. Aborting.")
            sys.exit(1)

    for old_path, new_path in renames:
        if args.dry_run:
            print(f"  {old_path.name}  ->  {new_path.name}")
        else:
            old_path.rename(new_path)

    if args.dry_run:
        print(f"\nDry run: {len(renames)} files would be renamed.")
    else:
        print(f"Renamed {len(renames)} files.")


if __name__ == "__main__":
    main()
