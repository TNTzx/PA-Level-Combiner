"""Contains the advanced combine controls."""


import tkinter as tk
import l_tkinter_utils


class AdvancedView(tk.Frame):
    """The advanced view."""
    def __init__(self, parent: tk.Widget):
        super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
        l_tkinter_utils.place_on_grid(self)
        l_tkinter_utils.set_weights(self, y = (1 for _ in range(4)))

        self.w_title = self.Title(self)
        self.w_base_level = self.BaseLevel(self)
        self.w_current_source_level = self.CurrentSourceLevel(self)

    class Title(l_tkinter_utils.Title):
        """The title."""
        def __init__(self, parent: tk.Widget):
            super().__init__(
                parent,
                title = "Advanced Controls",
                description = "These are advanced combining controls. Make sure you know how to use them!",
                title_size_mult = 0.5
            )
            l_tkinter_utils.place_on_grid(self)

    class Options(tk.Button):
        """Contains all combine options."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, text = "Combining Options...")
            l_tkinter_utils.place_on_grid(self, coords = (0, 1))
            l_tkinter_utils.set_font(self, font = l_tkinter_utils.make_font(size_mult = 1.2))

    class BaseLevel(l_tkinter_utils.EntryBrowseForm):
        """Base level entry."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, label_text = "Base level", label_size_mult = 1.2, initial = "<No Base Level>")
            l_tkinter_utils.place_on_grid(self, coords = (0, 2))

    class CurrentSourceLevel(tk.Frame):
        """Shows the current source level."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
            l_tkinter_utils.place_on_grid(self, coords = (0, 3))
            l_tkinter_utils.set_weights(self)

            self.w_label = self.Label(self)

        class Label(tk.Label):
            """Label."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent)
                l_tkinter_utils.place_on_grid(self)
                l_tkinter_utils.set_font(self)
                l_tkinter_utils.add_wrapping(self)


        def update_text(self, available: bool, source: str = "", folder_path: str = ""):
            """Updates the text."""
            if available:
                final_str = (
                    f"Current Source Level: {source}\n"
                    f"{folder_path}"
                )
            else:
                final_str = "Current Source Level: Not found!"
            l_tkinter_utils.update_text(self.w_label, final_str)
