from pathlib import Path


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def list_md_files(directory: Path):
    if not directory.exists():
        return []
    return [f for f in directory.glob("*.md") if f.is_file()]
