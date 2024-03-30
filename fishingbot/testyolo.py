from ultralytics import YOLO
from PIL import Image

def detect_bobber(image_path):
    # Load the YOLO model for bobber detection
    model = YOLO('cropped_bobbersearchbest.pt')

    # Run inference on the image
    results = model(image_path)

    # Iterate through the results for each detected object
    for result in results:
        # Process information for each detected object
        print(f"Class names: {result.names}")

        # Check if class index 0 (bobber) is present in the results
        if 0 in result.names:
            # Get the bounding box coordinates for 'bobber'
            bobber_boxes = result.boxes.xyxy[result.boxes.cls == 0]
            bobber_confidence = result.boxes.conf[result.boxes.cls == 0]

            # Iterate through each detected bobber
            for bobber_box in bobber_boxes:
                x_min, y_min, x_max, y_max = bobber_box
                print(f"Bobber detected at Upper Left: ({x_min}, {y_min}), Bottom Right: ({x_max}, {y_max}), Confidence: {bobber_confidence[0]}")

                # Plot the result with bounding boxes
                im_array = result.plot(labels=True, boxes=True)
                im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
                im.show()


# Provide the image path
image_path = r'C:\Users\Arthur\Downloads\nobobbertest.png'
detect_bobber(image_path)
