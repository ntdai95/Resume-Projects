from pathlib import Path
from app.ingestion.hashing import sha256_file


def test_sha256_file(tmp_path: Path):
    p = tmp_path/"sample.txt"
    p.write_text("hello")
    assert len(sha256_file(p)) == 64
