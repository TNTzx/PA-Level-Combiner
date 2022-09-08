"""Contains element selection."""


from __future__ import annotations

import copy

import tkinter as tk
import l_pa_cls_simple

import l_tkinter_utils
from l_tkinter_utils import l_utils


class CombineOptionWindow(tk.Toplevel):
    """The element controls."""
    def __init__(self, parent: tk.Widget, combine_settings: l_pa_cls_simple.CombineSettings = None):
        if combine_settings is None:
            combine_settings = l_pa_cls_simple.CombineSettings()

        super().__init__(parent)
        l_tkinter_utils.window_set_size(self, 1000, 600)
        l_tkinter_utils.window_center_to_screen(self)
        l_tkinter_utils.set_weights(self, y = (1, 1, 1))

        self.w_parent = parent

        self.w_title = self.Title(self)
        self.w_combine_options = self.CombineOptions(self)

        self.w_confirm_cancel = self.ConfirmCancel(self)
        l_tkinter_utils.button_link(self.w_confirm_cancel.w_confirm, self.confirm)
        l_tkinter_utils.button_link(self.w_confirm_cancel.w_disregard, self.disregard)


        self.is_confirmed = False


        self.include_options = self.w_combine_options.w_include.w_options.w_options
        include_values = [
            combine_settings.include_beatmap_objects,
            combine_settings.include_prefabs,
            combine_settings.include_markers,
            combine_settings.include_checkpoints,
            combine_settings.include_event_keyframes,
            combine_settings.include_bg_objects
        ]
        for idx, delete_first_value in enumerate(include_values):
            self.include_options[idx].set_value(delete_first_value)

        self.delete_first_options = self.w_combine_options.w_delete_first.w_options.w_options
        delete_first_values = [
            combine_settings.delete_first_checkpoint,
            combine_settings.delete_first_event_keyframes
        ]
        for idx, delete_first_value in enumerate(delete_first_values):
            self.delete_first_options[idx].set_value(delete_first_value)

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
                    super().__init__(parent, title, description, title_size_mult = 0.6)
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
                        self.variable = tk.IntVar(value = 1)
                        super().__init__(parent, text = text, variable = self.variable, anchor = tk.W)
                        l_utils.set_font(self, font = l_tkinter_utils.make_font(size_mult = 1.2))
                        self.text = text

                    def set_value(self, value: bool):
                        """Sets the value of this option."""
                        self.variable.set(1 if value else 0)

                    def get_value(self):
                        """Gets the value of this option."""
                        return bool(self.variable.get())


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
                        w_option.text: bool(w_option.variable.get())
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
                    label_title = "Include:",
                    label_desc = (
                        "If on, it will be taken from all levels and added to the combined level.\n"
                        "If off, it won't be included in the combined level.\n"
                        "Note that the base level will always keep these no matter if it's off or on."
                    )
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
                        "If on, it will be deleted from all other levels other than the source level.\n"
                        "If off, it will be kept for all levels, essentially having duplicates."
                    )
                )
                l_tkinter_utils.place_on_grid(self, coords = (1, 0))

    class ConfirmCancel(tk.Frame):
        """Contains the confirm and cancel buttons."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, **l_tkinter_utils.FRAME_BORDER)
            l_tkinter_utils.place_on_grid(self, coords = (0, 2))
            l_tkinter_utils.set_weights(self, x = (1, 1))

            self.w_confirm = self.Confirm(self)
            self.w_disregard = self.DisregardChanges(self)

        class Confirm(tk.Button):
            """The confirm button."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Confirm Changes")
                l_tkinter_utils.place_on_grid(self)
                l_tkinter_utils.set_font(self, font = l_tkinter_utils.make_font(size_mult = 1.5, bold = True))

        class DisregardChanges(tk.Button):
            """The disregard changes button."""
            def __init__(self, parent: tk.Widget):
                super().__init__(parent, text = "Disregard Changes")
                l_tkinter_utils.place_on_grid(self, coords = (1, 0))
                l_tkinter_utils.set_font(self, font = l_tkinter_utils.make_font(size_mult = 1.5))


    def confirm(self):
        """The confirm button bind."""
        self.is_confirmed = True
        self.destroy()

    def disregard(self):
        """The cancel button bind."""
        self.is_confirmed = False
        self.destroy()


    def get_combine_settings(self):
        """Gets the combine settings according to this form."""
        def get_value(options: list[self.CombineOptions.CombineOptionSet.Options.Option], idx: int):
            """Gets the value of the option in a list with index."""
            return options[idx].get_value()

        def get_value_include(idx: int):
            """Gets the value of the include option with index."""
            return get_value(self.include_options, idx)

        def get_value_delete_first(idx: int):
            """Gets the value of the delete first option with index."""
            return get_value(self.delete_first_options, idx)

        return l_pa_cls_simple.CombineSettings(
            include_beatmap_objects = get_value_include(0),
            include_prefabs = get_value_include(1),
            include_markers = get_value_include(2),
            include_checkpoints = get_value_include(3),
            include_event_keyframes = get_value_include(4),
            include_bg_objects = get_value_include(5),

            delete_first_checkpoint = get_value_delete_first(0),
            delete_first_event_keyframes = get_value_delete_first(1),
        )


    def show(self):
        """Shows this window then returns the combine settings when done."""
        l_tkinter_utils.window_wait_active(self.w_parent, self)
        if not self.is_confirmed:
            return None

        return self.get_combine_settings()


def show_combine_option(parent: tk.Widget, original_combine_settings: l_pa_cls_simple.CombineSettings = None):
    """Shows the combine option window then returns combine settings when closed."""
    if original_combine_settings is None:
        original_combine_settings = l_pa_cls_simple.CombineSettings()

    new_combine_settings = copy.deepcopy(original_combine_settings)

    w_combine_option = CombineOptionWindow(parent, new_combine_settings)
    result = w_combine_option.show()

    if result is None:
        return original_combine_settings

    return result
