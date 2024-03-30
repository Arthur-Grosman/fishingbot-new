import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import os
import time
from datetime import datetime
import keyboard


def capture_and_save_screenshots(window_name, save_dir, cutoff_percentage=5, interval=1):
    # Find the window by title
    w = gw.getWindowsWithTitle(window_name)

    if not w:
        print(f"Window with title '{window_name}' not found.")
        return

    w = w[0]

    # Activate the window
    w.activate()

    # Check if the save directory exists
    if not os.path.exists(save_dir):
        print(f"Save directory '{save_dir}' does not exist. Please create the directory.")
        return

    screenshot_count = 0

    try:
        while True:
            # Get the position and size of the window
            x, y, width, height = w.left, w.top, w.width, w.height

            # Calculate the cutoff values
            cutoff_x = int(width * cutoff_percentage / 100)
            cutoff_y = int(height * cutoff_percentage / 100)

            # Calculate the new region for capturing the screenshot
            capture_region = (x + cutoff_x, y + cutoff_y, width - 2 * cutoff_x, height - 2 * cutoff_y)

            # Capture screenshot of the specific window region
            screenshot = pyautogui.screenshot(region=capture_region)

            # Convert the screenshot to a NumPy array
            screenshot_np = np.array(screenshot)

            # Convert the BGR image to RGB
            screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)

            # Generate a timestamp for unique filenames
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            # Save the screenshot with a unique filename
            screenshot_filename = os.path.join(save_dir, f"screenshot_{timestamp}_{screenshot_count + 1}.png")
            cv2.imwrite(screenshot_filename, screenshot_rgb)

            print(f"Screenshot {screenshot_count + 1} saved: {screenshot_filename}")

            # Wait for the specified interval
            time.sleep(interval)

            screenshot_count += 1

            # Check if the Backspace key is pressed to interrupt the loop
            if keyboard.is_pressed("backspace"):
                print("Screenshot capture interrupted by Backspace key.")
                break

    except KeyboardInterrupt:
        print("Screenshot capture interrupted.")


if __name__ == "__main__":
    # Set the window name
    window_name = "World of Warcraft"

    # Set the directory to save screenshots
    save_directory = r"C:\Users\Arthur\Documents\fishingbot\data\startwowimages"

    # Cutoff percentage on each side
    cutoff_percentage = 1

    # Interval between screenshots (in seconds)
    interval = 1

    # Capture and save screenshots until interrupted by the user
    capture_and_save_screenshots(window_name, save_directory, cutoff_percentage, interval)
