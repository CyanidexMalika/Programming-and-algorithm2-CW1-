import tkinter as tk
import cv2
from PIL import Image, ImageTk

class MyApplication:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.is_capturing = False
        
        
        self.canvas = tk.Canvas(window, width=800, height=600)
        self.canvas.pack()
        
        # Buttons to starting the webcam and closing
        self.btn_start = tk.Button(window, text="Start Capture", width=20, command=self.start_capture)
        self.btn_start.pack(side=tk.LEFT, padx=5, pady=10)
        
        self.btn_stop = tk.Button(window, text="Stop Capture", width=20, command=self.stop_capture, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Video source opening ho hai
        self.vid = cv2.VideoCapture(self.video_source)
        if not self.vid.isOpened():
            raise RuntimeError("Error: Could not open video source")
        
        # Start the update loop to display video frames
        self.update()
        
    
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Starting the Tkinter windoiw
        self.window.mainloop()
        
    def start_capture(self):
        self.is_capturing = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        
    def stop_capture(self):
        self.is_capturing = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
    # Clears the last frame from stop capture getting stuck
        self.canvas.delete("all")

        
    def update(self):
        # updating video frames continuously
        if self.is_capturing:
            ret, frame = self.vid.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # This part fixes mirror video footage from the webcam
                rgb_frame = cv2.flip(rgb_frame, 1)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(rgb_frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)
        
    def on_closing(self):
# Release the video source and closing the window
        if self.vid.isOpened():
            self.vid.release()
        self.window.destroy()


MyApplication(tk.Tk(), "Video Capture")
