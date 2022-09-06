"""Contains element selection."""


from __future__ import annotations

import tkinter as tk

import l_tkinter_utils
from l_tkinter_utils import l_utils


class CombineOptionWindow(tk.Toplevel):
    """The element controls."""
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        l_tkinter_utils.window_set_size(self, 1280, 720)
        l_tkinter_utils.window_center_to_screen(self)
        l_tkinter_utils.set_weights(self, y = (1, 1, 1))

        self.w_title = self.Title(self)
        self.w_combine_options = self.CombineOptions(self)
        self.w_confirm_cancel = self.ConfirmCancel(self)

    class Title(l_tkinter_utils.Title):
        """Title."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, title = "Combine Options", description = "Edit combine options.")
            l_tkinter_utils.place_on_grid(self)

    class CombineOptions(tk.Frame):
        """Contains the combine options."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
            l_tkinter_utils.place_on_grid(self, coords = (0, 1))
            l_tkinter_utils.set_weights(self, x = (1, 1))

            self.w_include = self.Include(self)
            self.w_delete_first = self.DeleteFirst(self)

        class CombineOptionSet(tk.Frame):
            """Defines a combine option set."""
            def __init__(self, parent: tk.Widget, options: list[str], label_title: str = "", label_desc: str = ""):
                super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
                l_tkinter_utils.set_weights(self, x = (1, 1))

                self.w_title = self.Title(self, label_title, label_desc)
                self.w_options = self.Options(self, options)

            class Title(l_tkinter_utils.Title):
                """Title."""
                def __init__(self, parent: tk.Widget, title: str, description: str = None):
                    super().__init__(parent, title, description, title_size_mult = 0.5)
                    l_tkinter_utils.place_on_grid(self)

            class Options(tk.Frame):
                """Contains all options."""
                def __init__(self, parent: tk.Widget, options_strs: list[str]):
                    super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
                    l_tkinter_utils.place_on_grid(self, coords = (1, 0))

                    option_type = self.Option
                    self.w_options: list[option_type] = []

                    self.update_options(options_strs)

                class Option(tk.Checkbutton):
                    """The option checkbutton."""
                    def __init__(self, parent: tk.Widget, text: str):
                        self.variable = tk.IntVar()
                        super().__init__(parent, text = text, variable = self.variable, anchor = tk.LEFT)
                        self.text = text


                def update_options(self, option_strs: list[str]):
                    """Updates the options."""
                    for w_option in self.w_options:
                        w_option.destroy()

                    self.w_options.clear()

                    for idx, option_str in enumerate(option_strs):
                        w_option = self.Option(self, text = option_str)
                        l_tkinter_utils.place_on_grid(w_option, coords = (0, idx))
                        self.w_options.append(w_option)

                    l_utils.set_weights(self, y = (1 for _ in option_strs))


                def get_option_strs(self):
                    """Gets the option strings."""
                    return [w_option.text for w_option in self.w_options]

                def get_result(self):
                    """Gets the result."""
                    return {
                        w_option.text: True if w_option.variable.get() == 1 else False
                        for w_option in self.w_options
                    }

        class Include(CombineOptionSet):
            """Contains options that dictate if an element is included or not."""
            def __init__(self, parent: tk.Widget):
                super().__init__(
                    parent,
                    options = [
                        "Beatmap Objects",
                        "Prefabs",
                        "Markers",
                        "Checkpoints",
                        "Event Keyframes",
                        "BG Objects"
                    ],
                    label_title = "Include:"
                )
                l_tkinter_utils.place_on_grid(self)

        class DeleteFirst(CombineOptionSet):
            """Contains options that dictate if the first instance of an element is kept or not."""
            def __init__(self, parent: tk.Widget):
                super().__init__(
                    parent,
                    options = [
                        "Checkpoint",
                        "Event Keyframes"
                    ],
                    label_title = "Delete First:",
                    label_desc = (
                        "If on, this deletes the first checkpoint / event keyframe from all other levels other than the source level.\n"
                        "If off, this keeps the first checkpoints / event keyframes from all levels, essentially having duplicate first checkpoints / event keyframes."
                    )
                )
                l_tkinter_utils.place_on_grid(self, coords = (1, 0))

    class ConfirmCancel(tk.Frame):
        """Contains the confirm and cancel buttons."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
            l_tkinter_utils.place_on_grid(self, coords = (0, 2))
            l_tkinter_utils.set_weights(self, x = (1, 1))

        class Confirm(tk.Button):
            """The confirm button."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Confirm")
                l_tkinter_utils.place_on_grid(self)
                l_tkinter_utils.set_font(self, font = l_tkinter_utils.make_font(size_mult = 1.5, bold = True))

        class Cancel(tk.Button):
            """The cancel button."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Cancel")
                l_tkinter_utils.place_on_grid(self)
                l_tkinter_utils.set_font(self, font = l_tkinter_utils.make_font(size_mult = 1.5))
