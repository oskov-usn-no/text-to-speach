# text-to-speach

CLI (`tts`) that OCRs screenshots to `.txt` and reads text aloud. Target platform is **Windows**;
the agent container is Linux and can only run unit tests.

## Layout
- `src/text_to_speach/cli.py` — argparse CLI: `ocr`, `speak`, `run` (ocr + speak), `voices`.
- `src/text_to_speach/ocr.py` — Tesseract via `pytesseract`; files, folders, or clipboard (`PIL.ImageGrab`).
- `src/text_to_speach/tts.py` — `pyttsx3` (SAPI5 on Windows): speak or save `.wav`.
- `tests/` — pytest; only tests that don't need Tesseract or a TTS engine.

## Commands
```
uv sync
uv run pytest
uv run tts --help
```

## Conventions
- Python 3.12, uv for dependencies (`uv add`, never pip). Keep dependencies pip-installable on Windows
  without build tools.
- Defaults are Polish: OCR `--lang pol`, speech `--voice Polish` (Microsoft Paulina). Keep README in
  sync when changing defaults or options.
- Text files are read and written as UTF-8.
- Tesseract is an external install (`winget install UB-Mannheim.TesseractOCR`); lookup order is PATH,
  `TESSERACT_CMD`, then `C:\Program Files\Tesseract-OCR\tesseract.exe`.

## Testing limits
- Tesseract, clipboard image grab and SAPI5 voices are unavailable in the agent container. Don't
  install them to "test" here; tell the user what to verify on Windows instead.
