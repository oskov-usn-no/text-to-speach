# text-to-speach

Two features:

1. **OCR**: reads screenshots (files, folders, or the clipboard) and saves the text as `.txt`.
2. **Text-to-speech**: reads the text aloud with the Windows voices, or saves it as `.wav`.

## Prerequisites (Windows)

```powershell
winget install astral-sh.uv
winget install UB-Mannheim.TesseractOCR
```

OCR defaults to Polish and needs `pol.traineddata` (add `nor.traineddata` for Norwegian). Choose them
under "Additional language data" in the Tesseract installer, or download them from
https://github.com/tesseract-ocr/tessdata into `C:\Program Files\Tesseract-OCR\tessdata`.
If Tesseract is not on PATH or in its default location, set `TESSERACT_CMD` to the full path of `tesseract.exe`.

Speech defaults to the Polish voice (Microsoft Paulina). Install it under Settings → Time & language →
Speech → Add voices → Polish. Use `--voice` to pick another, e.g. `--voice Jon` for Norwegian.

## Usage

```powershell
uv sync
uv run tts ocr "$env:USERPROFILE\Pictures\Screenshots"   # -> output\*.txt
uv run tts ocr --clipboard                                # after Win+Shift+S
uv run tts speak output\screenshot1.txt
uv run tts run --clipboard                               # OCR + read aloud (Polish)
uv run tts run --clipboard --lang nor --voice Jon        # Norwegian
uv run tts run shot.png --save                            # writes output\shot.wav
uv run tts voices
```

Options: `--lang` (default `pol`, combine with `+`, e.g. `pol+eng`), `--out` (default `output`), `--voice` (default `Polish`), `--rate`.

## Tests

```powershell
uv run pytest
```
