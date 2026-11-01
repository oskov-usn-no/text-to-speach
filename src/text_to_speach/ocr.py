import os
import shutil
from pathlib import Path

import pytesseract
from PIL import Image, ImageGrab

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".gif", ".webp"}
WINDOWS_TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")


def _configure_tesseract() -> None:
    if shutil.which("tesseract"):
        return
    configured = os.environ.get("TESSERACT_CMD")
    if configured:
        pytesseract.pytesseract.tesseract_cmd = configured
    elif WINDOWS_TESSERACT.exists():
        pytesseract.pytesseract.tesseract_cmd = str(WINDOWS_TESSERACT)


def collect_images(paths: list[Path]) -> list[Path]:
    images: list[Path] = []
    for path in paths:
        if path.is_dir():
            images.extend(sorted(p for p in path.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES))
        else:
            images.append(path)
    return images


def image_to_text(image: Image.Image, lang: str) -> str:
    _configure_tesseract()
    return pytesseract.image_to_string(image, lang=lang).strip()


def file_to_text(path: Path, lang: str) -> str:
    with Image.open(path) as image:
        return image_to_text(image, lang)


def clipboard_to_text(lang: str) -> str:
    image = ImageGrab.grabclipboard()
    if not isinstance(image, Image.Image):
        raise SystemExit("Clipboard does not contain an image (use Win+Shift+S first).")
    return image_to_text(image, lang)
