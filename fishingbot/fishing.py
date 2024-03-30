import time
import random
import pyautogui
import windowcapture
from bobbersearch import monitor_region
from startwow import start_wow, close_window
from check4buffs import Check4Buffs
from basics import take_screen
from basics import my_log

# import tkinter as tk
# from thresholdwindow import ThresholdWindow

launcher_path = r"C:\Program Files (x86)\Battle.net\Battle.net.exe"
game_version = "classic"
desired_x = 0
desired_y = 0

desired_width = 1280
desired_height = int(desired_width * 0.5625)

# path for screenshots if something doesn't work
save_path = r"C:\Users\Arthur\Documents\fishingbot\screenshots"

threshold_value = 4

'''root = tk.Tk()
threshold_window = ThresholdWindow(root)
root.mainloop()

threshold_value = threshold_window.get_threshold_value()
print("Threshold value:", threshold_value)'''


def do_fishing():
    # count how many times we have thrown the bobber
    longbreakcounter = 0

    while True:
        wincap = windowcapture.WindowCapture('World of Warcraft', 'bobbersearchbest.pt')

        Check4Buffs()
        time.sleep(2)

        notfound = 0
        while True:
            pyautogui.press("1")
            time.sleep(3)

            # Find bobber
            class_index = 0
            result = wincap.window_capture(class_index, desired_x, desired_y, desired_width, desired_height)
            if result != 0 and len(result) > 0:
                my_log("Bobber detected.")
                break
            else:
                notfound += 1

            if notfound == 5:
                my_log("Bobber not found 5 times in a row.")
                saved_path = take_screen(save_path)
                my_log(f"Screenshot saved at: {saved_path}")
                return 1
            time.sleep(5)

        # Get the bounding box of the bobber
        bbx1 = int(result[0][0]) + desired_x  # bounding box upper left (x)
        bby1 = int(result[0][1]) + desired_y  # bounding box upper left (y)
        bbx2 = int(result[0][2]) + desired_x  # bounding box bottom right (x)
        bby2 = int(result[0][3]) + desired_y  # bounding box bottom right (y)

        # check if the bobber has moved
        result = monitor_region(threshold_value, bbx1, bby1, bbx2, bby2)

        # Bobber has moved, click after a short delay
        if result == 0:
            time.sleep(random.uniform(0.1, 0.5))
            pyautogui.rightClick((bbx1 + bbx2) / 2, (bby1 + bby2) / 2, duration=0.2)

        # breaks
        if longbreakcounter == 150:
            my_log("Doing long break.")
            time.sleep(random.uniform(120, 300))
            longbreakcounter = 0
        else:
            time.sleep(random.uniform(1, 1.5))
            longbreakcounter += 1

# do_fishing()

for failcount in range(41):
    status = start_wow(launcher_path, game_version, desired_x, desired_y, desired_width, desired_height)
    if status == 0:
        do_fishing()
    close_window("World of Warcraft")
    close_window("Battle.net")
exit(0)

