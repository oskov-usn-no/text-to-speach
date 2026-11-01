from pathlib import Path

from text_to_speach.ocr import collect_images


def test_collect_images_filters_folder(tmp_path: Path) -> None:
    (tmp_path / "a.png").touch()
    (tmp_path / "b.txt").touch()
    (tmp_path / "c.JPG").touch()
    assert [p.name for p in collect_images([tmp_path])] == ["a.png", "c.JPG"]
