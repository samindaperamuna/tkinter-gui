from tkinter import LEFT, BOTH, E, W, N, messagebox, END, Tk, StringVar, _setit
from tkinter.ttk import Frame, Notebook, Label, Entry, Button, OptionMenu

from data.json_util import read_settings, write_settings, reset_default
from screen_utils import center_window
from ui.theme import AppStyle


class Config(Frame):
    data = None

    def __init__(self, parent=None):
        super().__init__(parent)
        parent.bind('<Return>', self.on_accept_button_click)

        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        style = AppStyle()
        style.configure("SELF.TLabel", width=15)
        style.configure("SELF.TEntry", width=200, padding=5)
        style.configure("SELF.TMenubutton", width=200, padding=5)

        # Tab container.
        notebook = Notebook(self)

        # Main tab content
        main = Frame(notebook)
        main.columnconfigure(1, weight=1)

        screen_label = Label(main, text="Screen", style="SELF.TLabel")
        screen_label.grid(row=0, column=0, padx=[10, 0], pady=[10, 0], sticky=W)
        self.screen_entry = Entry(main, style="SELF.TEntry")
        self.screen_entry.grid(row=0, column=1, padx=[0, 10], pady=[10, 0], sticky=W + E)

        width_label = Label(main, text="Width percent", style="SELF.TLabel")
        width_label.grid(row=1, column=0, padx=[10, 0], pady=[5, 0], sticky=W)
        self.width_entry = Entry(main, style="SELF.TEntry")
        self.width_entry.grid(row=1, column=1, padx=[0, 10], pady=[5, 0], sticky=W + E)

        height_label = Label(main, text="Height percent", style="SELF.TLabel")
        height_label.grid(row=2, column=0, padx=[10, 0], pady=[5, 0], sticky=W)
        self.height_entry = Entry(main, style="SELF.TEntry")
        self.height_entry.grid(row=2, column=1, padx=[0, 10], pady=[5, 0], sticky=W + E)

        camera_type_label = Label(main, text="Camera type", style="SELF.TLabel")
        camera_type_label.grid(row=3, column=0, padx=[10, 0], pady=[5, 10], sticky=W)
        self.camera_type_entry = Entry(main, style="SELF.TEntry")
        self.camera_type_entry.grid(row=3, column=1, padx=[0, 10], pady=[5, 10], sticky=W + E)

        # Frames tab content.
        frames = Frame(notebook)
        frames.columnconfigure(1, weight=1)

        frame_interval_label = Label(frames, text="Frame interval", style="SELF.TLabel")
        frame_interval_label.grid(row=0, column=0, padx=[10, 0], pady=[10, 0], sticky=W)
        self.frame_interval_entry = Entry(frames, style="SELF.TEntry")
        self.frame_interval_entry.grid(row=0, column=1, padx=[0, 10], pady=[10, 0], sticky=W + E)

        frame_rate_label = Label(frames, text="Frame rate", style="SELF.TLabel")
        frame_rate_label.grid(row=1, column=0, padx=[10, 0], pady=[10, 0], sticky=W)
        self.frame_rate_entry = Entry(frames, style="SELF.TEntry")
        self.frame_rate_entry.grid(row=1, column=1, padx=[0, 10], pady=[10, 0], sticky=W + E)

        frame_count_label = Label(frames, text="Frame count", style="SELF.TLabel")
        frame_count_label.grid(row=2, column=0, padx=[10, 0], pady=[10, 0], sticky=W)
        self.frame_count_entry = Entry(frames, style="SELF.TEntry")
        self.frame_count_entry.grid(row=2, column=1, padx=[0, 10], pady=[10, 0], sticky=W + E)

        # Cameras tab content.
        cameras = Frame(notebook)
        cameras.columnconfigure(1, weight=1)

        camera_label = Label(cameras, text="Cameras", style="SELF.TLabel")
        camera_label.grid(row=0, column=0, padx=[10, 0], pady=[10, 0], sticky=W)

        self.selected_camera_var = StringVar(self)
        self.selected_camera_var.trace('w', self.on_camera_option_select)

        self.cameras_options = OptionMenu(cameras, self.selected_camera_var, style="SELF.TMenubutton")
        self.cameras_options.grid(row=0, column=1, padx=[0, 10], pady=[10, 0], sticky=E)

        add_cam_button = Button(cameras, text="Add", width=5, command=self.on_add_cam_button_click)
        add_cam_button.grid(row=0, column=2, padx=[0, 10], pady=[10, 0], sticky=E)

        delete_cam_button = Button(cameras, text="Delete", width=5, command=self.on_delete_cam_button_click)
        delete_cam_button.grid(row=0, column=3, padx=[0, 10], pady=[10, 0], sticky=E)

        self.edit_cam_entry = Entry(cameras, style="SELF.TEntry")
        self.edit_cam_entry.grid(row=1, column=0, columnspan=3, padx=10, pady=[5, 0], sticky=W + E)

        edit_cam_button = Button(cameras, text="Edit", width=5, command=self.on_edit_cam_button_click)
        edit_cam_button.grid(row=1, column=2, columnspan=2, padx=[0, 10], pady=[5, 0], sticky=E)

        # Add the tabs.
        notebook.add(main, text="Main")
        notebook.add(frames, text="Frames")
        notebook.add(cameras, text="Cameras")

        notebook.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky=W + E)

        accept_button = Button(self, text="Accept")
        accept_button.grid(row=1, column=1, padx=[0, 10], sticky=N + E)
        accept_button.bind("<Button-1>", self.on_accept_button_click)

        default_button = Button(self, text="Default")
        default_button.grid(row=1, column=2, padx=[0, 10], sticky=N + E)
        default_button.bind("<Button-1>", self.on_default_button_click)

        cancel_button = Button(self, text="Cancel")
        cancel_button.grid(row=1, column=3, padx=[0, 10], sticky=N + E)
        cancel_button.bind("<Button-1>", self.on_cancel_button_click)

        # Load configuration.
        self.load_config()

    def on_camera_option_select(self, *args):
        if self.data is not None:
            self.edit_cam_entry.delete(0, END)
            self.edit_cam_entry.insert(0, self.data["cameras"][self.selected_camera_var.get()])

    def on_add_cam_button_click(self):
        # Get the no of cameras.
        index = len(self.data["cameras"])
        # Add the camera to the data dictionary.
        self.data["cameras"][str(index)] = self.edit_cam_entry.get()

        # Update camera select box.
        self.clear_cameras()
        self.add_cameras(index)

    def on_delete_cam_button_click(self):
        size = len(self.data["cameras"])
        if size > 1:
            index = size - 1
            self.data["cameras"].pop(str(index))

            # Update cameras
            self.clear_cameras()
            self.add_cameras(index - 1)
        else:
            messagebox.showinfo("Cannot Delete Camera", "There must be at least one camera on the list.")

    def on_edit_cam_button_click(self):
        index = self.selected_camera_var.get()
        self.data["cameras"][str(index)] = self.edit_cam_entry.get()

        # Update camera select box.
        self.clear_cameras()
        self.add_cameras(index)

    def on_accept_button_click(self, _):
        self.save_config()

    def on_default_button_click(self, _):
        res = messagebox.askyesno("Confirm Settings Reset", "Are you sure you want to reset settings to default?")

        if res is True:
            reset_default()
            self.reset_form()
            self.load_config()

    def on_cancel_button_click(self, _):
        self.master.destroy()

    def reset_form(self):
        """Clear the current form content"""
        self.screen_entry.delete(0, END)
        self.width_entry.delete(0, END)
        self.height_entry.delete(0, END)
        self.camera_type_entry.delete(0, END)
        self.frame_interval_entry.delete(0, END)
        self.frame_rate_entry.delete(0, END)
        self.frame_count_entry.delete(0, END)

        self.clear_cameras()

    def load_config(self):
        data = read_settings()

        # Load main section.
        self.screen_entry.insert(0, data["main"]["screen"])
        self.width_entry.insert(0, data["main"]["width_percent"])
        self.height_entry.insert(0, data["main"]["height_percent"])
        self.camera_type_entry.insert(0, data["main"]["type_camera"])

        # Load frames section
        self.frame_interval_entry.insert(0, data["frames"]["frame_interval"])
        self.frame_rate_entry.insert(0, data["frames"]["frame_rate"])
        self.frame_count_entry.insert(0, data["frames"]["frame_count"])
        # Set the class data field to the JSON dict.

        self.data = data

        self.add_cameras(0)

    def clear_cameras(self):
        self.cameras_options['menu'].delete(0, 'end')

    def add_cameras(self, selection: int):
        cams = []
        # Load cameras section
        for cam in self.data["cameras"]:
            cams.append(cam)

        # Sort list
        cams = sorted(cams)

        # Append list to options.
        for cam in cams:
            self.cameras_options['menu'].add_command(label=cam, command=_setit(self.selected_camera_var, cam))

        # Set selected item to the 0
        self.selected_camera_var.set(selection)

    def save_config(self):
        data = self.data

        # Set main section.
        data["main"]["screen"] = self.screen_entry.get()
        data["main"]["width_percent"] = self.width_entry.get()
        data["main"]["height_percent"] = self.height_entry.get()
        data["main"]["type_camera"] = self.camera_type_entry.get()

        # Set frames section.
        data["frames"]["frame_interval"] = self.frame_interval_entry.get()
        data["frames"]["frame_rate"] = self.frame_rate_entry.get()
        data["frames"]["frame_count"] = self.frame_count_entry.get()

        # Save JSON data into file.
        if not write_settings(data):
            messagebox.showerror(title="An Error Occurred!", message="Couldn't save the changes.")
        else:
            self.master.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Config Test Screen")
    root.geometry("400x235")
    center_window(root)

    config = Config(parent=root)
    root.mainloop()
