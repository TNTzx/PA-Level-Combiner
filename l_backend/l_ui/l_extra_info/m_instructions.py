"""Contains the instructions UI."""


import tkinter as tk
import tkinter.ttk as ttk

import l_tkinter_utils


class Instructions(tk.Toplevel):
    """Contains the instructions."""
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        l_tkinter_utils.set_weights(self, y = (1, 1, 1))
        l_tkinter_utils.window_set_size(self, 720, 720)
        l_tkinter_utils.window_center_to_screen(self)

        self.w_title = self.Title(self)
        self.w_notebook = self.Notebook(self)
        self.w_close = self.Close(self)

    class Title(l_tkinter_utils.Title):
        """The title."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, title = "Instructions", title_size_mult = 0.5)
            l_tkinter_utils.place_on_grid(self)

    class Notebook(ttk.Notebook):
        """Notebook!"""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent)
            l_tkinter_utils.place_on_grid(self, coords = (0, 1))
            l_tkinter_utils.notebook_set_style(self)

    class Close(tk.Button):
        """The close button."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, text = "Close")
            l_tkinter_utils.place_on_grid(self, coords = (0, 2))
            l_tkinter_utils.set_font(self)
