"""Contains the instructions UI."""


import tkinter as tk
import tkinter.ttk as ttk

import l_tkinter_utils


class Instructions(tk.Toplevel):
    """Contains the instructions."""
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        l_tkinter_utils.set_weights(self, y = (1, 3, 1))
        l_tkinter_utils.window_set_size(self, 720, 720)
        l_tkinter_utils.window_center_to_screen(self)

        self.w_title = self.Title(self)
        self.w_notebook = self.Notebook(self)
        self.w_close = self.Close(self)

    class Title(l_tkinter_utils.Title):
        """The title."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, title = "Instructions", title_size_mult = 0.5)
            l_tkinter_utils.place_on_grid(self)

    class Notebook(ttk.Notebook):
        """Notebook!"""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, height = 500, width = 500)
            l_tkinter_utils.place_on_grid(self, coords = (0, 1))

            self.frame_infos = [
                l_tkinter_utils.NotebookFrameInfo("Workflow", WorkflowTab(self)),
                l_tkinter_utils.NotebookFrameInfo("Simple Tab", SimpleTab(self)),
                l_tkinter_utils.NotebookFrameInfo("Advanced Tab", AdvancedTab(self))
            ]

            l_tkinter_utils.notebook_add_frames(self, self.frame_infos)

    class Close(tk.Button):
        """The close button."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent, text = "Close")
            l_tkinter_utils.place_on_grid(self, coords = (0, 2))
            l_tkinter_utils.set_font(self)


class InstructionTab(l_tkinter_utils.ScrollableFrame):
    """Instruction tab."""
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        l_tkinter_utils.place_on_grid(self)

        self.w_label_format = self.LabelFormat(self.w_canvas.w_frame)

        self.title_font = l_tkinter_utils.make_font(size_mult = 2, bold = True)
        self.header_font = l_tkinter_utils.make_font(bold = True)

    class LabelFormat(l_tkinter_utils.LabelFormat):
        """The label."""
        def __init__(self, parent: tk.Widget):
            super().__init__(parent)
            l_tkinter_utils.place_on_grid(self)

    def set_texts(self, texts: list[l_tkinter_utils.LabelFormatText]):
        """Sets the texts."""
        self.w_label_format.add_texts(texts)


class WorkflowTab(InstructionTab):
    """The workflow tab."""
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        self.set_texts(
            [
                l_tkinter_utils.LabelFormatText(
                    "Workflow",
                    font = self.title_font,
                    anchor = tk.CENTER
                ),
                l_tkinter_utils.LabelFormatText(
                    "1. Select the PA version of the levels that you'll use to combine."
                ),
                l_tkinter_utils.LabelFormatText(
                    "2. Add your level folders using the \"Add Level Folder\" button. Edit and delete if necessary."
                ),
                l_tkinter_utils.LabelFormatText(
                    "3. Create a folder to store the combined level, then use the \"Browse\" button to set the output folder to that folder."
                ),
                l_tkinter_utils.LabelFormatText(
                    "4. Set other combine options in the \"Advanced\" tab."
                ),
                l_tkinter_utils.LabelFormatText(
                    "5. Press the combine button!"
                )
            ]
        )


class SimpleTab(InstructionTab):
    """The simple tab."""
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        self.set_texts(
            [
                l_tkinter_utils.LabelFormatText(
                    "The Simple Tab",
                    font = self.title_font,
                    anchor = tk.CENTER
                ),

                l_tkinter_utils.LabelFormatText(
                    "PA Version",
                    font = self.header_font,
                    bullet_level = 1
                ),
                l_tkinter_utils.LabelFormatText(
                    (
                        "\tThis is where you select the PA version. The available PA versions are the only ones supported in the program.\n"
                        "\tInitially, most buttons are deactivated. To activate them, select a PA version.\n"
                        "\n"
                        "\tYou have to select the PA version where all of the levels that you're going to combine are in. "
                        "If your levels are not in the same version, you can open the levels in the PA editor with your desired version, then save the levels.\n"
                        "\n"
                        "\tSwitching versions while you still have added levels will remove the levels in the list after a warning pops up.\n"
                        "\tThe \"Clear\" button besides the PA version select will clear the PA version. This will also remove the levels in the list if there are any.\n"
                        "\n"
                        "\tYogurt"
                    )
                ),

                l_tkinter_utils.LabelFormatText(
                    "Level Folder List",
                    font = self.header_font,
                    bullet_level = 1
                ),
                l_tkinter_utils.LabelFormatText(
                    "\tThis is where you manage which levels are going to be combined."
                ),

                    l_tkinter_utils.LabelFormatText(
                        "Add Level Folder",
                        font = self.header_font,
                        bullet_level = 2
                    ),
                    l_tkinter_utils.LabelFormatText(
                        (
                            "This is where you add a level folder. Clicking this button will bring up a dialog box which is where you can select a folder that contains a level.\n"
                            "If the level is invalid (not compatible with selected version, can't be imported, etc.), an error pops up.\n"
                            "To exit without adding, simply close the dialog box."
                        ),
                        bullet_char = "\t",
                        bullet_level = 2
                    ),

                    l_tkinter_utils.LabelFormatText(
                        "Edit Level Folder",
                        font = self.header_font,
                        bullet_level = 2
                    ),
                    l_tkinter_utils.LabelFormatText(
                        (
                            "Edits the selected level folder. "
                            "You must select one and only one level folder to edit."
                        ),
                        bullet_char = "\t",
                        bullet_level = 2
                    ),

                    l_tkinter_utils.LabelFormatText(
                        "Delete Level Folder",
                        font = self.header_font,
                        bullet_level = 2
                    ),
                    l_tkinter_utils.LabelFormatText(
                        (
                            "Deletes the selected level folders. "
                            "You must select more than one level folder to delete from the list.\n"
                            "Note that this doesn't delete the folder from the disk, it only removes it from the list of level folders being combined.\n"
                        ),
                        bullet_char = "\t",
                        bullet_level = 2
                    ),


                l_tkinter_utils.LabelFormatText(
                    "Output Level Folder",
                    font = self.header_font,
                    bullet_level = 1
                ),
                l_tkinter_utils.LabelFormatText(
                    "\tThis is where you enter where the combined level will go to.\n"
                    "\tClick the \"Browse\" button to browse for a folder. If the entered folder doesn't exist, the program will try to make it."
                )
            ]
        )


