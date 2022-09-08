"""Contains the simple view."""


from __future__ import annotations

import typing as typ

import tkinter as tk
import tkinter.filedialog as tkfd

import l_tkinter_utils
import l_pa_cls_simple


class SimpleView(tk.Frame):
    """The simple view."""
    def __init__(self, parent: tk.Widget, main_window: tk.Toplevel):
        super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
        l_tkinter_utils.place_on_grid(self)
        l_tkinter_utils.set_weights(self, y = (1 for _ in range(5)))

        self.w_main_window = main_window

        self.w_version_select = self.VersionSelect(self)
        self.w_level_select = self.LevelSelect(self, main_window)
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
        def __init__(self, parent: tk.Widget, main_window: tk.Toplevel, level_folder_paths: list[str] = None):
            if level_folder_paths is None:
                level_folder_paths = []

            super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
            l_tkinter_utils.place_on_grid(self, coords = (0, 1))
            l_tkinter_utils.set_weights(self, x = (4, 1, 1), y = (1, 2))

            self.w_parent = parent
            self.w_main_window = main_window

            self.w_title = self.Title(self)
            self.w_level_list = self.LevelList(self)

            self.w_edit_buttons = self.EditButtons(self)
            self.w_edit_buttons.add = self.add_level_folder
            self.w_edit_buttons.edit = self.edit_level_folder
            self.w_edit_buttons.remove = self.remove_level_folder

            self.w_select_buttons = self.SelectButtons(self)
            self.w_select_buttons.sel_all = lambda: self.set_select_all(True)
            self.w_select_buttons.sel_none = lambda: self.set_select_all(False)


            self._level_folder_paths = level_folder_paths

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


        def update_listbox(self):
            """Updates the listbox with the level folder paths."""
            l_tkinter_utils.listbox_update(self.w_level_list.w_listbox, self._level_folder_paths)

        @staticmethod
        def _update_wrapper(func: typ.Callable):
            """Adds the update listbox method to the end."""
            def wrapper(self: SimpleView.LevelSelect):
                func(self)
                self.update_listbox()

            return wrapper


        @_update_wrapper
        def add_level_folder(self):
            """Adds a level folder."""
            path = tkfd.askdirectory(title = "Select a folder containing a level")
            if path == "":
                return
            self._level_folder_paths.append(path)


        @_update_wrapper
        def edit_level_folder(self):
            """Edits a level folder."""
            selected = l_tkinter_utils.listbox_get_selected(self.w_level_list.w_listbox, self._level_folder_paths)
            if len(selected) != 1:
                l_tkinter_utils.error_messagebox(self.w_main_window, "You must select one and only one item to edit.")
                return
            selected: str = selected[0]

            class EntryBrowseForm(l_tkinter_utils.EntryBrowseForm):
                """Form......"""
                def __init__(self, parent: tk.Widget):
                    super().__init__(
                        parent,
                        label_text = "Enter the new path to edit the current level folder path.",
                        label_size_mult = 1,
                        initial = selected
                    )

                def browse(self) -> str:
                    return tkfd.askdirectory(title = "Choose a level folder.")

            form_result = l_tkinter_utils.form_messagebox(self.w_main_window, EntryBrowseForm)

            if form_result is None:
                return

            selected_index = self._level_folder_paths.index(selected)
            self._level_folder_paths[selected_index] = form_result


        @_update_wrapper
        def remove_level_folder(self):
            """Deletes the selected level folder."""
            selected_items = l_tkinter_utils.listbox_get_selected(self.w_level_list.w_listbox, self._level_folder_paths)
            if len(selected_items) == 0:
                l_tkinter_utils.error_messagebox(self.w_main_window, "You must select at least one item to delete.")
                return

            confirm = l_tkinter_utils.messagebox(
                self.w_main_window,
                title = "Deleting Level Folders",
                description = "Are you sure you want to delete these level folders?\n" + "\n".join(selected_items),
                options = (l_tkinter_utils.Options.yes, l_tkinter_utils.Options.no)
            )

            if confirm == l_tkinter_utils.Options.no or confirm is None:
                return

            for selected_item_idx in l_tkinter_utils.listbox_get_selected_idx(self.w_level_list.w_listbox):
                del self._level_folder_paths[selected_item_idx]


        def set_select_all(self, select_all: bool):
            """Selects or deselects all items in the listbox."""
            l_tkinter_utils.listbox_set_select_all(self.w_level_list.w_listbox, select_all)


        def get_level_folders(self):
            """Gets the level folders in the list."""
            return [l_pa_cls_simple.LevelFolder.from_folder(folder_path) for folder_path in self._level_folder_paths]

    class Output(l_tkinter_utils.EntryBrowseForm):
        """The output folder form."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, label_text = "Output Level Folder", label_size_mult = 1.5)
            l_tkinter_utils.place_on_grid(self, coords = (0, 2))
