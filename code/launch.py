"""Launches the main program. This is the script for launching with batch files."""


import win32.lib.win32con as w32con
import win32.win32gui as w32gui

import main


def run():
    """le run"""
    console_window = w32gui.GetForegroundWindow()
    w32gui.ShowWindow(console_window, w32con.SW_HIDE)

    main.main()

    w32gui.ShowWindow(console_window, w32con.SW_SHOW)


if __name__ == "__main__":
    run()
