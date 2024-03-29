"""Contains the simple view."""


from __future__ import annotations

import tkinter as tk
import tkinter.filedialog as tkfd

import l_tkinter_utils
import l_pa_cls_simple


class SimpleView(tk.Frame):
    """The simple view."""
    def __init__(self, parent: tk.Widget):
        super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
        l_tkinter_utils.place_on_grid(self)
        l_tkinter_utils.set_weights(self, y = (1 for _ in range(5)))

        self.w_version_select = self.VersionSelect(self)
        self.w_level_select = self.LevelSelect(self)
        self.w_output = self.Output(self)

    class VersionSelect(l_tkinter_utils.OptionMenuForm):
        """The version select dropdown."""
        def __init__(self, parent: tk.Widget):
            super().__init__(
                parent,
                label_text = "PA Version",
                label_size_mult = 1.5,
                options = [
                    version.get_description() for version in l_pa_cls_simple.PAVersion.get_all_versions()
                ],
                initial = "Select PA Version..."
            )
            l_tkinter_utils.place_on_grid(self)

    class LevelSelect(tk.Frame):
        """The level select."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
            l_tkinter_utils.place_on_grid(self, coords = (0, 1))
            l_tkinter_utils.set_weights(self, x = (4, 1, 1), y = (1, 2))

            self.w_parent = parent

            self.w_title = self.Title(self)
            self.w_level_list = self.LevelList(self)

            self.w_edit_buttons = self.EditButtons(self)
            self.w_select_buttons = self.SelectButtons(self)

        class Title(l_tkinter_utils.Title):
            """The level select title."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, title = "Level Folder List", title_size_mult = 0.5)
                l_tkinter_utils.place_on_grid(self, span_set = (3, 1))

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

        class SelectButtons(l_tkinter_utils.SelectControls):
            """Contains select controls."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent)
                l_tkinter_utils.place_on_grid(self, coords = (2, 1))

    class Output(l_tkinter_utils.EntryBrowseForm):
        """The output folder form."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, label_text = "Output Level Folder", label_size_mult = 1.5)
            l_tkinter_utils.place_on_grid(self, coords = (0, 2))

        def browse(self) -> str:
            return tkfd.askdirectory()
