import subprocess
import time
import pygetwindow as gw
import pyautogui
import win32gui
import win32con

import windowcapture
from window_manager import WindowManager
from basics import my_log

# Class Names in startwowbest.pt: {0: 'accountfield', 1: 'battlenetplay', 2: 'classicwowicon', 3: 'enterworld', 4: 'healthbar', 5: 'wowicon'}


def close_window(window_name):
    for tries in range(30):
        hwnd = win32gui.FindWindow(None, window_name)
        if hwnd != 0:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            my_log(f"Tried to close {window_name}")
        else:
            my_log(f"Window {window_name} closed or not found.")
            break
        time.sleep(0.3)
    time.sleep(3)

def is_window_open(title):
    try:
        window = gw.getWindowsWithTitle(title)[0]
        return True
    except IndexError:
        return False

def start_wow(launcher_path, game_version, desired_x, desired_y, desired_width, desired_height):
    # Run launcher
    subprocess.Popen([launcher_path])

    # Wait for Battle.net to open
    timeout = 30
    start_time = time.time()

    while not is_window_open("Battle.net"):
        time.sleep(1)
        if time.time() - start_time > timeout:
            my_log("Timeout: Battle.net window did not open within {} seconds.".format(timeout))
            return 1

    my_log("Battle.net window is open.")
    time.sleep(5)

    # get screen width and height
    screen_width, screen_height = pyautogui.size()
    print("Desktop Width:", screen_width)
    print("Desktop Height:", screen_height)

    # check for (classic) wow icon
    wincap = windowcapture.WindowCapture('Battle.net', 'startwowbest.pt')
    failcount = 0
    for i in range(6):
        if game_version == "classic":
            class_index = 2
        else:
            class_index = 5
        result = wincap.window_capture(class_index, 0, 0, screen_width, screen_height)
        if result != 0 and len(result) > 0:
            pyautogui.click((result[0][0] + result[0][2]) / 2, (result[0][1] + result[0][3]) / 2, duration=0.2)
            break
        else:
            failcount += 1
        time.sleep(5)
    if failcount == 6:
        my_log("Couldn't detect icon screen.")
        return 1
    time.sleep(5)

    # Check for "Play" button
    failcount = 0
    for i in range(6):
        class_index = 1
        result = wincap.window_capture(class_index, 0, 0, screen_width, screen_height)
        if result != 0 and len(result) > 0:
            pyautogui.click((result[0][0] + result[0][2]) / 2, (result[0][1] + result[0][3]) / 2, duration=0.2)
            break
        else:
            failcount += 1
        time.sleep(5)
    if failcount == 6:
        my_log("Couldn't detect 'Play' button.")
        return 1
    time.sleep(5)

    # Wait for WoW window to open
    timeout = 30
    start_time = time.time()

    while not is_window_open("World of Warcraft"):
        time.sleep(1)
        if time.time() - start_time > timeout:
            my_log("Timeout: WoW window did not open within {} seconds.".format(timeout))
            return 1

    my_log("WoW window is open.")
    time.sleep(5)

    wincap = windowcapture.WindowCapture('World of Warcraft', 'startwowbest.pt')
    window_manager = WindowManager('World of Warcraft')
    window_manager.resize_and_move_window(desired_x, desired_y, desired_width, desired_height)
    time.sleep(3)
    close_window("Battle.net")

    # check for "Enter World" button
    for i in range(6):
        class_index = 3
        result = wincap.window_capture(class_index, desired_x, desired_y, desired_width, desired_height)
        if result != 0 and len(result) > 0:
            my_log("'Enter World' button detected.")
            # pyautogui.click((result[0][0] + result[0][2])/2, (result[0][1] + result[0][3])/2, duration=0.2)
            pyautogui.press('enter')
            time.sleep(20)
            return 0
        time.sleep(5)

    my_log("Couldn't detect 'Enter World' button.")
    return 1


if __name__ == "__main__":
    close_window("Battle.net")
    close_window("World of Warcraft")
    start_wow(r"C:\Program Files (x86)\Battle.net\Battle.net.exe", "classic", 0, 0, 1280, 720)
