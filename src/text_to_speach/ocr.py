import os
import shutil
from collections.abc import Iterator
from pathlib import Path

import pytesseract
from PIL import Image, ImageGrab
from pypdf import PdfReader

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".gif", ".webp"}
PDF_SUFFIX = ".pdf"
WINDOWS_TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")


def _configure_tesseract() -> None:
    if shutil.which("tesseract"):
        return
    configured = os.environ.get("TESSERACT_CMD")
    if configured:
        pytesseract.pytesseract.tesseract_cmd = configured
    elif WINDOWS_TESSERACT.exists():
        pytesseract.pytesseract.tesseract_cmd = str(WINDOWS_TESSERACT)


def collect_images(paths: list[Path]) -> list[tuple[Path, Path]]:
    """Return (root, image) pairs, PDFs included; folders are searched recursively."""
    images: list[tuple[Path, Path]] = []
    for path in paths:
        if path.is_dir():
            images.extend(
                (path, p) for p in sorted(path.rglob("*")) if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES | {PDF_SUFFIX}
            )
        else:
            images.append((path.parent, path))
    return images


def image_to_text(image: Image.Image, lang: str) -> str:
    _configure_tesseract()
    return pytesseract.image_to_string(image, lang=lang).strip()


def pdf_images(path: Path) -> Iterator[Image.Image]:
    """Yield the images embedded in a PDF, in page order."""
    for page in PdfReader(path).pages:
        for embedded in page.images:
            image = embedded.image
            yield image if image.mode in ("1", "L", "RGB", "RGBA") else image.convert("RGB")


def pdf_to_text(path: Path, lang: str) -> str:
    texts = (image_to_text(image, lang) for image in pdf_images(path))
    return "\n\n".join(text for text in texts if text)


def file_to_text(path: Path, lang: str) -> str:
    if path.suffix.lower() == PDF_SUFFIX:
        return pdf_to_text(path, lang)
    with Image.open(path) as image:
        return image_to_text(image, lang)


def clipboard_to_text(lang: str) -> str:
    image = ImageGrab.grabclipboard()
    if not isinstance(image, Image.Image):
        raise SystemExit("Clipboard does not contain an image (use Win+Shift+S first).")
    return image_to_text(image, lang)
