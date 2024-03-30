import numpy as np
import win32gui, win32ui, win32con
from ultralytics import YOLO
from PIL import Image

from window_manager import WindowManager
from basics import my_log


class WindowCapture:
    def __init__(self, window_name, model_file):
        self.window_manager = WindowManager(window_name)
        self.yolo_model = YOLO(model_file)

    def get_screenshot(self, roi_x1, roi_y1, roi_x2, roi_y2):
        wDC = win32gui.GetWindowDC(self.window_manager.hwnd_desktop)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        roi_x2 = roi_x2 + roi_x1
        roi_y2 = roi_y2 + roi_y1
        dataBitMap.CreateCompatibleBitmap(dcObj, roi_x2 - roi_x1, roi_y2 - roi_y1)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (roi_x2 - roi_x1, roi_y2 - roi_y1), dcObj, (roi_x1, roi_y1), win32con.SRCCOPY)
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (roi_y2 - roi_y1, roi_x2 - roi_x1, 4)
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.window_manager.hwnd_desktop, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        img = img[..., :3]
        img = np.ascontiguousarray(img)
        return img

    def analyze_screenshot(self, screenshot, class_index):
        my_log(f"Analyzing screenshot for class index {class_index}...")
        yolo_results = self.yolo_model.predict(screenshot)
        detected_objects = []

        for yolo_result in yolo_results:
            if class_index in yolo_result.names:
                object_boxes = yolo_result.boxes.xyxy[yolo_result.boxes.cls == class_index]
                object_confidence = yolo_result.boxes.conf[yolo_result.boxes.cls == class_index]

                for object_box, confidence in zip(object_boxes, object_confidence):
                    x_min, y_min, x_max, y_max = object_box
                    my_log(
                        f"Object detected at Upper Left: ({x_min}, {y_min}), Bottom Right: ({x_max}, {y_max}), Confidence: {confidence}")
                    detected_objects.append((x_min, y_min, x_max, y_max, confidence))

                    '''# Plot the result with bounding boxes
                    im_array = yolo_result.plot(labels=True, boxes=True)
                    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
                    im.show()'''

        return detected_objects if detected_objects else None

    def window_capture(self, class_index, roi_x1, roi_y1, roi_x2, roi_y2):
        screenshot = self.get_screenshot(roi_x1, roi_y1, roi_x2, roi_y2)
        result_from_analyze = self.analyze_screenshot(screenshot, class_index)

        if result_from_analyze:
            return result_from_analyze

        # No object detected, return 0
        return 0


# Example usage:
if __name__ == "__main__":
    wincap = WindowCapture('World of Warcraft',
                           'bobbersearchbest.pt')

    # Import and use the WindowManager class for resizing and moving the window
    from window_manager import WindowManager

    window_manager = WindowManager('World of Warcraft')
    window_manager.resize_and_move_window(desired_x=0, desired_y=0, desired_width=1280, desired_height=720)

    # Specify the region of interest: top-left corner (x1, y1) and bottom-right corner (x2, y2)
    result = wincap.window_capture(class_index=0, roi_x1=0, roi_y1=0, roi_x2=1280, roi_y2=720)

    if result != 0 and len(result) > 0:
        print(f"Confidence: {result[0][4]}")
    else:
        print("No object detected.")
