"""Contains element selection."""


from __future__ import annotations

import tkinter as tk

import l_tkinter_utils


class CombineOptionWindow(tk.Toplevel):
    """The element controls."""

    class Title(l_tkinter_utils.Title):
        """Title."""

    class CombineOptions(tk.Frame):
        """Contains the combine options."""

        class CombineOptionSet(tk.Frame):
            """Defines a combine option set."""
            def __init__(self, parent: tk.Widget, options: list[str], label_text: str = ""):
                super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)

                self.w_title = self.Title(self, label_text)
                self.w_options = self.Options(self, options)

            class Title(l_tkinter_utils.Title):
                """Title."""
                def __init__(self, parent: tk.Widget, label_text: str = ""):
                    super().__init__(parent, title = label_text)
                    l_tkinter_utils.place_on_grid(self)

            class Options(tk.Frame):
                """Contains all options."""
                def __init__(self, parent: tk.Widget, options: list[str]):
                    super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
                    l_tkinter_utils.place_on_grid(self, coords = (1, 0))

                    self.w_options = []
                    self.w_options: self.Option

                class Option(tk.Checkbutton):
                    """The option checkbutton."""
                    def __init__(self, parent: tk.Widget, text: str):
                        super().__init__(parent, text = text)

                def update_options(self):
                    """Updates the options."""
                    for w_option in self.w_options:
                        w_option



        class Include(CombineOptionSet):
            """Contains options that dictate if an element is included or not."""

        class DeleteFirst(CombineOptionSet):
            """Contains options that dictate if the first instance of an element is kept or not."""


    class ConfirmCancel(tk.Frame):
        """Contains the confirm and cancel buttons."""

        class Confirm(tk.Button):
            """The confirm button."""

        class Cancel(tk.Button):
            """The cancel button."""

test: list[CombineOptionWindow.CombineOptions.CombineOptionSet.Options.Option]
