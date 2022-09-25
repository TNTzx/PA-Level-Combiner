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

            self.frame_infos = [
                l_tkinter_utils.NotebookFrameInfo("Workflow", Workflow(self))
            ]

    class Close(tk.Button):
        """The close button."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, text = "Close")
            l_tkinter_utils.place_on_grid(self, coords = (0, 2))
            l_tkinter_utils.set_font(self)


class Workflow(l_tkinter_utils.ScrollableFrame):
    """Workflow tab"""
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        l_tkinter_utils.place_on_grid(self)

        self.w_label_format = self.LabelFormat(self.w_canvas.w_frame)

    class LabelFormat(l_tkinter_utils.LabelFormat):
        """The label."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent)
            l_tkinter_utils.place_on_grid(self)
            l_tkinter_utils.set_font(self)

            texts = [
                l_tkinter_utils.LabelFormatText(
                    "1. Select the PA version of the levels that you'll use to combine."
                ),
                l_tkinter_utils.LabelFormatText(
                    "2. Add your level folders using the \"Add Level Folder\" button. Edit and delete if necessary."
                ),
                l_tkinter_utils.LabelFormatText(
                    "3. Create a folder to store the combined level, then use the \"Browse\" button to set the output folder to that folder."
                ),
                l_tkinter_utils.LabelFormatText(
                    "4. Set other combine options in the \"Advanced\" tab."
                ),
                l_tkinter_utils.LabelFormatText(
                    "5. Press the combine button!"
                )
            ]

            self.add_texts(texts)
