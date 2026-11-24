from pathlib import Path

from text_to_speach.cli import _collect_texts, _text_target
from PIL import Image

from text_to_speach import ocr
from text_to_speach.ocr import collect_images


def test_collect_images_recurses_and_filters(tmp_path: Path) -> None:
    (tmp_path / "a.png").touch()
    (tmp_path / "b.txt").touch()
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "c.JPG").touch()
    (tmp_path / "sub" / "d.PDF").touch()
    found = collect_images([tmp_path])
    assert [(root, image.relative_to(tmp_path).as_posix()) for root, image in found] == [
        (tmp_path, "a.png"),
        (tmp_path, "sub/c.JPG"),
        (tmp_path, "sub/d.PDF"),
    ]


def test_text_target_next_to_image(tmp_path: Path) -> None:
    image = tmp_path / "sub" / "shot.png"
    assert _text_target(tmp_path, image, None) == tmp_path / "sub" / "shot.txt"


def test_text_target_mirrors_structure_under_out(tmp_path: Path) -> None:
    image = tmp_path / "in" / "sub" / "shot.png"
    out = tmp_path / "out"
    assert _text_target(tmp_path / "in", image, out) == out / "sub" / "shot.txt"


def test_collect_texts_recurses_and_filters(tmp_path: Path) -> None:
    (tmp_path / "a.txt").touch()
    (tmp_path / "b.png").touch()
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "c.TXT").touch()
    found = _collect_texts([tmp_path])
    assert [p.relative_to(tmp_path).as_posix() for p in found] == ["a.txt", "sub/c.TXT"]


def test_collect_texts_keeps_files_as_given(tmp_path: Path) -> None:
    single = tmp_path / "x.md"
    assert _collect_texts([single]) == [single]


def test_pdf_to_text_ocrs_embedded_images_in_order(tmp_path: Path, monkeypatch) -> None:
    pdf = tmp_path / "doc.pdf"
    pages = [Image.new("RGB", (40, 20), "red"), Image.new("CMYK", (40, 20)), Image.new("L", (40, 20), 255)]
    pages[0].save(pdf, save_all=True, append_images=pages[1:])
    seen: list[str] = []

    def fake_ocr(image: Image.Image, lang: str) -> str:
        seen.append(image.mode)
        return "" if len(seen) == 2 else f"text{len(seen)}"

    monkeypatch.setattr(ocr, "image_to_text", fake_ocr)
    assert ocr.file_to_text(pdf, "pol") == "text1\n\ntext3"
    assert seen == ["RGB", "RGB", "L"]
