"""About window."""


import tkinter as tk

import l_tkinter_utils


class About(tk.Toplevel):
    """Contains the instructions."""
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        l_tkinter_utils.set_weights(self, y = (1, 3))
        l_tkinter_utils.window_set_size(self, 720, 360)
        l_tkinter_utils.window_center_to_screen(self)
        l_tkinter_utils.window_set_title(self, "About")

        self.w_title = self.Title(self)
        self.w_label_format = self.LabelFormat(self)

    class Title(l_tkinter_utils.Title):
        """The title."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, title = "About", title_size_mult = 0.5)
            l_tkinter_utils.place_on_grid(self)

    class LabelFormat(l_tkinter_utils.LabelFormat):
        """The label."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent)
            l_tkinter_utils.place_on_grid(self, coords = (0, 1))

            self.add_texts(
                [
                    l_tkinter_utils.LabelFormatText(
                        "PA Level Combiner",
                        font = l_tkinter_utils.make_font(size_mult = 4, bold = True),
                        anchor = tk.CENTER,
                        justify = tk.CENTER
                    ),
                    l_tkinter_utils.LabelFormatText(
                        (
                            "Program by //TNTzx\n"
                            "\n"
                            "that's it at the moment lmao"
                        ),
                        anchor = tk.CENTER,
                        justify = tk.CENTER
                    )
                ]
            )
