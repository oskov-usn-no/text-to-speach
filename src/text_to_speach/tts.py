from pathlib import Path

import pyttsx3


def list_voices() -> list[tuple[str, str]]:
    engine = pyttsx3.init()
    return [(voice.id, voice.name) for voice in engine.getProperty("voices")]


def _engine(voice: str | None, rate: int | None) -> pyttsx3.Engine:
    engine = pyttsx3.init()
    if voice:
        match = next(
            (v for v in engine.getProperty("voices") if voice.lower() in (v.id + v.name).lower()),
            None,
        )
        if match is None:
            raise SystemExit(f"No voice matching '{voice}'. Run 'tts voices' to list them.")
        engine.setProperty("voice", match.id)
    if rate:
        engine.setProperty("rate", rate)
    return engine


def speak(text: str, voice: str | None = None, rate: int | None = None) -> None:
    engine = _engine(voice, rate)
    engine.say(text)
    engine.runAndWait()


def save(text: str, out: Path, voice: str | None = None, rate: int | None = None) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    engine = _engine(voice, rate)
    engine.save_to_file(text, str(out))
    engine.runAndWait()
