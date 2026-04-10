# Save-O-Clock

**Save-O-Clock** is a multi-monitor Windows screensaver that renders custom HTML content on each screen individually. It uses the Chromium-based **WebView2** engine for high-performance, modern web standards support.

[Save-O-Clock Preview](https://soc.ex-it.nl/)

## 🌟 Features

- **Multi-Monitor Support**: Automatically detects all connected monitors and renders the screensaver on each one.
- **WPF Configuration**: A premium Windows 11-style settings interface with Mica effects.
- **Chromium Rendering**: Powered by WebView2 (Edge engine) for modern HTML/CSS/JS support.
- **High Performance**: Optimized for modern hardware with minimal footprint.
- **C# 12**: Built using the latest .NET technologies.

## 🚀 Getting Started

### Prerequisites

- **Windows 10 or 11**.
- **.NET 10 SDK** (to build) or **.NET 10 Desktop Runtime** (to run).
- **WebView2 Runtime** (included with Windows 10/11).

### How to Build

1. Install the [.NET 10 SDK](https://dotnet.microsoft.com/en-us/download/dotnet/10.0).
2. Clone or download this repository.
3. Run `build.bat`.
4. This will generate `Save-O-Clock.scr` in the project root.

### Installation

1. Right-click the generated `Save-O-Clock.scr` file.
2. Select **Install** to set it as your active screensaver.
3. Alternatively, copy `Save-O-Clock.scr` to `C:\Windows\System32` to make it available in the Windows Screen Saver Settings dropdown.

## ⚙️ Configuration

1. Open the Windows **Screen Saver Settings**.
2. Select **Save-O-Clock** from the list.
3. Click **Settings...** to open the configuration window.
4. Browse and select the HTML file you wish to display.
5. Click **Save** to apply the changes.

## 🛠️ Project Structure

- `Save-O-Clock.csproj`: Modern SDK project file.
- `src/Screensaver.cs`: Core logic for multi-monitor rendering and WebView2 hosting.
- `src/ConfigWindow.xaml`: WPF-based Windows 11 style settings UI.
- `src/ConfigWindow.xaml.cs`: Code behind for the configuration window.
- `src/soc.html`: A default sample HTML clock.
- `build.bat`: Build automation script using `dotnet publish`.
