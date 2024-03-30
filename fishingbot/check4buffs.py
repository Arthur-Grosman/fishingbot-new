import time
import pyautogui

from basics import my_log

DoBuffs = True
BuffTimer2 = 0

def Check4Buffs():
    global BuffTimer2

    # apply lure
    BuffTimerDiff = time.time() * 1000 - BuffTimer2
    if DoBuffs and BuffTimerDiff > 600000:  # 600000 milliseconds = 10 minutes

        # deleting junk with "dejunk" addon
        my_log("Deleting Junk.")
        for i in range(5):
            pyautogui.hotkey('alt', '0')
            time.sleep(0.2)

        # lure on "2" and fishing rod on "3"
        my_log("Casting buff on key: '2'")
        pyautogui.press('2')
        time.sleep(0.3)
        pyautogui.press('3')
        time.sleep(10)

        BuffTimer2 = time.time() * 1000