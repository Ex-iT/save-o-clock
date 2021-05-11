import argparse
import webbrowser
import sys
from collections import namedtuple
from tkinter import *
from tkinter.font import Font
from datetime import datetime
from screeninfo import get_monitors

time_format = '%H:%M'
font_family = 'JetBrains Mono'
font_size = 200
foreground_color = 'white'
background_color = 'black'
app_name = 'Save-O-Clock'
app_version = '0.0.1'
app_url = 'https://github.com/Ex-iT/save-o-clock'

class Save_O_Clock:
    def __init__(self, preview = False):
        self.root = Tk()
        self.root.title(app_name)
        self.root.configure(background='black', cursor='none')
        self.root.geometry('0x0+-100+-100') # Make sure the initial window doesn't show
        self.root.bind_all('<Key>', self.close)
        self.root.bind_all('<Motion>', self.close)
        self.root.update_idletasks()

        if preview:
            Monitor = namedtuple('Monitor', ['width', 'height', 'x', 'y'])
            Create_Screen(self.root, Monitor(100, 100, 0, 0))
        else:
            for monitor in get_monitors():
                Create_Screen(self.root, monitor)

    def close(self, event=None):
        self.root.destroy()


class Config_Dialog:
    def __init__(self):
        width = 300
        height = 100
        self.root = Tk()
        self.root.title(f'{app_name} - Config')
        self.root.geometry(f'{width}x{height}')
        self.root.resizable(False, False)

        self.label = Label(
            self.root,
            text = f'{app_name} - v{app_version}',
        )
        self.label.pack()
        self.label.place(
            y = 20,
            width = width
        )

        self.link = Label(
            self.root,
            text = app_url,
            fg = 'blue',
            cursor = 'hand2'
        )
        self.link.bind('<Button-1>', lambda e: webbrowser.open_new(app_url))
        self.link.pack()
        self.link.place(
            y = 40,
            width = width
        )


class Create_Screen:
    def __init__(self, root, monitor):
        self.monitor = monitor
        self.root = Toplevel(root)
        self.root.configure(background=background_color)
        self.root.geometry(f'{self.monitor.width}x{self.monitor.height}+{self.monitor.x}+{self.monitor.y}')
        self.root.update_idletasks()
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(1)

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
        self.label.configure(font=Font(family=font_family, size=font_size))
        self.label.pack()

        self.updateLabel(self)

    def updateLabel(self, event=None):
        self.label.configure(text=datetime.now().strftime(time_format))
        self.root.after(250, self.updateLabel)


if __name__ == '__main__':
    # Screen Saver command-line arguments.
    # https://docs.microsoft.com/en-us/troubleshoot/windows/win32/screen-saver-command-line
    parser = argparse.ArgumentParser(description='Running the application with no arguments shows the Settings dialog.', prefix_chars='/')
    g = parser.add_mutually_exclusive_group()
    g.add_argument('/c', help='Show the Settings dialog box, modal to the foreground window.', action='store_true')
    g.add_argument('/p', help='Preview Screen Saver as child of window <HWND>.', metavar='<HWND>', nargs=1, type=int)
    g.add_argument('/s', help='Run the Screen Saver.', action='store_true')
    args = parser.parse_args()

    log = open('log.txt', 'a+')
    time_stamp = datetime.now().strftime('%D %H:%M:%S')
    log.write(f'{time_stamp} :: {str(sys.argv)}\n')
    log.close()

    if args.c or (not args.c and not args.p and not args.s):
        w = Config_Dialog()
        w.root.mainloop()

    if args.p and args.p[0] > 1:
        w = Save_O_Clock(preview=True)
        w.root.mainloop()

    if args.s:
        w = Save_O_Clock()
        w.root.mainloop()
