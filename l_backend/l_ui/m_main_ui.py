"""Contains the full UI."""


from __future__ import annotations

import typing as typ

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfd

import l_tkinter_utils
import l_pa_cls_simple

from .. import l_library
from . import m_simple, m_advanced


class MainWindow(tk.Toplevel):
    """The main window."""
    def __init__(self, parent: tk.Widget, combine_job: l_library.CombineJob = None):
        if combine_job is None:
            combine_job = l_library.CombineJob()

        super().__init__(parent)
        l_tkinter_utils.set_weights(self, y = (1 for _ in range(4)))
        l_tkinter_utils.window_set_size(self, 1280, 720)
        l_tkinter_utils.window_center_to_screen(self)
        l_tkinter_utils.window_set_title(self, "PA Level Combiner")

        self.w_title = self.Title(self)
        self.w_view_manager = self.ViewManager(self)
        self.w_combine_controls = self.CombineControls(self)
        self.w_misc_buttons = self.MiscButtons(self)


        self.w_simple = self.w_view_manager.w_simple
        self.w_level_listbox = self.w_simple.w_level_select.w_level_list.w_listbox

        self.w_advanced = self.w_view_manager.w_advanced


        self.w_requires_version = [
            self.w_simple.w_level_select,
            self.w_simple.w_output,

            self.w_advanced.w_base_level,
            self.w_advanced.w_current_source_level
        ]

        self.w_view_manager.w_simple.w_version_select.on_change = self.set_requires_version_update
        self.set_requires_version_update()


        self.level_folder_paths = combine_job.level_folder_paths

    class Title(l_tkinter_utils.Title):
        """The title."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, title = "PA Level Combiner")
            l_tkinter_utils.place_on_grid(self)

    class ViewManager(ttk.Notebook):
        """The view manager."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent)
            l_tkinter_utils.place_on_grid(self, coords = (0, 1))
            l_tkinter_utils.notebook_set_style(self)

            self.w_simple = m_simple.SimpleView(self)
            self.w_advanced = m_advanced.AdvancedView(self)

            frames = [
                l_tkinter_utils.NotebookFrameInfo("Simple", self.w_simple),
                l_tkinter_utils.NotebookFrameInfo("Advanced", self.w_advanced)
            ]
            l_tkinter_utils.notebook_add_frames(self, frames)

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
                l_tkinter_utils.set_font(self, font = l_tkinter_utils.make_font(size_mult = 1.2))

        class Button(tk.Button):
            """The combine button."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Combine!")
                l_tkinter_utils.place_on_grid(self, coords = (1, 0))
                l_tkinter_utils.set_font(self, font = l_tkinter_utils.make_font(size_mult = 1.2, bold = True))

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


    def set_active_requires_version(self, active: bool):
        """Sets the activity of the widgets that requires the version field to be filled."""
        for widget in self.w_requires_version:
            l_tkinter_utils.set_active(widget, active)

    def set_requires_version_update(self):
        """Updates the widgets that requires the version field to be filled."""
        self.set_active_requires_version(self.w_view_manager.w_simple.w_version_select.is_filled())


    def update_level_listbox(self):
        """Updates the listbox with the level folder paths."""
        l_tkinter_utils.listbox_update(
            self.w_level_listbox,
            self.level_folder_paths
        )

    @staticmethod
    def update_wrapper(func: typ.Callable):
        """Adds the update listbox method to the end."""
        def wrapper(self: MainWindow):
            func(self)
            self.update_level_listbox()

        return wrapper


    @update_wrapper
    def add_level_folder(self):
        """Adds a level folder."""
        path = tkfd.askdirectory(title = "Select a folder containing a level")
        if path == "":
            return
        self.level_folder_paths.append(path)


    @update_wrapper
    def edit_level_folder(self):
        """Edits a level folder."""
        selected = l_tkinter_utils.listbox_get_selected(self.w_level_listbox, self.level_folder_paths)
        if len(selected) != 1:
            l_tkinter_utils.error_messagebox(self, "You must select one and only one item to edit.")
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

        form_result = l_tkinter_utils.form_messagebox(self, EntryBrowseForm, "Edit Level Folder Path")

        if form_result is None:
            return

        selected_index = self.level_folder_paths.index(selected)
        self.level_folder_paths[selected_index] = form_result


    @update_wrapper
    def remove_level_folder(self):
        """Deletes the selected level folder."""
        selected_items = l_tkinter_utils.listbox_get_selected(self.w_level_listbox, self.level_folder_paths)
        if len(selected_items) == 0:
            l_tkinter_utils.error_messagebox(self, "You must select at least one item to delete.")
            return

        confirm = l_tkinter_utils.messagebox(
            self,
            title = "Deleting Level Folders",
            description = "Are you sure you want to delete these level folders?\n" + "\n".join(selected_items),
            options = (l_tkinter_utils.Options.yes, l_tkinter_utils.Options.no)
        )

        if confirm == l_tkinter_utils.Options.no or confirm is None:
            return

        for selected_item_idx in l_tkinter_utils.listbox_get_selected_idx(self.w_level_listbox):
            del self.level_folder_paths[selected_item_idx]


    def set_select_all(self, select_all: bool):
        """Selects or deselects all items in the listbox."""
        l_tkinter_utils.listbox_set_select_all(self.w_level_listbox, select_all)


    def get_level_folders(self):
        """Gets the level folders in the list."""
        return [l_pa_cls_simple.LevelFolder.from_folder(folder_path) for folder_path in self.level_folder_paths]


    def update_source_level(self):
        """Updates the source level."""
        base_level_form = self.w_advanced.w_base_level
        current_source_level = self.w_advanced.w_current_source_level

        if base_level_form.is_filled():
            current_source_level.update_text(True, "Base Level", base_level_form.get_result())
        elif len(self.level_folder_paths) > 0:
            current_source_level.update_text(True, "First Level", self.level_folder_paths[0])
        else:
            current_source_level.update_text(False)
