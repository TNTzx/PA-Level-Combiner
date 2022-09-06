"""Contains the full UI."""


import tkinter as tk

import l_tkinter_utils


class MainWindow(tk.Toplevel):
    """The main window."""

    class Title(l_tkinter_utils.Title):
        """The title."""

    class LevelSelect(tk.Frame):
        """The level select."""

        class Title(l_tkinter_utils.Title):
            """The level select title."""

        class LevelList(l_tkinter_utils.ScrolledListbox):
            """The level list."""

        class EditButtons(l_tkinter_utils.AddRemoveEdit):
            """The edit buttons."""

    class Output(l_tkinter_utils.EntryBrowseForm):
        """The output folder form."""

    class VersionSelect(l_tkinter_utils.OptionMenuForm):
        """The version select dropdown."""

    class CombineControls(tk.Frame):
        """Contains the combining controls."""

        class Options(tk.Button):
            """Contains all combine options."""

        class Button(tk.Button):
            """The combine button."""

    class MiscButtons(tk.Frame):
        """Contains all the miscellaneous buttons."""

        class Instructions(tk.Button):
            """Shows the instructions on how to use."""

        class About(tk.Button):
            """The about button."""

        class Github(tk.Button):
            """Opens the Github page."""
