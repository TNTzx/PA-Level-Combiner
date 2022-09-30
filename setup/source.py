"""Sets up the program."""


import os

import tkinter as tk
import tkinter.filedialog as tkfd

import winshell


os.system("cls")


def create_shortcut(target_file_path: str, save_path: str, icon_path: str = "", start_in_folder_path: str = "", description: str = ""):
    """Creates a shortcut."""
    winshell.CreateShortcut(
        Path = save_path,
        Target = target_file_path,
        StartIn = start_in_folder_path,
        Icon = (icon_path, 0),
        Description = description
    )


CURRENT_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
CODE_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "code"))


def ask_for_shortcut_save():
    """Asks where to save the file. Returns the path."""
    root = tk.Tk()
    root.withdraw()

    file_path = tkfd.asksaveasfilename(
        title = "Save the combiner's shortcut to where?",
        initialdir = os.getcwd(),
        initialfile = "PA Level Combiner",
        defaultextension = "*.lnk",
        filetypes = (("Shortcut File", "*.lnk"), )
    )

    root.destroy()

    if file_path == "":
        raise ValueError("No path selected.")

    return file_path


print("Select shortcut path:")
shortcut_path = ask_for_shortcut_save()

print(shortcut_path)

print("Creating shortcut...")

run_path = os.path.abspath(
    os.path.join(
        CODE_PATH,
        "..", "code", "run.bat"
    )
)

create_shortcut(
    target_file_path = run_path,
    save_path = shortcut_path,
    start_in_folder_path = CODE_PATH,
    description = "The PA Level Combiner tool."
)

print("Created shortcut.")
input("Press Enter to Exit. ")
