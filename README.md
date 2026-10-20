# organize-downloads

Python script that automatically organizes files by extension, moving them into the standard user folders (`~/Pictures`, `~/Videos`, `~/Music`, `~/Documents`, `~/Others`).

Standard library only. No dependencies.

## Features

- Extension-based mapping to destination folders
- Automatically creates destination folders if missing
- Conflict prevention (numeric suffix instead of overwriting)
- `--dry-run` mode to preview without moving anything
- Detailed terminal logs
- Optional `systemd --user` integration to run automatically

## Installation

```bash
mkdir -p ~/.local/bin
cp organize_downloads.py ~/.local/bin/
chmod +x ~/.local/bin/organize_downloads.py
```

Make sure `~/.local/bin` is in your `PATH`:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Usage

```bash
organize_downloads.py                # organizes ~/Downloads
organize_downloads.py -s /path       # organizes another folder
organize_downloads.py --dry-run       # shows what would happen, no moves
organize_downloads.py -v              # verbose logs
```

## Automation (systemd timer)

```bash
mkdir -p ~/.config/systemd/user
cp systemd/organize-downloads.service systemd/organize-downloads.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now organize-downloads.timer
```

Check:

```bash
systemctl --user list-timers organize-downloads.timer
journalctl --user -u organize-downloads.service
```

## Extension mapping

| Category  | Extensions                                                             | Destination    |
|-----------|-------------------------------------------------------------------------|-----------------|
| Images    | png, jpg, jpeg, gif, webp, svg, bmp, tiff, heic, ico, raw                | `~/Pictures`   |
| Videos    | mp4, mkv, avi, mov, webm, flv, wmv, m4v, mpeg                            | `~/Videos`     |
| Audio     | mp3, flac, wav, aac, ogg, m4a, opus, wma                                 | `~/Music`      |
| Documents | pdf, docx, doc, txt, odt, xlsx, xls, pptx, ppt, epub, csv, md, rtf, ods   | `~/Documents`  |
| Other     | any other extension                                                      | `~/Others`     |

## License

MIT. See [LICENSE](LICENSE).
