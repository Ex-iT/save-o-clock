from tkinter import *
from tkinter.font import Font
from datetime import datetime


class Save_O_Clock:
    def __init__(self):
        self.root = Tk()
        self.root.title('Save-O-Clock')
        self.root.configure(background='black')
        # self.root.geometry('1024x768')
        self.root.attributes('-fullscreen', True)
        self.root.bind_all('<Key>', self.close)
        self.root.bind_all('<Motion>', self.close)

        self.root.update_idletasks()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.frame = Frame(self.root, cursor='none')
        self.frame.pack()

        self.clock = Label(
            self.frame,
            text='',
            fg='white',
            bg='black',
            width=self.screen_width,
            height=self.screen_height,
            cursor='none'
        )
        self.clock.configure(font=Font(family='JetBrains Mono', size=200))
        self.clock.pack()

        self.updateClock()

    def updateClock(self, event=None):
        self.clock.configure(text=datetime.now().strftime('%H:%M'))
        self.root.after(1000, self.updateClock)

    def close(self, event=None):
        self.root.destroy()


if __name__ == '__main__':
    w = Save_O_Clock()
    w.root.mainloop()
