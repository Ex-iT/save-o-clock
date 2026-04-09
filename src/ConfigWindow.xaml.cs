using System;
using System.IO;
using System.Windows;
using System.Runtime.InteropServices;
using Microsoft.Win32;
using System.Windows.Interop;

namespace SaveOClock
{
    public partial class ConfigWindow : Window
    {
        [DllImport("dwmapi.dll")]
        private static extern int DwmSetWindowAttribute(IntPtr hwnd, int attr, ref int attrValue, int attrSize);

        private const int DWMWA_SYSTEMBACKDROP_TYPE = 38;
        private const int DWMWA_WINDOW_CORNER_PREFERENCE = 33;

        public ConfigWindow()
        {
            InitializeComponent();
            LoadSettings();
            
            this.SourceInitialized += (s, e) => 
            {
                ApplyModernEffects();
            };
        }

        private void ApplyModernEffects()
        {
            IntPtr hWnd = new WindowInteropHelper(this).Handle;

            // Mica Alt (type 4)
            int backdropType = 4; 
            DwmSetWindowAttribute(hWnd, DWMWA_SYSTEMBACKDROP_TYPE, ref backdropType, sizeof(int));
        }

        private void LoadSettings()
        {
            PathTextBox.Text = Program.GetHtmlPath();
        }

        private void BrowseButton_Click(object sender, RoutedEventArgs e)
        {
            var openFileDialog = new Microsoft.Win32.OpenFileDialog();
            openFileDialog.Filter = "HTML files (*.html;*.htm)|*.html;*.htm|All files (*.*)|*.*";
            if (openFileDialog.ShowDialog() == true)
            {
                PathTextBox.Text = openFileDialog.FileName;
            }
        }

        private void SaveButton_Click(object sender, RoutedEventArgs e)
        {
            string path = PathTextBox.Text.Trim();
            
            try
            {
                using RegistryKey key = Registry.CurrentUser.CreateSubKey(@"SOFTWARE\SaveOClock");
                key.SetValue("HtmlPath", path);
                this.Close();
            }
            catch (Exception ex)
            {
                System.Windows.MessageBox.Show("Error saving settings: " + ex.Message);
            }
        }

        private void CancelButton_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }

        private void HelpButton_Click(object sender, RoutedEventArgs e)
        {
            var psi = new System.Diagnostics.ProcessStartInfo
            {
                FileName = "https://github.com/Ex-iT/save-o-clock",
                UseShellExecute = true
            };
            System.Diagnostics.Process.Start(psi);
        }
    }
}
