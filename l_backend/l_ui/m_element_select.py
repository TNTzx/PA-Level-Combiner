"""Contains element selection."""


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
            options: list[str]

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
