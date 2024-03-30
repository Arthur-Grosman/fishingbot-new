# window_manager.py

import win32gui
import win32con

class WindowManager:
    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        self.hwnd_desktop = win32gui.GetDesktopWindow()

    def resize_and_move_window(self, desired_x=0, desired_y=0, desired_width=1280, desired_height=720):
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.MoveWindow(self.hwnd, desired_x, desired_y, desired_width, desired_height, True)
