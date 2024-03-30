import pyautogui
import pygetwindow as gw
import time
from datetime import datetime


def my_log(msg):
    import datetime
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"{current_time}: {msg}")

    with open('log.txt', 'a') as file:
        file.write(f"{current_time}: {msg}\n")


def take_screen(save_path):
    # Wait for a moment to make sure the window is activated
    time.sleep(2)

    # Get the currently focused window
    active_window = gw.getWindowsWithTitle(gw.getActiveWindow().title)[0]

    # Take a screenshot of the window
    screenshot = pyautogui.screenshot(
        region=(active_window.left, active_window.top, active_window.width, active_window.height))

    # Generate a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Set the desired save path
    save_path = fr"{save_path}\screenshot_{timestamp}.png"

    # Save the screenshot to the specified path with the generated filename
    screenshot.save(save_path)
    return save_path


# Example usage
if __name__ == "__main__":
    # Set the desired save path
    save_path = r"C:\Users\Arthur\Documents\fishingbot\screenshots"

    # Call the function to take a screenshot with the specified save path
    saved_path = take_screen(save_path)
    print(f"Screenshot saved at: {saved_path}")

    my_log('running basics.py')
