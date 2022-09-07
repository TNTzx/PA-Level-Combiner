"""Contains the full UI."""


import tkinter as tk
import tkinter.ttk as ttk

import l_tkinter_utils
import l_pa_cls_simple


class MainWindow(tk.Toplevel):
    """The main window."""
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        l_tkinter_utils.set_weights(self, y = (1 for _ in range(6)))
        l_tkinter_utils.window_set_size(self, 1280, 720)
        l_tkinter_utils.window_center_to_screen(self)

        self.w_title = self.Title(self)

    class Title(l_tkinter_utils.Title):
        """The title."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, title = "PA Level Combiner", description = "A program used to combine levels.")
            l_tkinter_utils.place_on_grid(self)

    class ViewManager(ttk.Notebook):
        """The view manager."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent)
            l_tkinter_utils.place_on_grid(self, coords = (0, 1))

    class CombineControls(tk.Frame):
        """Contains the combining controls."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
            l_tkinter_utils.place_on_grid(self, coords = (0, 2))
            l_tkinter_utils.set_weights(self, x = (1, 1))

            self.w_options = self.Options(self)
            self.w_button = self.Button(self)

        class Options(tk.Button):
            """Contains all combine options."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Combining Options...")
                l_tkinter_utils.place_on_grid(self)
                l_tkinter_utils.set_font(self, font = l_tkinter_utils.make_font(size_mult = 1.5))

        class Button(tk.Button):
            """The combine button."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Combine!")
                l_tkinter_utils.place_on_grid(self, coords = (1, 0))
                l_tkinter_utils.set_font(self, font = l_tkinter_utils.make_font(size_mult = 1.5, bold = True))

    class MiscButtons(tk.Frame):
        """Contains all the miscellaneous buttons."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
            l_tkinter_utils.place_on_grid(self, coords = (0, 3))
            l_tkinter_utils.set_weights(self, x = (1, 1, 1))

            self.w_instructions = self.Instructions(self)
            self.w_about = self.About(self)
            self.w_github = self.Github(self)

        class Instructions(tk.Button):
            """Shows the instructions on how to use."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Instructions...")
                l_tkinter_utils.place_on_grid(self)
                l_tkinter_utils.set_font(self)

        class About(tk.Button):
            """The about button."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "About...")
                l_tkinter_utils.place_on_grid(self, coords = (1, 0))
                l_tkinter_utils.set_font(self)

        class Github(tk.Button):
            """Opens the Github page."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Open Github Page...")
                l_tkinter_utils.place_on_grid(self, coords = (2, 0))
                l_tkinter_utils.set_font(self)
