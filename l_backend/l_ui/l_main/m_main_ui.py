"""Contains the full UI."""


from __future__ import annotations

import typing as typ

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfd

import webbrowser

import l_tkinter_utils
import l_pa_cls_simple

from ... import l_library
from .. import m_combine_option, m_ui_excs, l_extra_info
from . import m_main_mixin, m_checks


class MainWindow(tk.Toplevel, m_main_mixin.MainWindowMixin):
    """The main window."""
    def __init__(self, parent: tk.Widget, combine_job: l_library.CombineJob = None):
        if combine_job is None:
            combine_job = l_library.CombineJob(version = l_pa_cls_simple.v20_4_4, output_folder_path = "D:/Xander Files/[1] cluster/[1] self/[4] programming/[1] tools/pa level combiner/v2/test environment/combining/output/test")

        super().__init__(parent)
        l_tkinter_utils.set_weights(self, y = (1 for _ in range(4)))
        l_tkinter_utils.window_set_size(self, 1280, 720)
        l_tkinter_utils.window_center_to_screen(self)
        l_tkinter_utils.window_set_title(self, "PA Level Combiner")

        l_tkinter_utils.notebook_set_style()


        self.w_title = self.Title(self)
        self.w_view_manager = self.ViewManager(self)
        self.w_combine_controls = self.CombineButton(self)
        self.w_misc_buttons = self.MiscButtons(self)

        self.w_instructions = None
        self.w_about = None

        self.w_simple = self.w_view_manager.w_simple
        self.w_level_listbox = self.w_simple.w_level_select.w_level_list.w_listbox

        self.w_advanced = self.w_view_manager.w_advanced


        self.level_folder_paths = [
            str(level_folder) for level_folder in combine_job.level_folders
        ] + [
            "D:/Xander Files/[1] cluster/[1] self/[4] programming/[1] tools/pa level combiner/v2/test environment/combining/base/pacm combine level 1",
            "D:/Xander Files/[1] cluster/[1] self/[4] programming/[1] tools/pa level combiner/v2/test environment/combining/base/pacm combine level 2"
        ]
        l_tkinter_utils.listbox_update(self.w_simple.w_level_select.w_level_list.w_listbox, self.level_folder_paths)
        self.combine_settings = combine_job.combine_settings


        self.w_simple.w_version_select.w_option_menu.variable.set(
            combine_job.version.get_description()
            if combine_job.version is not None else
            self.w_simple.w_version_select.initial
        )


        self.w_simple.w_output.w_browse.w_entry.variable.set(combine_job.output_folder_path)


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

        l_tkinter_utils.button_link(self.w_combine_controls.w_button, self.run_combine_job)


        l_tkinter_utils.button_link(self.w_misc_buttons.w_instructions, self.open_instructions)
        l_tkinter_utils.button_link(self.w_misc_buttons.w_about, self.open_about)
        l_tkinter_utils.button_link(self.w_misc_buttons.w_github, self.open_github)


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
        """Updates the source level label."""
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
        while True:
            path = tkfd.askdirectory(title = "Select a folder containing a level")
            if path == "":
                return

            try:
                m_checks.check_level_folder(self.get_version(), path)
            except m_ui_excs.LevelFolderImportException as exc:
                l_tkinter_utils.messagebox(self, "Invalid level folder!", str(exc), (l_tkinter_utils.Options.ok, ))
                continue

            break

        self.level_folder_paths.append(path)


    @_update_wrapper
    def edit_level_folder(self):
        """Edits a level folder."""
        selected = l_tkinter_utils.listbox_get_selected(self.w_level_listbox, self.level_folder_paths)
        if len(selected) != 1:
            l_tkinter_utils.error_messagebox(self, "You must select one and only one item to edit.")
            return
        selected: str = selected[0]

        while True:
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

            try:
                m_checks.check_level_folder(self.get_version(), form_result)
            except m_ui_excs.LevelFolderImportException as exc:
                l_tkinter_utils.messagebox(self, "Invalid level folder!", str(exc), (l_tkinter_utils.Options.ok, ))
                continue

            break

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
        if not version_widget.is_filled():
            raise m_ui_excs.VersionNotSelected()

        return l_pa_cls_simple.PAVersion.get_version_from_description(version_widget.get_result())

    def get_level_folders(self):
        """Gets the level folders in the list."""
        version = self.get_version()
        if len(self.level_folder_paths) == 0:
            raise m_ui_excs.NoLevelFolders()

        first_level_folder = version.import_level_folder(self.level_folder_paths[0])
        if len(self.level_folder_paths) > 1:
            rest_level_folders = [
                version.import_level_folder(folder_path, load_audio = False)
                for folder_path in self.level_folder_paths[1:]
            ]
        else:
            rest_level_folders = []

        return [first_level_folder] + rest_level_folders

    def get_base_level_folder(self):
        """Gets the base level."""
        base_level_form = self.w_advanced.w_base_level
        if not base_level_form.is_filled():
            return None

        return self.get_version().import_level_folder(base_level_form.get_result())

    def get_output_path(self):
        """Gets the output path."""
        output_form = self.w_simple.w_output
        if not output_form.is_filled():
            raise m_ui_excs.NoOutputPath()

        return output_form.get_result()


    def get_combine_job(self):
        """Gets the combine job."""
        try:
            version = self.get_version()
        except m_ui_excs.VersionNotSelected as exc:
            raise m_ui_excs.GetCombineJobException(str(exc)) from exc
        except l_pa_cls_simple.VersionNotFound as exc:
            raise m_ui_excs.GetCombineJobException(f"Version {exc.missing_version_number} is not supported!") from exc


        def raise_import_exc(import_exc: l_pa_cls_simple.ImportException, source: str):
            """Raises the import exception."""
            new_exc = m_checks.to_lfolder_import_exc(import_exc)
            raise m_ui_excs.GetCombineJobException(f"{source.capitalize()}: " + str(new_exc)) from new_exc

        try:
            level_folders = self.get_level_folders()
        except m_ui_excs.NoLevelFolders as exc:
            raise m_ui_excs.GetCombineJobException(str(exc)) from exc
        except l_pa_cls_simple.ImportException as exc:
            raise_import_exc(exc, "level folder")

        try:
            base_level_folder = self.get_base_level_folder()
        except l_pa_cls_simple.ImportException as exc:
            raise_import_exc(exc, "base level folder")

        try:
            output_folder_path = self.get_output_path()
        except m_ui_excs.NoOutputPath as exc:
            raise m_ui_excs.GetCombineJobException(str(exc)) from exc


        return l_library.CombineJob(
            version = version,
            level_folders = level_folders,
            base_level_folder = base_level_folder,
            output_folder_path = output_folder_path,
            combine_settings = self.combine_settings
        )


    def run_combine_job(self):
        """Runs the combine job."""
        confirm = l_tkinter_utils.messagebox(
            self,
            title = "Confirm Combine Start",
            description = "Do you want to start combining now?",
            options = (l_tkinter_utils.Options.yes, l_tkinter_utils.Options.no)
        )
        if confirm == l_tkinter_utils.Options.no:
            return


        try:
            combine_job = self.get_combine_job()
        except m_ui_excs.GetCombineJobException as exc:
            l_tkinter_utils.error_messagebox(self, str(exc))
            self.set_requires_version_update()
            return


        class JobProgress(l_tkinter_utils.ProgressbarPopup):
            """The progress bar."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent)
                l_tkinter_utils.window_set_size(self, 720, 200)
                l_tkinter_utils.window_center_to_screen(self)

            class TitledProgressbar(l_tkinter_utils.TitledProgressbar):
                """The titled progressbar."""

                class Title(l_tkinter_utils.Title):
                    """The title widget."""
                    def __init__(self, parent: tk.Widget):
                        super().__init__(parent, title = "Combining...")

                class Progressbar(ttk.Progressbar):
                    """The progressbar."""
                    def __init__(self, parent: tk.Widget):
                        super().__init__(parent, orient = tk.HORIZONTAL, mode = "indeterminate")
                        l_tkinter_utils.progress_move(self)


            def set_description(self, desc: str):
                """Sets the description."""
                self.w_titled_progressbar.w_title.set_description(desc)
                self.update()


        job_progress = JobProgress(self)
        # l_tkinter_utils.window_set_visibility(job_progress, False)

        def run_job():
            """Runs the job."""
            l_tkinter_utils.window_set_visibility(job_progress, True)
            l_tkinter_utils.set_active(self, False)

            job_progress.set_description("Combining and writing to output path...")

            combine_job.run_job()

            finish_job()


        def finish_job():
            l_tkinter_utils.window_set_visibility(job_progress, False)

            open_level_folder = "Open Level Folder"
            finish_choose = l_tkinter_utils.messagebox(
                self,
                title = "Finished",
                description = "Combining finished!",
                options = (l_tkinter_utils.Options.ok, open_level_folder)
            )

            l_tkinter_utils.set_active(self, True)

            if finish_choose == open_level_folder:
                l_pa_cls_simple.open_folder_in_explorer(self.get_combine_job().output_folder_path)


        l_tkinter_utils.progress_run_func(run_job)



    def open_instructions(self):
        """Opens the instructions menu."""
        self.w_instructions = l_tkinter_utils.window_open_if_closed(self.w_instructions, l_extra_info.Instructions(self))

    def open_about(self):
        """Opens the about menu."""
        self.w_about = l_tkinter_utils.window_open_if_closed(self.w_about, l_extra_info.About(self))


    def open_github(self):
        """Opens the Github page."""
        def show_error():
            """Shows the error."""
            l_tkinter_utils.error_messagebox(self, "The Chrome browser can't be found!")

        try:
            chrome = webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s &")
        except webbrowser.Error:
            show_error()
            return

        chrome.open_new_tab("https://www.github.com/TNTzx/PA-Level-Combiner")
