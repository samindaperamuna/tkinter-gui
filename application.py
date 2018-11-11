from tkinter import Tk

from screen_utils import center_window
from ui.login import Login

if __name__ == "__main__":
    root = Tk()
    root.geometry("300x125")
    root.title("Login")
    root.resizable(False, False)
    center_window(root)
    Login(root)
    root.mainloop()
