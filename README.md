# Save-O-Clock

A simple screensaver in Python (v3.8) with the [TKinter](https://wiki.python.org/moin/TkInter) package, supports multiple monitors.
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

To build a standalone executable with [PyInstaller](https://www.pyinstaller.org/) use the following command:

```bash
    $ pipenv run pyinstaller save-o-clock.py
```
