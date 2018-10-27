from tkinter import LEFT, BOTH, PhotoImage, SUNKEN
from tkinter.ttk import Frame, Button

from ui.theme import AppStyle


class Main(Frame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        style = AppStyle()

        # Top frame styles.
        style.configure("TOP.TFrame")

        # Bottom frame styles.
        style.configure("BOT.TFrame")

        top_frame = Frame(self, padding=10, style="TOP.TFrame")
        top_frame.grid(row=0, column=0, sticky="ew")

        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(5, weight=1)

        self._biometry_image = PhotoImage(file="resources/biometrical.gif")
        biometry_button = Button(top_frame, image=self._biometry_image, compound=LEFT, text="Recognize")
        biometry_button.grid(row=0, column=1, padx=[0, 10])

        self._open_image = PhotoImage(file="resources/folder_open.gif")
        open_button = Button(top_frame, image=self._open_image, compound=LEFT, text="Open")
        open_button.grid(row=0, column=2, padx=[0, 10])

        self._config_image = PhotoImage(file="resources/config.gif")
        config_button = Button(top_frame, image=self._config_image, compound=LEFT, text="Config")
        config_button.grid(row=0, column=3, padx=[0, 10])

        self._update_image = PhotoImage(file="resources/download.gif")
        update_button = Button(top_frame, image=self._update_image, compound=LEFT, text="Update")
        update_button.grid(row=0, column=4, padx=[0, 10])

        bottom_frame = Frame(self, padding=10, style="BOT.TFrame", relief=SUNKEN)
        bottom_frame.grid(row=1, column=0, padx=10, pady=[0, 10], sticky="nsew")
