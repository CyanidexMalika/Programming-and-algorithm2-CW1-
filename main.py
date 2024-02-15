import tkinter as tk
import cv2
from PIL import Image, ImageTk

class MyApplication:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.is_capturing = False
        
    
        self.frame = tk.Frame(window, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas to display the video feed
        self.canvas = tk.Canvas(self.frame, bg="black")
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Buttons for starting and stopping video capture
        self.btn_start = tk.Button(self.frame, text="Start Capture", width=15, command=self.start_capture, bg="green", fg="white")
        self.btn_start.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.btn_stop = tk.Button(self.frame, text="Stop Capture", width=15, command=self.stop_capture, bg="red", fg="white", state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Open the video source
        self.vid = cv2.VideoCapture(self.video_source)
        if not self.vid.isOpened():
            raise RuntimeError("Error: Could not open video source")
        
        # Dimensions of video frame
        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Start the update loop to display video frames
        self.update()
        
        # Handle window closing event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Set a fixed window size
        self.window.geometry(f"{self.width + 20}x{self.height + 100}")
        
        # Start the Tkinter window
        self.window.mainloop()
        
    def start_capture(self):
        self.is_capturing = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        
    def stop_capture(self):
        self.is_capturing = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        # Clear the canvas
        self.canvas.delete("all")
        
    def update(self):
        # Updating video frames continuously
        if self.is_capturing:
            ret, frame = self.vid.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # This part fixes mirror video footage from the webcam
                rgb_frame = cv2.flip(rgb_frame, 1)
                # Resize the video frame to match the canvas size
                rgb_frame = cv2.resize(rgb_frame, (self.canvas.winfo_width(), self.canvas.winfo_height()))
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(rgb_frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)
        
    def on_closing(self):
        # Release the video source and closing the window
        if self.vid.isOpened():
            self.vid.release()
        self.window.destroy()

MyApplication(tk.Tk(), "Video Capture")
