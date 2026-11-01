import argparse
from datetime import datetime
from pathlib import Path

from text_to_speach import ocr, tts


def _text_target(root: Path, image: Path, out: Path | None) -> Path:
    if out is None:
        return image.with_suffix(".txt")
    return out / image.relative_to(root).with_suffix(".txt")


def _ocr_to_files(args: argparse.Namespace) -> list[Path]:
    written: list[Path] = []
    if args.clipboard:
        folder = args.out or Path("output")
        folder.mkdir(parents=True, exist_ok=True)
        target = folder / f"clipboard-{datetime.now():%Y%m%d-%H%M%S}.txt"
        target.write_text(ocr.clipboard_to_text(args.lang), encoding="utf-8")
        written.append(target)
    for root, image in ocr.collect_images(args.images):
        target = _text_target(root, image, args.out)
        if args.skip_existing and target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(ocr.file_to_text(image, args.lang), encoding="utf-8")
        written.append(target)
    for path in written:
        print(path)
    return written


def _speak_files(files: list[Path], args: argparse.Namespace) -> None:
    for path in files:
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            continue
        if args.save:
            tts.save(text, path.with_suffix(".wav"), args.voice, args.rate)
            print(path.with_suffix(".wav"))
        else:
            tts.speak(text, args.voice, args.rate)


def cmd_ocr(args: argparse.Namespace) -> None:
    _ocr_to_files(args)


def cmd_speak(args: argparse.Namespace) -> None:
    _speak_files(args.files, args)


def cmd_run(args: argparse.Namespace) -> None:
    _speak_files(_ocr_to_files(args), args)


def cmd_voices(_: argparse.Namespace) -> None:
    for voice_id, name in tts.list_voices():
        print(f"{name}\t{voice_id}")


def _add_ocr_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("images", nargs="*", type=Path, help="Image files or folders (searched recursively)")
    parser.add_argument("--clipboard", action="store_true", help="OCR the image on the clipboard")
    parser.add_argument("--lang", default="pol", help="Tesseract languages, e.g. pol, nor, pol+eng (default: pol)")
    parser.add_argument(
        "--out",
        type=Path,
        help="Write .txt files here, mirroring the folder structure (default: next to each image; "
        "clipboard text goes to 'output')",
    )
    parser.add_argument("--skip-existing", action="store_true", help="Skip images that already have a .txt")


def _add_tts_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--voice", default="Polish", help="Part of a voice name or id (default: Polish, see 'tts voices')")
    parser.add_argument("--rate", type=int, help="Words per minute")
    parser.add_argument("--save", action="store_true", help="Write .wav next to each .txt instead of speaking")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="tts", description="Screenshot OCR and text-to-speech")
    sub = parser.add_subparsers(required=True)

    p_ocr = sub.add_parser("ocr", help="OCR screenshots to .txt files")
    _add_ocr_args(p_ocr)
    p_ocr.set_defaults(func=cmd_ocr)

    p_speak = sub.add_parser("speak", help="Read .txt files aloud")
    p_speak.add_argument("files", nargs="+", type=Path)
    _add_tts_args(p_speak)
    p_speak.set_defaults(func=cmd_speak)

    p_run = sub.add_parser("run", help="OCR screenshots, then read the text aloud")
    _add_ocr_args(p_run)
    _add_tts_args(p_run)
    p_run.set_defaults(func=cmd_run)

    p_voices = sub.add_parser("voices", help="List installed voices")
    p_voices.set_defaults(func=cmd_voices)

    args = parser.parse_args(argv)
    if getattr(args, "images", None) == [] and not getattr(args, "clipboard", True):
        parser.error("give image paths or --clipboard")
    args.func(args)
