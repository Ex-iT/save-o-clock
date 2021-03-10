from tkinter import *
from tkinter.font import Font
from datetime import datetime
from screeninfo import get_monitors

time_format = '%H:%M:%S'

class Save_O_Clock:
    def __init__(self):
        self.root = Tk()
        self.root.title('Save-O-Clock')
        self.root.configure(background='black', cursor='none')
        self.root.geometry('0x0')
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
        self.root.configure(background='black')
        self.root.geometry(f'{self.monitor.width}x{self.monitor.height}+{self.monitor.x}+{self.monitor.y}')
        self.root.update_idletasks()
        self.root.attributes('-topmost', True)
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
            fg='white',
            bg='black',
            width=self.monitor.width,
            height=self.monitor.height
        )
        self.label.configure(font=Font(family='JetBrains Mono', size=200))
        self.label.pack()

        self.updateLabel(self)

    def updateLabel(self, event=None):
        self.label.configure(text=datetime.now().strftime(time_format))
        self.root.after(250, self.updateLabel)


if __name__ == '__main__':
    w = Save_O_Clock()
    w.root.mainloop()
