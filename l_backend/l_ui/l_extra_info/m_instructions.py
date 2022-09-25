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
                l_tkinter_utils.NotebookFrameInfo("Simple Tab", SimpleTab(self))
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
    """The workflow tab."""
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
                    "Level Select",
                    font = self.header_font,
                    bullet_level = 1
                ),
                l_tkinter_utils.LabelFormatText(
                    "\tThis is where you manage which levels are going to be combined."
                ),

                l_tkinter_utils.LabelFormatText(
                    "Add Level Folder",
                    font = self.header_font,
                    bullet_level = 1
                ),
                l_tkinter_utils.LabelFormatText(
                    (
                        "This is where you add a level folder. Clicking this button will bring up a dialog box which is where you can select a folder that contains a level.\n"
                        "If the level is invalid, an error pops up."
                    ),
                    bullet_char = "\t",
                    bullet_level = 1
                ),
            ]
        )

        
