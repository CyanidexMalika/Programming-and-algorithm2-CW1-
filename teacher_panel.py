import tkinter as tk
from tkinter import messagebox
import cv2
import sqlite3
from datetime import datetime

class TeachersPanel:
    def __init__(self, master=None):
        self.master = master or tk.Tk()
        self.master.title("Teacher's Panel")

        # Connect to the SQLite database
        self.conn = sqlite3.connect('attendance.db')
        self.create_students_table()
        self.create_attendance_table()
        self.create_subject_tables()  # Create tables for subjects
        self.attendance_recorded = set()  # Set to keep track of recorded attendance

        # Welcome label
        welcome_label = tk.Label(self.master, text="Welcome to Teacher's Panel", font=("Arial", 16))
        welcome_label.pack(pady=20)

        # Buttons for taking attendance for different subjects
        subjects = ["Programming", "OS", "Pentest", "Skill Development"]
        for subject in subjects:
            btn_subject_attendance = self.create_custom_button(f"{subject} Attendance", lambda s=subject: self.do_attendance(subject))
            btn_subject_attendance.pack(pady=10)

    def create_custom_button(self, text, command):
        return tk.Button(
            self.master,
            text=text,
            command=command,
            font=("Arial", 12),
            relief=tk.GROOVE,
            bg="#3498db",     # Blue color
            fg="white",
            padx=20,
            pady=10,
            activebackground="#2980b9"  # Darker blue color when active
        )

    def create_students_table(self):
        # Create a 'students' table if not exists
        query = '''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            contact TEXT NOT NULL,
            email TEXT NOT NULL,
            face_id INTEGER NOT NULL
        );
        '''
        self.conn.execute(query)
        self.conn.commit()

    def create_attendance_table(self):
        # Create an 'attendance' table if not exists
        query = '''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            date TEXT DEFAULT CURRENT_DATE,
            subject TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (id)
        );
        '''
        self.conn.execute(query)
        self.conn.commit()

    def create_subject_tables(self):
        # Create tables for subjects if not exists
        subjects = ["Programming", "OS", "Pentest", "Skill Development"]
        for subject in subjects:
            query = f'''
            CREATE TABLE IF NOT EXISTS {subject.lower().replace(" ", "_")}_attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                date TEXT DEFAULT CURRENT_DATE,
                FOREIGN KEY (student_id) REFERENCES students (id)
            );
            '''
            self.conn.execute(query)
            self.conn.commit()

    def do_attendance(self, subject):
        # Load the trained model
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer.yml')

        # Load the cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Open the webcam
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                # Recognize the face
                id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])

                # Check if the confidence is within a certain threshold
                if confidence < 100:
                    # Fetch the student ID and name from the database using the recognized ID
                    query = "SELECT id, first_name FROM students WHERE id=?"
                    result = self.conn.execute(query, (id_,)).fetchone()

                    if result:
                        student_id, student_name = result

                        # Check if attendance already recorded for this student on the current date and subject
                        attendance_key = (student_id, datetime.now().date(), subject)
                        if attendance_key not in self.attendance_recorded:
                            # Insert attendance data into the subject-specific table
                            status = "Present"  # You can modify this based on your logic
                            attendance_query = f"INSERT INTO {subject.lower().replace(' ', '_')}_attendance (student_id, status, date) VALUES (?, ?, ?)"
                            self.conn.execute(attendance_query, (student_id, status, datetime.now().date()))
                            self.conn.commit()

                            # Add to the set to mark attendance as recorded
                            self.attendance_recorded.add(attendance_key)

                            # Display the student name and ID on the frame
                            cv2.putText(frame, f"ID: {student_id} - {student_name} - Status: {status}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                            # Show a prompt that attendance is done for the student
                            messagebox.showinfo("Attendance Done", f"Attendance recorded for {student_name} in {subject}")

                # Draw a rectangle around the face for tracking
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # Display the student name within the tracking box
                cv2.putText(frame, f"ID: {id_} - {student_name}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Display the frame
            cv2.imshow('Live Attendance', frame)

            # Break the loop when 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the webcam and close the window
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    teachers_panel = TeachersPanel()
    teachers_panel.master.mainloop()