class AdvancedTab(InstructionTab):
    """The advanced tab."""
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        self.set_texts(
            [
                l_tkinter_utils.LabelFormatText(
                    "The Advanced Tab",
                    font = self.title_font,
                    anchor = tk.CENTER
                ),

                l_tkinter_utils.LabelFormatText(
                    "Combine Options",
                    font = self.header_font,
                    bullet_level = 1
                ),
                l_tkinter_utils.LabelFormatText(
                    (
                        "This contains all the options for combining. Clicking this button will display a window for all the combine options."
                    ),
                    bullet_char = "\t",
                    bullet_level = 1
                ),

                    l_tkinter_utils.LabelFormatText(
                        "Include",
                        font = self.header_font,
                        bullet_level = 2
                    ),
                    l_tkinter_utils.LabelFormatText(
                        (
                            "This is where you choose which level elements (markers, beatmap objects, etc.) will be included in the combined level. "
                                "A check mark besides the element means that the element will be included in the combined level. "
                                "No check mark means the element will not be included.\n"
                            "For example, if \"Markers\" is enabled, then all markers from the levels being combined will be included in the combined level. "
                                "If \"Markers\" is disabled, then there would be no markers in the combined level.\n"
                            "The program supports one-level combining, where you can add just one level. "
                                "Changing the \"Include\" options can function as removing markers / checkpoints / etc. from a level.\n"
                            "\n"
                            "Note that if \"Checkpoints\" and/or \"Event Keyframes\" are unchecked, "
                                "the combined level will still include the default first checkpoints and/or event keyframes "
                                "which are derived from a new blank level."
                        ),
                        bullet_char = "\t",
                        bullet_level = 2
                    ),

                    l_tkinter_utils.LabelFormatText(
                        "Delete First",
                        font = self.header_font,
                        bullet_level = 2
                    ),
                    l_tkinter_utils.LabelFormatText(
                        (
                            "This dictates if first checkpoints / event keyframes should be included.\n"
                            "If an element is checked, the first instance of that element (seen at the start of the level) "
                                "for every level to be combined will not be included, and instead will be taken from the source level (see below). "
                                "This means that there will only be one of that element at the start of the level and there would be no duplicates.\n"
                            "If an element is unchecked, first instances of that element (seen at the start of the level) from all levels will be included, "
                                "which will give out a level with duplicate checkpoints / event keyframes at the start of the level.\n"
                        ),
                        bullet_char = "\t",
                        bullet_level = 2
                    ),


                l_tkinter_utils.LabelFormatText(
                    "Base Level",
                    font = self.header_font,
                    bullet_level = 1
                ),
                l_tkinter_utils.LabelFormatText(
                    (
                        "This is a level in which all elements will be included regardless of the combine options.\n"
                        "An example use case of this is where you are the host of a collab, and you have a base level with only markers and checkpoints. "
                            "This base level is what you send out to your collab members. "
                            "After receiving each person's part, you'd want to combine these parts, but in doing so, you'd duplicate the level's markers and checkpoints. "
                            "Using the combine options won't help since if you were to not include the markers and checkpoints, there would be no markers and checkpoints in the combined level. "
                            "This feature fixes that, where you can put the base level with only the markers and checkpoints in, then you can uncheck \"Markers\" and \"Checkpoints\" on the combine options. "
                            "This will discard all the markers and checkpoints from the parts, but it'll still keep the markers and checkpoints from the base level, which will give a combined level with no duplicate markers and checkpoints."
                    ),
                    bullet_char = "\t",
                    bullet_level = 1
                ),

                l_tkinter_utils.LabelFormatText(
                    "Source Level",
                    font = self.header_font,
                    bullet_level = 1
                ),
                l_tkinter_utils.LabelFormatText(
                    (
                        "This is the level folder in which the metadata, audio, first checkpoints and event keyframes (if included), and other information will be derived from.\n"
                        "The base level will be the source level, but if it's not entered, the first level in the list of levels will be used as the source level."
                    ),
                    bullet_char = "\t",
                    bullet_level = 1
                ),
            ]
        )
