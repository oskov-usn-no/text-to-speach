from pathlib import Path

from text_to_speach.cli import _text_target
from text_to_speach.ocr import collect_images


def test_collect_images_recurses_and_filters(tmp_path: Path) -> None:
    (tmp_path / "a.png").touch()
    (tmp_path / "b.txt").touch()
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "c.JPG").touch()
    found = collect_images([tmp_path])
    assert [(root, image.relative_to(tmp_path).as_posix()) for root, image in found] == [
        (tmp_path, "a.png"),
        (tmp_path, "sub/c.JPG"),
    ]


def test_text_target_next_to_image(tmp_path: Path) -> None:
    image = tmp_path / "sub" / "shot.png"
    assert _text_target(tmp_path, image, None) == tmp_path / "sub" / "shot.txt"


def test_text_target_mirrors_structure_under_out(tmp_path: Path) -> None:
    image = tmp_path / "in" / "sub" / "shot.png"
    out = tmp_path / "out"
    assert _text_target(tmp_path / "in", image, out) == out / "sub" / "shot.txt"
