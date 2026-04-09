@echo off
set PROJECT_NAME=Save-O-Clock
set OUTPUT_NAME=Save-O-Clock.scr

echo Building %PROJECT_NAME% (.NET 8)...

dotnet publish -c Release -r win-x64 --no-self-contained -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true -o ./publish

if %ERRORLEVEL% equ 0 (
    echo.
    echo Success: Build complete.
    copy /Y ".\publish\%PROJECT_NAME%.exe" ".\%OUTPUT_NAME%"
    echo Copied binary to %OUTPUT_NAME%
) else (
    echo.
    echo Error: Build failed. Check if .NET 8 SDK is installed.
)
pause
