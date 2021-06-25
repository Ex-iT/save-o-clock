import sys
import pathlib
import argparse
import json
import webbrowser
import win32gui
from os import path
from collections import namedtuple
from tkinter import *
from tkinter.font import Font
from datetime import datetime
from screeninfo import get_monitors

# Default settings
time_format = '%H:%M'
font_family = 'JetBrains Mono'
font_size = 200
foreground_color = 'white'
background_color = 'black'

app_name = 'Save-O-Clock'
app_version = '0.0.1'
app_url = 'https://github.com/Ex-iT/save-o-clock'

# Only use this logging while debugging.
# Writing a file will make the screensaver crash (preview still works).
logging_enabled = False
log_file = 'log.txt'

class Save_O_Clock:
    def __init__(self, config = False, preview = False, config_handle = 0, preview_handle = 0):
        self.root = Tk()
        self.root.title(app_name)
        self.root.iconbitmap(path.join(cwd, 'save-o-clock.ico'))
        self.root.geometry('0x0+-100+-100') # Make sure the initial window doesn't show
        self.root.overrideredirect(True) # No window chrome and hide from task bar
        self.root.update_idletasks()

        if config:
            Config_Dialog(self.root, self.close)
        elif preview:
            self.handlePreview(preview_handle)
        else:
            self.handleScreenSaver()

    def handlePreview(self, preview_handle):
        hwnd = self.root.winfo_id()
        left, top, right, bottom = win32gui.GetWindowRect(preview_handle)
        Monitor = namedtuple('Monitor', ['width', 'height', 'x', 'y'])
        Create_Screen(self.root, Monitor((right-left), (bottom-top), left, top), hwnd, preview_handle)

    def handleScreenSaver(self):
        self.root.configure(background='black', cursor='none')
        self.root.bind_all('<Key>', self.close)
        self.root.bind_all('<Motion>', self.close)

        for monitor in get_monitors():
            Create_Screen(self.root, monitor)

    def close(self, event=None):
        self.root.destroy()


class Config_Dialog:
    def __init__(self, root, close, config_handle):
        width = 300
        height = 100
        self.root = Toplevel(root)
        self.root.title(f'{app_name} - Settings')
        self.root.iconbitmap(path.join(cwd, 'save-o-clock.ico'))
        self.root.geometry(f'{width}x{height}')
        self.root.resizable(False, False)
        self.root.update_idletasks()
        self.root.protocol('WM_DELETE_WINDOW', lambda: close())

        self.label = Label(self.root, text = f'{app_name} - v{app_version}')
        self.label.pack()
        self.label.place(y = 20, width = width)

        self.link = Label(self.root, text = app_url, fg = 'blue', cursor = 'hand2')
        self.link.bind('<Button-1>', lambda e: webbrowser.open_new(app_url))
        self.link.pack()
        self.link.place(y = 40, width = width)


class Create_Screen:
    def __init__(self, root, monitor, root_handle = 0, preview_handle = 0):
        self.monitor = monitor
        self.font_size = font_size
        self.root = Toplevel(root)
        self.root.configure(background=background_color)
        self.root.update_idletasks()
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)

        pos = f'{self.monitor.width}x{self.monitor.height}+{self.monitor.x}+{self.monitor.y}'

        if preview_handle > 0:
            self.font_size = 12
            win32gui.SetParent(root_handle, preview_handle)

        self.root.geometry(pos)

        self.createFrame(self)

    def createFrame(self, event=None):
        self.frame = Frame(
            self.root,
            cursor = 'none',
            width = self.monitor.width,
            height = self.monitor.height
        )
        self.frame.pack()

        self.createClock(self)

    def createClock(self, event=None):
        self.label = Label(
            self.frame,
            cursor = 'none',
            text = '',
            fg = foreground_color,
            bg = background_color,
            width = self.monitor.width,
            height = self.monitor.height
        )
        self.label.configure(font=Font(family=font_family, size=self.font_size))
        self.label.pack()

        self.updateLabel(self)

    def updateLabel(self, event=None):
        self.label.configure(text=datetime.now().strftime(time_format))
        self.root.after(250, self.updateLabel)


def logger(message):
    if (logging_enabled):
        log = open(log_file, 'a+')
        time_stamp = datetime.now().strftime('%D %H:%M:%S')
        log.write(f'{time_stamp} :: {message}\n')
        log.close()

def setJsonSettings(settings_file):
    if path.isfile(settings_file):
        logger('Settings file found')
        try:
            with open(settings_file) as json_settings:
                settings = json.load(json_settings)
                if 'time_format' in settings: global time_format; time_format = settings['time_format']
                if 'font_family' in settings: global font_family; font_family = settings['font_family']
                if 'font_size' in settings: global font_size; font_size = settings['font_size']
                if 'foreground_color' in settings: global foreground_color; foreground_color = settings['foreground_color']
                if 'background_color' in settings: global background_color; background_color = settings['background_color']
        except:
            logger('Failed reading settings file')

def getArgs():
    # Screen Saver command-line arguments.
    # https://docs.microsoft.com/en-us/troubleshoot/windows/win32/screen-saver-command-line
    parser = argparse.ArgumentParser(description='Running the application with no arguments shows the Settings dialog.', prefix_chars='/')
    g = parser.add_mutually_exclusive_group()
    g.add_argument('/c', '/C', help='Show the Settings dialog box, modal to the foreground window.', nargs='*')
    g.add_argument('/p', '/P', help='Preview Screen Saver as child of window <HWND>.', metavar='<HWND>', nargs=1, type=int)
    g.add_argument('/s', '/S', help='Run the Screen Saver.', action='store_true')

    logger(str(sys.argv))

    return parser.parse_args()

def main():
    setJsonSettings(path.join(cwd, 'settings.json'))
    args = getArgs()

    if args.c or (not args.c and not args.p and not args.s):
        config_handle = 0
        if args.c:
            config_handle = int(args.c[0][1:])

        w = Save_O_Clock(config = True, config_handle = config_handle)

    if args.p and args.p[0] > 1:
        w = Save_O_Clock(preview = True, preview_handle = args.p[0])

    if args.s:
        w = Save_O_Clock()

    w.root.mainloop()


if __name__ == '__main__':
    cwd = pathlib.Path(__file__).parent.resolve()
    main()
