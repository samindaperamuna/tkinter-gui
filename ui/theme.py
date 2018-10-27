from tkinter.ttk import Style


class AppStyle(Style):

    def __init__(self):
        super().__init__()
        self.theme_use('clam')
