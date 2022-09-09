"""Contains the full UI."""


from __future__ import annotations

import typing as typ

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfd

import l_tkinter_utils
import l_pa_cls_simple

from .. import l_library
from . import m_simple, m_advanced, m_combine_option, m_ui_excs


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
        self.w_combine_controls = self.CombineButton(self)
        self.w_misc_buttons = self.MiscButtons(self)


        self.level_folder_paths = combine_job.level_folder_paths
        self.combine_settings = combine_job.combine_settings


        self.w_simple = self.w_view_manager.w_simple
        self.w_level_listbox = self.w_simple.w_level_select.w_level_list.w_listbox

        self.w_advanced = self.w_view_manager.w_advanced


        self.w_simple.w_version_select.w_option_menu.variable.set(
            combine_job.version.get_description()
            if combine_job.version is not None else
            self.w_simple.w_version_select.initial
        )

        self.w_requires_version = [
            self.w_simple.w_level_select,
            self.w_simple.w_output,
            self.w_advanced
        ]

        self.w_simple.w_version_select.on_change = self._version_select_bind
        self.set_requires_version_update()
        self.previous_selected_version = self.w_simple.w_version_select.get_result()
        self._version_select_bind_trigger = True

        level_select_edit_buttons = self.w_simple.w_level_select.w_edit_buttons
        level_select_edit_buttons.add = self.add_level_folder
        level_select_edit_buttons.edit = self.edit_level_folder
        level_select_edit_buttons.remove = self.remove_level_folder

        level_select_sel_buttons = self.w_simple.w_level_select.w_select_buttons
        level_select_sel_buttons.sel_all = lambda: self.set_select_all(True)
        level_select_sel_buttons.sel_none = lambda: self.set_select_all(False)

        self.w_advanced.w_base_level.on_change = self.update_source_level
        self.update_source_level()

        l_tkinter_utils.button_link(self.w_advanced.w_options.w_button, self.open_combine_options)

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

    class CombineButton(tk.Frame):
        """Contains the combining controls."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
            l_tkinter_utils.place_on_grid(self, coords = (0, 2))
            l_tkinter_utils.set_weights(self)

            self.w_button = self.Button(self)

        class Button(tk.Button):
            """The combine button."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Combine!")
                l_tkinter_utils.place_on_grid(self)
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


    def set_active_requires_version(self, active: bool):
        """Sets the activity of the widgets that requires the version field to be filled."""
        for widget in self.w_requires_version:
            l_tkinter_utils.set_active(widget, active)

    def set_requires_version_update(self):
        """Updates the widgets that requires the version field to be filled."""
        self.set_active_requires_version(self.w_view_manager.w_simple.w_version_select.is_filled())

    def _version_select_bind(self):
        """Called when version select is changed."""
        if not self._version_select_bind_trigger:
            self._version_select_bind_trigger = True
            return

        if len(self.level_folder_paths) > 0:
            confirm = l_tkinter_utils.messagebox(
                self,
                title = "Version Select Change Warning",
                description = (
                    "Are you sure you want to change the version?\n"
                    "Changing versions will remove all imported level folders!"
                ),
                options = (l_tkinter_utils.Options.confirm, l_tkinter_utils.Options.cancel)
            )
            if confirm == l_tkinter_utils.Options.cancel:
                self._version_select_bind_trigger = False
                self.w_simple.w_version_select.w_option_menu.variable.set(self.previous_selected_version)
                return

            self.level_folder_paths.clear()
            self.update_level_listbox()

        self.set_requires_version_update()
        self.previous_selected_version = self.w_simple.w_version_select.get_result()


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


    def update_level_listbox(self):
        """Updates the listbox with the level folder paths."""
        l_tkinter_utils.listbox_update(
            self.w_level_listbox,
            self.level_folder_paths
        )
        self.update_source_level()

    @staticmethod
    def _update_wrapper(func: typ.Callable):
        """Adds the update listbox method to the end."""
        def wrapper(self: MainWindow):
            func(self)
            self.update_level_listbox()

        return wrapper


    @_update_wrapper
    def add_level_folder(self):
        """Adds a level folder."""
        path = tkfd.askdirectory(title = "Select a folder containing a level")
        if path == "":
            return
        self.level_folder_paths.append(path)


    @_update_wrapper
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


    @_update_wrapper
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


    def open_combine_options(self):
        """Opens the combine options then sets the combine settings."""
        self.combine_settings = m_combine_option.show_combine_option(self, self.combine_settings)


    def get_version(self):
        """Gets the selected version."""
        version_widget = self.w_simple.w_version_select
        if version_widget.is_filled():
            return l_pa_cls_simple.PAVersion.get_version_from_description(version_widget.get_result())

        return None

    def get_level_folders(self):
        """Gets the level folders in the list."""
        version = self.get_version()
        first_level_folder = version.import_level_folder(self.level_folder_paths[0])
        rest_level_folders = [
            version.import_level_folder(folder_path, load_audio = False)
            for folder_path in self.level_folder_paths[1:]
        ]

        level_folders = [first_level_folder] + rest_level_folders
        if len(level_folders) == 0:
            raise m_ui_excs.NoLevelFolders()

        return level_folders

    def get_base_level_folder(self):
        """Gets the base level."""
        base_level_form = self.w_advanced.w_base_level
        if not base_level_form.is_filled():
            return None

        return self.get_version().import_level_folder(base_level_form.get_result())

    def get_output_path(self):
        """Gets the output path."""
        return self.w_simple.w_output.get_result()


    def get_combine_job(self):
        """Gets the combine job."""
        try:
            version = self.get_version()
        except l_pa_cls_simple.VersionNotFound as exc:
            raise m_ui_excs.GetCombineJobException(f"Version {exc.missing_version_number} is not supported!") from exc


        import_excs = (l_pa_cls_simple.FolderNotFound, l_pa_cls_simple.LevelFileNotFound, l_pa_cls_simple.IncompatibleVersionImport)

        def raise_import_exc(import_exc: l_pa_cls_simple.ImportException, level_folder_type: str):
            """Raises a `GetCombineJobException` based on the import exception."""
            if isinstance(import_exc, l_pa_cls_simple.FolderNotFound): # TEST
                raise m_ui_excs.GetCombineJobException(
                    f"The {level_folder_type} {import_exc.not_found_folder} can't be found!"
                ) from exc
            if isinstance(import_exc, l_pa_cls_simple.LevelFileNotFound): # TEST
                raise m_ui_excs.GetCombineJobException(
                    f"The {level_folder_type} {exc.level_folder_path} doesn't have the {exc.missing_file} file!"
                ) from exc
            if isinstance(import_exc, l_pa_cls_simple.IncompatibleVersionImport): # TEST
                raise m_ui_excs.GetCombineJobException(
                    (
                        f"The {level_folder_type} {exc.level_folder_path} with version {exc.importing_version_num} "
                        f"is not compatible with the currently selected version ({exc.current_version_num})."
                    )
                ) from exc

        try:
            level_folders = self.get_level_folders()
        except m_ui_excs.NoLevelFolders as exc: # TEST
            raise m_ui_excs.GetCombineJobException(str(exc)) from exc
        except import_excs as exc:
            raise_import_exc(exc, "level folder")

        try:
            base_level_folder = self.get_base_level_folder()
        except import_excs as exc: # TEST
            raise_import_exc(exc, "base level folder")


        output_folder_path = self.get_output_path()


        return l_library.CombineJob(
            version = version,
            level_folders = level_folders,
            base_level_folder = base_level_folder,
            output_folder_path = output_folder_path,
            combine_settings = self.combine_settings
        )


    def run_combine_job(self):
        """Runs the combine job."""
        # TODO
        # TODO remember to make the output path if it doesn't exist
