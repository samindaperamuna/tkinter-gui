from tkinter import LEFT, BOTH
from tkinter.ttk import Frame, Notebook

from ui.theme import AppStyle


class Config(Frame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        style = AppStyle()
        style.configure("MAIN.TNotebook")

        # Tab container.
        notebook = Notebook(self, style="MAIN.TNotebook")

        # Tabs
        main = Frame(notebook)
        frames = Frame(notebook)
        cameras = Frame(notebook)

        # Add the tabs.
        notebook.add(main, text="Main")
        notebook.add(frames, text="Frames")
        notebook.add(cameras, text="Cameras")

        notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
