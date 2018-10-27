from tkinter import Tk

from screen_utils import center_window
from ui.main import Main

if __name__ == "__main__":
    root = Tk()
    root.geometry("640x480")
    root.title("Tkinter GUI")
    center_window(root)
    ui = Main(root)
    root.mainloop()
