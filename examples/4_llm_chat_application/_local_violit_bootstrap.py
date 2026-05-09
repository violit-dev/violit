from pathlib import Path
import sys


def bootstrap_local_violit() -> None:
    src_path = Path(__file__).resolve().parents[2] / "src"
    src_text = str(src_path)
    if src_text not in sys.path:
        sys.path.insert(0, src_text)