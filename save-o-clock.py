from tkinter import *
from tkinter.font import Font
from datetime import datetime
from screeninfo import get_monitors

class Save_O_Clock:
    def __init__(self, monitor):
        self.root = Tk()
        self.root.title('Save-O-Clock')
        self.root.configure(background='black')
        # self.root.geometry(f'{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}')
        self.root.attributes('-fullscreen', True)
        self.root.bind_all('<Key>', self.close)
        self.root.bind_all('<Motion>', self.close)

        self.root.update_idletasks()

        self.createFrame(self, monitor)


    def createFrame(self, event, monitor):
        self.frame = Frame(
            self.root,
            cursor='none',
            width=monitor.width,
            height=monitor.height
        )
        self.frame.pack()

        self.createClock(self, monitor)


    def createClock(self, event, monitor):
        self.label = Label(
            self.frame,
            text='',
            fg='white',
            bg='black',
            width=monitor.width,
            height=monitor.height,
            cursor='none'
        )
        self.label.configure(font=Font(family='JetBrains Mono', size=200))
        self.label.pack()

        self.updateLabel(self)


    def updateLabel(self, event=None):
        self.label.configure(text=datetime.now().strftime('%H:%M'))
        self.root.after(1000, self.updateLabel)


    def close(self, event=None):
        self.root.destroy()


if __name__ == '__main__':
    for monitor in get_monitors():
        w = Save_O_Clock(monitor)
        w.root.mainloop()
