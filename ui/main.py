from tkinter import LEFT, X, Y, BOTH, Canvas, PhotoImage
from tkinter.ttk import Frame, Style, Button

from ui.theme import AppStyle


class Main(Frame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pack()

        style = AppStyle()

        # Top frame styles.
        style.configure("TOP.TFrame", width=600)

        # Bottom frame styles.
        style.configure("BOT.TFrame")

        top_frame = Frame(self, padding="10", style="TOP.TFrame")
        top_frame.pack(fill=X)

        self._biometry_image = PhotoImage(file="resources/biometrical.gif")
        biometry_button = Button(top_frame, image=self._biometry_image, compound=LEFT, text="Recognize")
        biometry_button.pack(side=LEFT, padx=10)

        self._open_image = PhotoImage(file="resources/folder_open.gif")
        open_button = Button(top_frame, image=self._open_image, compound=LEFT, text="Open")
        open_button.pack(side=LEFT, padx=10)

        self._config_image = PhotoImage(file="resources/config.gif")
        config_button = Button(top_frame, image=self._config_image, compound=LEFT, text="Config")
        config_button.pack(side=LEFT, padx=10)

        self._update_image = PhotoImage(file="resources/download.gif")
        update_button = Button(top_frame, image=self._update_image, compound=LEFT, text="Update")
        update_button.pack(side=LEFT, padx=10)

        # bottom_frame = Frame(self, style="BOT.TFrame")
        # bottom_frame.pack(anchor='center')
        #
        # canvas = Canvas(bottom_frame, width=100, height=100)
        # canvas.pack()
