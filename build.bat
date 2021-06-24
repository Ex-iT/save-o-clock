@echo off
pipenv run pyinstaller save-o-clock.py ^
    --nowindowed ^
    --noconsole ^
    --icon "save-o-clock.ico" ^
    --add-binary "save-o-clock.ico;." ^
    --noupx ^
    --noconfirm

ren ".\dist\save-o-clock\save-o-clock.exe" "save-o-clock.scr"

