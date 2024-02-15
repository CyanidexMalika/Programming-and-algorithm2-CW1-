import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
import os

class CustomButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            relief=tk.FLAT,
            bg="#4CAF50",  # Background color
            fg="white",   # Text color
            font=("Helvetica", 12),
            padx=10,      # Horizontal padding
            pady=5,       # Vertical padding
            activebackground="#45a049",  # Background color when active
            activeforeground="white",     # Text color when active
            cursor="hand2"                # Cursor style
        )

class MyApplication:
    def __init__(self, window, window_title, video_source=0, canvas_width=800, canvas_height=600):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.is_capturing = False
        self.is_registering = False
        
        self.frame = tk.Frame(window, bg="#f0f0f0")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas to display the video feed
        self.canvas = tk.Canvas(self.frame, bg="black", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(padx=10, pady=(10, 0))
        
        # Buttons for starting and stopping video capture
        self.btn_start = CustomButton(self.frame, text="Start Capture", width=15, command=self.start_capture)
        self.btn_start.pack(side=tk.LEFT, padx=10, pady=(20, 0))
        
        self.btn_stop = CustomButton(self.frame, text="Stop Capture", width=15, command=self.stop_capture, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=10, pady=(20, 0))
        
        self.btn_register = CustomButton(self.frame, text="Register Face", width=15, command=self.register_face, state=tk.DISABLED)
        self.btn_register.pack(side=tk.LEFT, padx=10, pady=(20, 0))
        
        # Open the video source
        self.vid = cv2.VideoCapture(self.video_source)
        if not self.vid.isOpened():
            raise RuntimeError("Error: Could not open video source")
        
        # Initialize canvas with a blank image
        self.blank_image = np.zeros((self.canvas_height, self.canvas_width, 3), np.uint8)
        self.blank_image[:] = (0, 0, 0)
        self.blank_photo = ImageTk.PhotoImage(image=Image.fromarray(self.blank_image))
        
        # Load the pre-trained face detection model
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Start the update loop to display video frames
        self.update()
        
        # Handle window closing event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Prevent window from being resized
        self.window.resizable(False, False)
        
        # Start the Tkinter window
        self.window.mainloop()
        
    def start_capture(self):
        self.is_capturing = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.btn_register.pack(side=tk.LEFT, padx=10, pady=(20, 0))  # Show the Register Face button
        self.btn_register.config(state=tk.NORMAL)  # Enable the Register Fac button
        
    def stop_capture(self):
        self.is_capturing = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.btn_register.pack_forget()  
        self.btn_register.config(state=tk.DISABLED)  # Disable the Register Face button
        # Clear the canvas
        self.clear_canvas()
        
    def register_face(self):
        pass  
        
    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.blank_photo, anchor=tk.NW)
        
    def update(self):
        # Updating video frames continuously
        if self.is_capturing:
            ret, frame = self.vid.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # This part fixes mirror video footage from the webcam
                rgb_frame = cv2.flip(rgb_frame, 1)
                
                # Detecting face in every single frames of the video captureeee
                faces = self.face_cascade.detectMultiScale(rgb_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                
                # Draw rectangles around the detected faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(rgb_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                # Resize the video frame to match the canvas size
                rgb_frame = cv2.resize(rgb_frame, (self.canvas_width, self.canvas_height))
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(rgb_frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        else:
            # Clear the canvas and display blank image
            self.clear_canvas()
        self.window.after(10, self.update)
        
    def on_closing(self):
        # Release the video source and closing the window
        if self.vid.isOpened():
            self.vid.release()
        self.window.destroy()


MyApplication(tk.Tk(), "Video Capture")
