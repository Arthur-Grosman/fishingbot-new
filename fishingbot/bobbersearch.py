import cv2
import numpy as np
import pyautogui
import time

from basics import my_log

def get_average_rgb(start_x, start_y, end_x, end_y):
    # Capture the screen
    screenshot = pyautogui.screenshot(region=(start_x, start_y, end_x - start_x, end_y - start_y))

    # Convert the screenshot to a NumPy array
    img_np = np.array(screenshot)

    # Convert the color from BGR to RGB (OpenCV uses BGR by default)
    img_rgb = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    # Calculate the average RGB values
    average_rgb = np.mean(img_rgb, axis=(0, 1))

    return average_rgb

def monitor_region(threshold, start_x, start_y, end_x, end_y, timeout=30):
    start_time = time.time()
    previous_average_rgb = None

    while True:
        time.sleep(0.1)

        average_rgb = get_average_rgb(start_x, start_y, end_x, end_y)
        print("Average RGB:", average_rgb)

        # Check if there's a previous value to compare
        if previous_average_rgb is not None:
            # Calculate the absolute difference between the current and previous average RGB values
            difference = np.abs(average_rgb - previous_average_rgb)

            # Check if any channel exceeds the threshold
            if np.any(difference > threshold):
                my_log("Movement detected!")
                return 0

        # Update the previous value
        previous_average_rgb = average_rgb

        # Check if the timeout has been reached
        if time.time() - start_time > timeout:
            my_log("No significant change detected within the timeout.")
            return 1

# Example usage
if __name__ == "__main__":
    bbx1, bby1, bbx2, bby2 = 100, 50, 200, 150
    threshold_value = 5

    result = monitor_region(threshold_value, bbx1, bby1, bbx2, bby2)
    print("Result:", result)
