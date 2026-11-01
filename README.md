# text-to-speach

A small Windows program that:

1. **Reads the text in screenshots** and saves it as a text file (`.txt`) next to each screenshot.
2. **Reads text aloud**, or saves the speech as a sound file (`.wav`).

Polish is the default language for both.

You use it by typing short commands in a terminal window. You can use **Command Prompt** or
**PowerShell**; every command below works in both.

---

## Getting started (one-time setup)

### Step 1: Open Command Prompt

Press **Windows key + R**, type `cmd` and press **Enter**. A black window opens; this is where you type
the commands. Type (or paste with right-click) one line at a time and press **Enter** after each.

### Step 2: Install the two tools the program needs

```
winget install astral-sh.uv
winget install UB-Mannheim.TesseractOCR
```

Answer **Y** if asked to accept terms. When both are done, **close the window and open a new one**
(Step 1 again) so Windows finds the new tools.

> If `winget` is not recognised, install or update **App Installer** from the Microsoft Store and try again.

### Step 3: Add Polish to the text reader

This step needs administrator rights. Click **Start**, type `cmd`, right-click **Command Prompt** and
choose **Run as administrator**. Then paste:

```
curl -L -o "C:\Program Files\Tesseract-OCR\tessdata\pol.traineddata" https://github.com/tesseract-ocr/tessdata/raw/main/pol.traineddata
```

Close the administrator window afterwards.

### Step 4: Add the Polish voice

Open **Settings → Time & language → Speech**. Under *Manage voices*, click **Add voices**, pick
**Polish** and install it.

### Step 5: Download the program

On the project's GitHub page, click the green **Code** button → **Download ZIP**. Unzip it to a folder
you can find again, for example `C:\text-to-speach`.

### Step 6: Prepare the program

In Command Prompt, go to the folder and let it set itself up (the first time takes a minute):

```
cd C:\text-to-speach
uv sync
```

### Step 7: Check that it works

```
uv run tts voices
```

You should see a line with **Polish** (Microsoft Paulina) in it. Setup is done.

---

## Everyday use

Always start by opening Command Prompt and going to the program folder:

```
cd C:\text-to-speach
```

**Tip:** to get a folder's path, open the folder in File Explorer, click the address bar at the top
and copy it. Put paths with spaces in quotes, like `"C:\My screenshots"`.

### Get the text from a folder of screenshots

```
uv run tts ocr "C:\My screenshots"
```

Every screenshot in the folder, **including all subfolders**, gets a `.txt` file with the same name
right next to it, e.g. `Screenshot 1.png` → `Screenshot 1.txt`.

Added more screenshots later? Only do the new ones:

```
uv run tts ocr "C:\My screenshots" --skip-existing
```

### Read a text file aloud

```
uv run tts speak "C:\My screenshots\Screenshot 1.txt"
```

### Do both at once (get the text and read it aloud)

```
uv run tts run "C:\My screenshots\Screenshot 1.png"
```

### Save the speech as sound files instead of playing it

Add `--save` to `run` or `speak`. A `.wav` file is saved next to each text file:

```
uv run tts run "C:\My screenshots" --save
```

### Use a screenshot you just took

Press **Windows key + Shift + S**, select an area of the screen, then:

```
uv run tts run --clipboard
```

The text is saved in the `output` folder inside the program folder.

### Stop reading aloud

Press **Ctrl + C** in the Command Prompt window.

---

## Options

| Option | What it does |
|---|---|
| `--skip-existing` | Skip screenshots that already have a `.txt` file |
| `--save` | Save speech as `.wav` instead of playing it |
| `--out "C:\Text"` | Put the text files in another folder (keeps the same subfolders) |
| `--lang pol` | Language of the screenshot text (default `pol`). Combine with `+`, e.g. `pol+eng` |
| `--voice Polish` | Which voice to use (default `Polish`). See `uv run tts voices` |
| `--rate 150` | Speaking speed in words per minute |

Other languages need their own language file in Step 3 (replace `pol` with e.g. `eng` or `nor`) and
their own voice in Step 4. Example for Norwegian: `uv run tts run "C:\Shots" --lang nor --voice Jon`.

## Troubleshooting

| Message | Fix |
|---|---|
| `'uv' is not recognized` | Close Command Prompt and open a new one. If it persists, repeat Step 2. |
| `tesseract is not installed or it's not in your PATH` | Repeat Step 2. If Tesseract is installed elsewhere, set `TESSERACT_CMD` to the full path of `tesseract.exe`. |
| `Failed loading language 'pol'` | Repeat Step 3. |
| `No voice matching 'Polish'` | Repeat Step 4, then check with `uv run tts voices`. |
| `Clipboard does not contain an image` | Take the screenshot with Windows key + Shift + S first. |

---

## For developers

```
git clone git@github.com:oskov-usn-no/text-to-speach.git
uv sync
uv run pytest
```

See `AGENTS.md` for project layout and conventions.
