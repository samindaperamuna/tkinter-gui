def center_window(top_level):
    """Center a given tkinter widget on the screen."""
    top_level.update_idletasks()

    screen_width = top_level.winfo_screenwidth()
    screen_height = top_level.winfo_screenheight()

    size = tuple(int(pos) for pos in top_level.geometry().split('+')[0].split('x'))
    x = screen_width / 2 - size[0] / 2
    y = screen_height / 2 - size[1] / 2

    top_level.withdraw()
    top_level.geometry("+%d+%d" % (x, y))
    top_level.deiconify()
