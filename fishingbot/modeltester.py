from ultralytics import YOLO
import cv2
import pygetwindow as gw
import numpy as np
import pyautogui
import time

# Function to capture a specific window by its title
def capture_window(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        x, y, width, height = window.left, window.top, window.width, window.height
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return img
    except IndexError:
        return None

# Specify the title of the currently running window
window_title = "Google Chrome"  # Replace with the actual window title

# Initialize YOLO model
model = YOLO('startwowbest.pt')

# Main loop for continuous capturing and tracking
while True:
    # Capture the window and use it as the video source
    window_img = capture_window(window_title)

    # Check if the window was successfully captured
    if window_img is not None:
        # Track the objects in the captured window
        results = model.track(source=window_img, show=True, save=False, tracker="bytetrack.yaml")
        for result in results:
            if 0 in result.names:
                object_boxes = result.boxes.xyxy[result.boxes.cls == 0]
                object_confidence = result.boxes.conf[result.boxes.cls == 0]

                for object_box, confidence in zip(object_boxes, object_confidence):
                    x_min, y_min, x_max, y_max = object_box
                    print(
                        f"Object detected at Upper Left: ({x_min}, {y_min}), Bottom Right: ({x_max}, {y_max}), Confidence: {confidence}")

    else:
        print(f"Window with title '{window_title}' not found.")
        break  # Exit the loop if the window is not found

    # You may want to introduce a delay here to control the frame rate
    time.sleep(0.05)
    # For example, time.sleep(0.1) to wait for 0.1 seconds between frames
