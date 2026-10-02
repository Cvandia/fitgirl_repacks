"""Validate snapshots and retain only the latest complete CSV."""

import argparse
import csv
import re
from datetime import UTC, datetime
from pathlib import Path

HEADER = ["ID", "标题", "时间", "链接", "封面", "说明", "简介"]
SNAPSHOT = re.compile(r"repacks-(\d{14})\.csv")
ROOT = Path(__file__).resolve().parent.parent


def validate_csv(path, minimum_count):
    seen = set()
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        if next(reader, None) != HEADER:
            raise ValueError("CSV header mismatch")
        for row in reader:
            if len(row) != len(HEADER):
                raise ValueError("Invalid column count")
            if not row[0] or row[0] in seen or not row[1].strip():
                raise ValueError("Missing title or missing/duplicate ID")
            datetime.fromisoformat(row[2])
            if not row[3].startswith("magnet:?"):
                raise ValueError("Invalid magnet link")
            seen.add(row[0])
    if not seen or len(seen) < minimum_count:
        raise ValueError(f"Incomplete snapshot: {len(seen)} < {minimum_count}")
    return len(seen)


def cleanup(root=ROOT, dry_run=False):
    root = Path(root).resolve()
    data_dir = (root / "data").resolve()
    if data_dir.parent != root:
        raise ValueError("Data directory must stay inside project")
    minimum_count = int((root / "spider/config.txt").read_text(encoding="utf-8").strip())
    if minimum_count <= 0:
        raise ValueError("Invalid previous complete count")
    snapshots = []
    for path in data_dir.glob("repacks-*.csv"):
        match = SNAPSHOT.fullmatch(path.name)
        if not match:
            continue
        datetime.strptime(match[1], "%Y%m%d%H%M%S").replace(tzinfo=UTC)
        if path.is_symlink() or path.resolve().parent != data_dir:
            raise ValueError(f"Unsafe snapshot path: {path}")
        snapshots.append(path)
    snapshots.sort(reverse=True)
    keep = None
    for path in snapshots:
        try:
            count = validate_csv(path, minimum_count)
        except (ValueError, csv.Error, UnicodeError) as error:
            print(f"Skip invalid snapshot {path.name}: {error}")
            continue
        keep = path
        break
    if keep is None:
        raise ValueError("No complete snapshot; nothing deleted")

    version = SNAPSHOT.fullmatch(keep.name)[1]
    # Regenerate the page before deletion so it never references an old CSV.
    template = (root / "spider/template.txt").read_text(encoding="utf-8")
    html = template.replace("{{lastupdated}}", version)
    html = html.replace("year-month-day", f"{version[:4]}-{version[4:6]}-{version[6:8]}")
    if f"data/{keep.name}" not in html or "{{lastupdated}}" in html:
        raise ValueError("Template does not reference retained snapshot")
    remove = [path for path in snapshots if path != keep]
    reclaimed = sum(path.stat().st_size for path in remove)
    print(f"Keep {keep.name}: {count} rows; remove {len(remove)} CSVs ({reclaimed / 1024**3:.2f} GiB)")
    if dry_run:
        return keep
    temporary = root / "index.htm.tmp"
    temporary.write_text(html, encoding="utf-8")
    temporary.replace(root / "index.htm")
    for path in remove:
        path.unlink()
    return keep


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Validate and preview without writing or deleting")
    cleanup(dry_run=parser.parse_args().dry_run)
