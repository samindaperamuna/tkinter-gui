import logging
from tkinter import CENTER, messagebox, StringVar
from tkinter import LEFT, BOTH, PhotoImage, SUNKEN, Toplevel, Canvas
from tkinter.ttk import Frame, Button, OptionMenu
from urllib.request import URLopener

from PIL.Image import fromarray
from PIL.ImageTk import PhotoImage

from data.json_util import read_settings
from file_utils import open_file
from screen_utils import center_window
from ui.config import Config
from ui.theme import AppStyle
from video_utils import VideoCapture


class Main(Frame):
    REMOTE_UPDATE_URL = "http://www.aiquimist.com/update/parameters.json"

    data = None
    shouldUpdate = False
    snapshot_dir = "snapshots"
    canvas = None
    capture = None
    photo = None
    delay = 15

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.bind("<configure>", self.on_window_resize())
        self.master.protocol("WM_DELETE_WINDOW", self.on_window_close)

        style = AppStyle()

        # Read application settings.
        self.data = read_settings()

        # Top frame styles.
        style.configure("TOP.TFrame")

        # Bottom frame styles.
        style.configure("BOT.TFrame")

        # Button styles.
        style.configure("TOP.TMenubutton", padding=13)

        top_frame = Frame(self, padding=10, style="TOP.TFrame")
        top_frame.grid(row=0, column=0, sticky="ew")

        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(6, weight=1)

        cams_list = self.get_cams_list()
        self.selected_camera_var = StringVar()
        self.selected_camera_var.trace('w', self.on_camera_option_select)

        self.cameras_option = OptionMenu(top_frame, self.selected_camera_var, None, *cams_list,
                                         command=self.on_camera_option_select, style="TOP.TMenubutton")
        self.cameras_option.grid(row=0, column=1, padx=[0, 10])

        self._biometry_image = PhotoImage(file="resources/biometrical.gif")
        biometry_button = Button(top_frame, image=self._biometry_image, compound=LEFT, text="Recognize",
                                 command=self.on_recognize_button_click)
        biometry_button.grid(row=0, column=2, padx=[0, 10])

        self._open_image = PhotoImage(file="resources/folder_open.gif")
        open_button = Button(top_frame, image=self._open_image, compound=LEFT, text="Open",
                             command=self.on_open_button_click)
        open_button.grid(row=0, column=3, padx=[0, 10])

        self._config_image = PhotoImage(file="resources/config.gif")
        config_button = Button(top_frame, image=self._config_image, compound=LEFT, text="Config",
                               command=self.on_config_button_click)
        config_button.grid(row=0, column=4, padx=[0, 10])

        self._update_image = PhotoImage(file="resources/download.gif")
        update_button = Button(top_frame, image=self._update_image, compound=LEFT, text="Update",
                               command=self.on_update_button_click)
        update_button.grid(row=0, column=5, padx=[0, 10])

        bottom_frame = Frame(self, padding=10, style="BOT.TFrame", relief=SUNKEN)
        bottom_frame.grid(row=1, column=0, padx=10, pady=[0, 10], sticky="nsew")

        self.canvas = Canvas(bottom_frame, bg="black")
        self.canvas.pack(fill=BOTH, expand=True)

        # Set the default camera.
        self.selected_camera_var.set(cams_list[0])

    def get_cams_list(self):
        cams = []
        # Load cameras section
        for cam in self.data["cameras"]:
            cams.append(cam)

        # Return the sorted list
        return sorted(cams)

    def on_window_close(self):
        self.shouldUpdate = False
        self.master.quit()

    def on_window_resize(self):
        if self.canvas is not None:
            self.canvas.configure(relx=0.5, rely=0.5, anchor=CENTER)

    def on_camera_option_select(self, *args):
        # Delete the existing capture object.
        if self.capture is not None:
            del self.capture

        source = self.data["cameras"][self.selected_camera_var.get()]
        self.init_video(source)

    def init_video(self, source):
        # Convert source to integer if numeric.
        if source.isnumeric():
            source = int(source)

        try:
            self.capture = VideoCapture(video_source=source, snapshot_dir=self.snapshot_dir)
        except ValueError as e:
            msg = "Couldn't open the stream: {0}".format(str(e))
            logging.critical(msg)
            messagebox.showerror("Error Opening Stream", msg)
            self.canvas.delete("all")
            return

        self.shouldUpdate = True

        while self.shouldUpdate:
            self.master.after(self.delay, self.update_canvas())

    def update_canvas(self):
        if self.capture is not None:
            # Force update values.
            self.canvas.update()
            can_width = self.canvas.winfo_width()
            can_height = self.canvas.winfo_height()

            # Get a frame from the video source.
            try:
                ret, frame = self.capture.get_frame(can_width, can_height)
                if ret:
                    self.photo = PhotoImage(image=fromarray(frame))
                    self.canvas.create_image(can_width / 2, can_height / 2, image=self.photo)
            except Exception as e:
                self.shouldUpdate = False

    def on_recognize_button_click(self):
        ret = self.capture.take_snapshot()
        if ret:
            messagebox.showinfo("Image Capture", "Snapshot saved!")
        else:
            messagebox.showerror("Image Capture", "Failed to save snapshot.")

    def on_open_button_click(self):
        open_file(self.snapshot_dir)

    def on_config_button_click(self):
        child = Toplevel(self)
        child.title("Config")
        child.geometry("400x235")
        center_window(child)
        child.transient(self)
        child.resizable(False, False)
        child.grab_set()
        Config(child)
        self.wait_window(child)

        # Read the new settings.
        self.data = read_settings()

    def on_update_button_click(self):
        try:
            opener = URLopener()
            opener.retrieve(self.REMOTE_UPDATE_URL, "resources/parameters.json")

            # Read the new settings.
            self.data = read_settings()
            messagebox.showinfo("Settings Update", "Settings successfully updated from the server.")
        except Exception as e:
            logging.critical("Couldn't open the remote settings file: {0}".format(str(e)))
            messagebox.showerror("Couldn't Update Settings", "Couldn't open the remote settings file.")
