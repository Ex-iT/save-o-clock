@echo off
pipenv run pyinstaller save-o-clock.py ^
    --nowindowed ^
    --noconsole ^
    --icon "save-o-clock.ico" ^
    --add-binary "save-o-clock.ico;." ^
    --add-binary "settings.json;." ^
    --noupx ^
    --onedir ^
    --clean ^
    --noconfirm

ren ".\dist\save-o-clock\save-o-clock.exe" "save-o-clock.scr"
ren ".\dist\save-o-clock\save-o-clock.exe.manifest" "save-o-clock.scr.manifest"
