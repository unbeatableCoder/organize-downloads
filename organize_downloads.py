#!/usr/bin/env python3

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from pathlib import Path

EXTENSION_MAP: dict[str, str] = {
    ".png": "Pictures", ".jpg": "Pictures", ".jpeg": "Pictures",
    ".gif": "Pictures", ".webp": "Pictures", ".svg": "Pictures",
    ".bmp": "Pictures", ".tiff": "Pictures", ".heic": "Pictures",
    ".ico": "Pictures", ".raw": "Pictures",
    ".mp4": "Videos", ".mkv": "Videos", ".avi": "Videos",
    ".mov": "Videos", ".webm": "Videos", ".flv": "Videos",
    ".wmv": "Videos", ".m4v": "Videos", ".mpeg": "Videos",
    ".mp3": "Music", ".flac": "Music", ".wav": "Music",
    ".aac": "Music", ".ogg": "Music", ".m4a": "Music",
    ".opus": "Music", ".wma": "Music",
    ".pdf": "Documents", ".docx": "Documents", ".doc": "Documents",
    ".txt": "Documents", ".odt": "Documents", ".xlsx": "Documents",
    ".xls": "Documents", ".pptx": "Documents", ".ppt": "Documents",
    ".epub": "Documents", ".csv": "Documents", ".md": "Documents",
    ".rtf": "Documents", ".ods": "Documents",
}

DEFAULT_CATEGORY = "Others"
HOME = Path.home()

logger = logging.getLogger("organize_downloads")


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s",
                                            datefmt="%H:%M:%S"))
    logger.setLevel(level)
    logger.addHandler(handler)


def resolve_destination_dir(category: str) -> Path:
    dest = HOME / category
    dest.mkdir(parents=True, exist_ok=True)
    return dest


def safe_destination_path(dest_dir: Path, filename: str) -> Path:
    candidate = dest_dir / filename
    if not candidate.exists():
        return candidate

    stem = candidate.stem
    suffix = candidate.suffix
    counter = 1
    while True:
        new_candidate = dest_dir / f"{stem}_{counter}{suffix}"
        if not new_candidate.exists():
            return new_candidate
        counter += 1


def categorize(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    return EXTENSION_MAP.get(ext, DEFAULT_CATEGORY)


def organize(source_dir: Path, dry_run: bool) -> tuple[int, int]:
    if not source_dir.is_dir():
        logger.error("Source folder does not exist: %s", source_dir)
        sys.exit(1)

    moved = 0
    failed = 0

    for entry in sorted(source_dir.iterdir()):
        if not entry.is_file():
            continue

        category = categorize(entry)
        dest_dir = resolve_destination_dir(category)
        dest_path = safe_destination_path(dest_dir, entry.name)

        if dry_run:
            logger.info("[DRY-RUN] %s -> %s", entry, dest_path)
            moved += 1
            continue

        try:
            shutil.move(str(entry), str(dest_path))
            logger.info("Moved: %s -> %s", entry, dest_path)
            moved += 1
        except (OSError, shutil.Error) as exc:
            logger.error("Failed to move %s: %s", entry, exc)
            failed += 1

    return moved, failed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Organizes files by extension into the standard user folders."
    )
    parser.add_argument(
        "-s", "--source",
        type=Path,
        default=HOME / "Downloads",
        help="Source folder (default: ~/Downloads)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without moving anything",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose logging (DEBUG)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(args.verbose)

    mode = "DRY-RUN" if args.dry_run else "REAL"
    logger.info("Starting (%s) | source: %s", mode, args.source)

    moved, failed = organize(args.source.expanduser().resolve(), args.dry_run)

    logger.info("Done. Files processed: %d | failures: %d", moved, failed)
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
