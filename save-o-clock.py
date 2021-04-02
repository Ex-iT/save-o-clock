from tkinter import *
from tkinter.font import Font
from datetime import datetime
from sys import platform
from screeninfo import get_monitors

time_format = '%H:%M'
font_family = 'JetBrains Mono'
font_size = 200
foreground_color = 'white'
background_color = 'black'
operating_system = 'windows'

class Save_O_Clock:
    def __init__(self):
        self.root = Tk()
        self.root.title('Save-O-Clock')
        self.root.configure(background='black', cursor='none')
        self.root.geometry('0x0+-100+-100') # Make sure the initial window doesn't show
        self.root.bind_all('<Key>', self.close)
        self.root.bind_all('<Motion>', self.close)
        self.root.update_idletasks()

        for monitor in get_monitors():
            Create_Window(self.root, monitor)

    def close(self, event=None):
        self.root.destroy()


class Create_Window:
    def __init__(self, root, monitor):
        self.monitor = monitor
        self.root = Toplevel(root)
        self.root.configure(background=background_color)
        self.root.geometry(f'{self.monitor.width}x{self.monitor.height}+{self.monitor.x}+{self.monitor.y}')
        self.root.update_idletasks()
        self.root.attributes('-topmost', True)

        if operating_system == 'windows':
            self.root.overrideredirect(1)
        elif operating_system == 'linux':
            self.root.attributes('-zoomed', True)
        elif operating_system == 'macos':
            self.root.attributes('-fullscreen', True)
        

        self.createFrame(self)

    def createFrame(self, event=None):
        self.frame = Frame(
            self.root,
            cursor='none',
            width=self.monitor.width,
            height=self.monitor.height
        )
        self.frame.pack()

        self.createClock(self)

    def createClock(self, event=None):
        self.label = Label(
            self.frame,
            cursor='none',
            text='',
            fg=foreground_color,
            bg=background_color,
            width=self.monitor.width,
            height=self.monitor.height
        )
        self.label.configure(font=Font(family=font_family, size=font_size))
        self.label.pack()

        self.updateLabel(self)

    def updateLabel(self, event=None):
        self.label.configure(text=datetime.now().strftime(time_format))
        self.root.after(250, self.updateLabel)


if __name__ == '__main__':
    if platform == 'linux' or platform == 'linux2':
        operating_system = 'linux'
    elif platform == 'darwin':
        operating_system = 'osx'
    elif platform == 'win32' or platform == 'cygwin':
        operating_system = 'windows'
        
    w = Save_O_Clock()
    w.root.mainloop()
