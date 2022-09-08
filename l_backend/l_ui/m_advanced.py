"""Contains the advanced combine controls."""


import tkinter as tk
import l_tkinter_utils


class AdvancedView(tk.Frame):
    """The advanced view."""
    def __init__(self, parent: tk.Widget):
        super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
        l_tkinter_utils.place_on_grid(self)
        l_tkinter_utils.set_weights(self, y = (1 for _ in range(3)))

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

    class BaseLevel(l_tkinter_utils.EntryBrowseForm):
        """Base level entry."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, label_text = "Base level", label_size_mult = 1.2, initial = "<No Base Level>")
            l_tkinter_utils.place_on_grid(self, coords = (0, 1))


    class CurrentSourceLevel(tk.Frame):
        """Shows the current source level."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
            l_tkinter_utils.place_on_grid(self, coords = (0, 2))
            l_tkinter_utils.set_weights(self)

            self.w_label = self.Label(self)

        class Label(tk.Label):
            """Label."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent)
                l_tkinter_utils.place_on_grid(self)
