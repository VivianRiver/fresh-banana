#!/usr/bin/env python3
"""
Resize Fresh Banana photos, recursively.

Finds every .jpg under the input folder (including all subfolders), resizes it
to a square, and writes it to the output folder, mirroring the subfolder
structure. Originals are never modified.

    input:   fresh-banana/day-01/b01_d01_1.jpg
    output:  resized_224/day-01/b01_d01_1.jpg

Usage:
    python resize_bananas.py <input_root> <output_root> [--size 224] [--quality 95]
                                                       [--flat] [--overwrite]

Examples:
    python resize_bananas.py ~/fresh-banana ~/fresh-banana-resized/512 --size 512
    python resize_bananas.py ~/fresh-banana ~/fresh-banana-resized/224 --size 224
    python resize_bananas.py ~/fresh-banana ~/fresh-banana-resized/224_flat --size 224 --flat

Requires Pillow:  pip install pillow
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps

IMAGE_SUFFIXES = {".jpg", ".jpeg"}


def pad_to_square(img):
    """Safety net: pad a non-square image to square using its average border color.
    Your photos are shot 1:1, so this should never actually run."""
    w, h = img.size
    if w == h:
        return img
    border = [img.getpixel((x, 0)) for x in range(w)]
    border += [img.getpixel((x, h - 1)) for x in range(w)]
    border += [img.getpixel((0, y)) for y in range(h)]
    border += [img.getpixel((w - 1, y)) for y in range(h)]
    fill = tuple(sum(c[i] for c in border) // len(border) for i in range(3))
    side = max(w, h)
    canvas = Image.new("RGB", (side, side), fill)
    canvas.paste(img, ((side - w) // 2, (side - h) // 2))
    return canvas


def resize_one(src, dst, size, quality):
    """Resize one image. Returns a warning string if something was unusual."""
    warning = None
    with Image.open(src) as img:
        # Apply EXIF orientation so pixels match what you see in the gallery
        img = ImageOps.exif_transpose(img).convert("RGB")
        if img.width != img.height:
            warning = f"{src} was {img.width}x{img.height}, padded to square"
            img = pad_to_square(img)
        # LANCZOS antialiases when downscaling, preventing shimmer on the cork texture
        img = img.resize((size, size), Image.LANCZOS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        img.save(dst, "JPEG", quality=quality)
    return warning


def main():
    parser = argparse.ArgumentParser(description="Recursively resize banana photos to a square size.")
    parser.add_argument("input_root", help="Top folder to search (all subfolders included)")
    parser.add_argument("output_root", help="Folder to write resized copies into")
    parser.add_argument("--size", type=int, default=224, help="Output side length in pixels (default: 224)")
    parser.add_argument("--quality", type=int, default=95, help="JPEG quality 1-100 (default: 95)")
    parser.add_argument("--flat", action="store_true",
                        help="Write every image directly into output_root instead of mirroring subfolders")
    parser.add_argument("--overwrite", action="store_true", help="Replace files that already exist in the output")
    args = parser.parse_args()

    in_root = Path(args.input_root).expanduser().resolve()
    out_root = Path(args.output_root).expanduser().resolve()

    if not in_root.is_dir():
        sys.exit(f"Error: {in_root} is not a directory")
    if out_root == in_root:
        sys.exit("Error: output_root must differ from input_root so originals are never touched")

    # Find all images under input_root, but skip anything already inside output_root
    # (in case you put the output folder inside the input folder)
    files = sorted(
        p for p in in_root.rglob("*")
        if p.is_file()
        and p.suffix.lower() in IMAGE_SUFFIXES
        and out_root not in p.resolve().parents
    )
    if not files:
        sys.exit(f"No .jpg files found under {in_root}")

    # Map each source file to its destination path
    jobs = []
    for src in files:
        if args.flat:
            dst = out_root / (src.stem + ".jpg")
        else:
            dst = out_root / src.relative_to(in_root).with_suffix(".jpg")
        jobs.append((src, dst))

    # In flat mode, two files with the same name would overwrite each other. Catch that up front.
    if args.flat:
        seen = {}
        for src, dst in jobs:
            if dst in seen:
                sys.exit(f"Error: name collision in --flat mode:\n  {seen[dst]}\n  {src}\n"
                         "Rename one of them, or run without --flat.")
            seen[dst] = src

    print(f"Found {len(jobs)} images under {in_root}")

    done, skipped, warnings, errors = 0, 0, [], []
    for i, (src, dst) in enumerate(jobs, start=1):
        if dst.exists() and not args.overwrite:
            skipped += 1
        else:
            try:
                w = resize_one(src, dst, args.size, args.quality)
                if w:
                    warnings.append(w)
                done += 1
            except Exception as e:
                errors.append(f"{src}: {e}")
        if i % 50 == 0 or i == len(jobs):
            print(f"  {i}/{len(jobs)} processed")

    print(f"\nResized {done} files to {args.size}x{args.size} in {out_root}")
    if skipped:
        print(f"Skipped {skipped} existing files (use --overwrite to replace)")
    for w in warnings:
        print(f"  Warning: {w}")
    for e in errors:
        print(f"  Error: {e}")


if __name__ == "__main__":
    main()
