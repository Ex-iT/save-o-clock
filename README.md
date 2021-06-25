# Save-O-Clock

A simple Windows Screen Saver (Win32 Screen Saver v4.0+) Python (v3.9) with the [pywin32](https://pypi.org/project/pywin32/) and [TKinter](https://wiki.python.org/moin/TkInter) packages, supports multiple monitors.
Displays a 24-hour clock (using [JetBrains Mono](https://www.jetbrains.com/lp/mono/) font) in the center of the screen.
Closes on mouse movement or any keyboard input.

## Development

First install all dependencies of this project using [pipenv](https://pypi.org/project/pipenv/) with the following command:

```bash
$ pipenv install --dev
```

This will automatically create a virtual environment to work in.

To start the application run:

```bash
$ pipenv run python save-o-clock.py
```

## Standalone application

To build a standalone executable (rename `.exe` to `.scr`) with [PyInstaller](https://www.pyinstaller.org/) use the following command (or run `build.bat`):

```powershell
pipenv run pyinstaller save-o-clock.py `
    --nowindowed `
    --noconsole `
    --icon "save-o-clock.ico" `
    --add-binary "save-o-clock.ico;." `
    --noupx `
    --onedir `
    --clean `
    --noconfirm; `
    mv .\dist\save-o-clock\save-o-clock.exe .\dist\save-o-clock\save-o-clock.scr
```

## Settings

When a `settings.json` file exists in the same directory as the `.scr` file it will try to take the settings from that file.
If it doesn't exist it will try fall back to it's defaults.

An example of a `settings.json` file (default settings):
```json
{
    "time_format": "%H:%M",
    "font_family": "JetBrains Mono",
    "font_size": 200,
    "foreground_color": "white",
    "background_color": "black"
}
```

## Attribution

Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
