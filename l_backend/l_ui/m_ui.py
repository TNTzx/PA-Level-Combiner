"""Contains the full UI."""


import tkinter as tk

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
        self.w_version_select = self.VersionSelect(self)
        self.w_level_select = self.LevelSelect(self)
        self.w_output = self.Output(self)
        self.w_combine_controls = self.CombineControls(self)
        self.w_misc_buttons = self.MiscButtons(self)

    class Title(l_tkinter_utils.Title):
        """The title."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, title = "PA Level Combiner", description = "A program used to combine levels.")
            l_tkinter_utils.place_on_grid(self)

    class VersionSelect(l_tkinter_utils.OptionMenuForm):
        """The version select dropdown."""
        def __init__(self, parent: tk.Widget):
            super().__init__(
                parent,
                label_text = "PA Version",
                options = [
                    version.get_description() for version in l_pa_cls_simple.PAVersion.get_all_versions()
                ],
                initial = "Select PA Version..."
            )
            l_tkinter_utils.place_on_grid(self, coords = (0, 1))

    class LevelSelect(tk.Frame):
        """The level select."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
            l_tkinter_utils.place_on_grid(self, coords = (0, 2))
            l_tkinter_utils.set_weights(self, x = (3, 1), y = (1, 2))

            self.w_title = self.Title(self)
            self.w_level_list = self.LevelList(self)
            self.w_edit_buttons = self.EditButtons(self)

        class Title(l_tkinter_utils.Title):
            """The level select title."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, title = "Level Folder List", title_size_mult = 0.5)
                l_tkinter_utils.place_on_grid(self, span_set = (2, 1))

        class LevelList(l_tkinter_utils.ScrolledListbox):
            """The level list."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent)
                l_tkinter_utils.place_on_grid(self, coords = (0, 1))

        class EditButtons(l_tkinter_utils.AddRemoveEdit):
            """The edit buttons."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, item_label = "Level Folder")
                l_tkinter_utils.place_on_grid(self, coords = (1, 1))

    class Output(l_tkinter_utils.EntryBrowseForm):
        """The output folder form."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, label_text = "Output Level Folder")
            l_tkinter_utils.place_on_grid(self, coords = (0, 3))

    class CombineControls(tk.Frame):
        """Contains the combining controls."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
            l_tkinter_utils.place_on_grid(self, coords = (0, 4)) # TODO
            l_tkinter_utils.set_weights(self, x = (1, 1))

            self.w_options = self.Options(self)
            self.w_button = self.Button(self)

        class Options(tk.Button):
            """Contains all combine options."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Combining Options...")
                l_tkinter_utils.place_on_grid(self)
                l_tkinter_utils.set_font(self)

        class Button(tk.Button):
            """The combine button."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Combine!")
                l_tkinter_utils.place_on_grid(self, coords = (1, 0))
                l_tkinter_utils.set_font(self, font = l_tkinter_utils.make_font(bold = True))

    class MiscButtons(tk.Frame):
        """Contains all the miscellaneous buttons."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
            l_tkinter_utils.place_on_grid(self, coords = (0, 5))
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
