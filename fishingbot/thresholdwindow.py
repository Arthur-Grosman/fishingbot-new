import tkinter as tk

class ThresholdWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Threshold Value")

        self.label = tk.Label(root, text="Enter the threshold value:")
        self.label.pack()

        self.threshold_entry = tk.Entry(root)
        self.threshold_entry.pack()

        self.threshold_entry.focus_set()  # Set focus to the entry field

        self.threshold_entry.bind("<Return>", lambda event: self.submit_threshold())

        # Flag to indicate whether the window should be destroyed
        self.should_destroy = False

    def submit_threshold(self):
        threshold_value = self.threshold_entry.get()
        try:
            threshold_value = float(threshold_value)
            if threshold_value <= 0:
                raise ValueError
            self.should_destroy = True  # Set the flag to destroy the window
            self.threshold_value = threshold_value  # Store the threshold value
        except ValueError:
            # Handle invalid input
            error_label = tk.Label(self.root, text="Please enter a valid positive number")
            error_label.pack()

        if self.should_destroy:
            self.root.destroy()  # Destroy the window

    def get_threshold_value(self):
        # Return the threshold value after the window is destroyed
        return self.threshold_value
