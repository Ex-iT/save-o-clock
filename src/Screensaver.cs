using System;
using System.Drawing;
using System.Windows.Forms;
using Microsoft.Win32;
using System.IO;
using System.Reflection;
using Microsoft.Web.WebView2.WinForms;
using Microsoft.Web.WebView2.Core;

namespace SaveOClock
{
    static class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            ApplicationConfiguration.Initialize();

            if (args.Length > 0)
            {
                string firstArgument = args[0].ToLower().Trim();
                string? secondArgument = null;

                // Handle cases like "/c:123456" or "/p 123456"
                if (firstArgument.Length > 2)
                {
                    secondArgument = firstArgument[3..].Trim();
                    firstArgument = firstArgument[..2];
                }
                else if (args.Length > 1)
                {
                    secondArgument = args[1];
                }

                if (firstArgument == "/c")
                {
                    ShowSettings();
                }
                else if (firstArgument == "/p")
                {
                    // Preview mode not fully implemented for WebView2 yet (requires complex parenting)
                    // We'll show a simple placeholder or exit
                    Application.Exit();
                }
                else if (firstArgument == "/s")
                {
                    ShowScreensaver();
                }
                else
                {
                    ShowSettings();
                }
            }
            else
            {
                ShowSettings();
            }
        }

        static void ShowSettings()
        {
            var configWindow = new ConfigWindow();
            configWindow.ShowDialog();
            Application.Exit();
        }

        static void ShowScreensaver()
        {
            string htmlPath = GetHtmlPath();
            
            foreach (Screen screen in Screen.AllScreens)
            {
                ScreensaverForm screensaverForm = new ScreensaverForm(screen, htmlPath);
                screensaverForm.Show();
            }

            Application.Run();
        }

        public static string GetHtmlPath()
        {
            using RegistryKey? key = Registry.CurrentUser.OpenSubKey(@"SOFTWARE\SaveOClock");
            return key?.GetValue("HtmlPath") as string ?? "";
        }
    }

    public class ScreensaverForm : Form
    {
        private Point mouseLocation;
        private WebView2? webView;
        private readonly string htmlPath;

        public ScreensaverForm(Screen screen, string htmlPath)
        {
            this.htmlPath = htmlPath;
            InitializeComponent(screen);
        }

        private async void InitializeComponent(Screen screen)
        {
            this.webView = new WebView2();
            this.SuspendLayout();

            // webView
            this.webView.Dock = DockStyle.Fill;
            this.webView.DefaultBackgroundColor = Color.Black;

            // ScreensaverForm
            this.BackColor = Color.Black;
            this.Bounds = screen.Bounds;
            this.StartPosition = FormStartPosition.Manual;
            this.FormBorderStyle = FormBorderStyle.None;
            this.TopMost = true;
            this.ShowInTaskbar = false;
            this.Controls.Add(this.webView);

            this.Load += ScreensaverForm_Load;
            
            // Events for exiting
            this.webView.KeyDown += (s, e) => Application.Exit();
            this.MouseMove += (s, e) => HandleMouseEvent(Cursor.Position);
            this.KeyDown += (s, e) => Application.Exit();

            this.ResumeLayout(false);

            try 
            {
                string userDataFolder = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "SaveOClock");
                var env = await CoreWebView2Environment.CreateAsync(null, userDataFolder);
                await webView.EnsureCoreWebView2Async(env);
                
                webView.CoreWebView2.Settings.AreDefaultContextMenusEnabled = false;
                webView.CoreWebView2.Settings.AreDevToolsEnabled = false;

                // Inject script to detect any interaction and post message to exit
                string script = @"
                    window.addEventListener('mousemove', function(e) {
                        if (Math.abs(e.movementX) > 2 || Math.Abs(e.movementY) > 2) {
                            window.chrome.webview.postMessage('exit');
                        }
                    });
                    window.addEventListener('mousedown', () => window.chrome.webview.postMessage('exit'));
                    window.addEventListener('keydown', () => window.chrome.webview.postMessage('exit'));
                ";
                await webView.CoreWebView2.AddScriptToExecuteOnDocumentCreatedAsync(script);
                webView.CoreWebView2.WebMessageReceived += (s, args) => {
                    if (args.TryGetWebMessageAsString() == "exit") Application.Exit();
                };
                
                if (File.Exists(htmlPath))
                {
                    webView.Source = new Uri(htmlPath);
                }
                else if (!string.IsNullOrEmpty(htmlPath))
                {
                    // Path was specified but file is missing
                    string errorHtml = $"<html><body style='background:black;color:white;display:flex;flex-direction:column;justify-content:center;align-items:center;height:100vh;overflow:hidden;font-family:sans-serif'><h1>File Not Found</h1><p style='color:#999'>{htmlPath}</p></body></html>";
                    webView.NavigateToString(errorHtml);
                }
                else
                {
                    // No path set, use embedded fallback
                    string fallbackHtml = ReadEmbeddedResource("SaveOClock.src.soc.html");
                    webView.NavigateToString(fallbackHtml);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"WebView2 Error: {ex.Message}");
                Application.Exit();
            }
        }

        private void ScreensaverForm_Load(object? sender, EventArgs e)
        {
            Cursor.Hide();
        }

        private void HandleMouseEvent(Point currentPosition)
        {
            if (!mouseLocation.IsEmpty)
            {
                if (Math.Abs(mouseLocation.X - currentPosition.X) > 15 ||
                    Math.Abs(mouseLocation.Y - currentPosition.Y) > 15)
                {
                    Application.Exit();
                }
            }
            mouseLocation = currentPosition;
        }

        private string ReadEmbeddedResource(string resourceName)
        {
            var assembly = Assembly.GetExecutingAssembly();
            using Stream? stream = assembly.GetManifestResourceStream(resourceName);
            if (stream == null) return "<html><body style='background:black;color:white;'><h1>Embedded resource not found.</h1></body></html>";
            using StreamReader reader = new StreamReader(stream);
            return reader.ReadToEnd();
        }
    }
}
