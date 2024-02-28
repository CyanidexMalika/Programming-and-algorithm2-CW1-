import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import cv2
import os
import numpy as np

class StudentsDetailWindow:
    def __init__(self, master, conn):
        self.master = master
        self.master.title("Students Detail")

        # Pass the connection to the StudentsDetailWindow class
        self.conn = conn

        # Create a title label
        title_label = tk.Label(self.master, text="Students", font=("Arial", 20))
        title_label.pack(pady=10)

        # Create a frame for student registration
        registration_frame = tk.Frame(self.master, bd=5, relief=tk.RIDGE)
        registration_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Widgets for student registration frame
        registration_label = tk.Label(registration_frame, text="Student Registration", font=("Arial", 14))
        registration_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Entry widgets for student registration
        self.first_name_entry = self.create_entry(registration_frame, "First Name:", row=1)
        self.last_name_entry = self.create_entry(registration_frame, "Last Name:", row=2)
        self.contact_entry = self.create_entry(registration_frame, "Contact:", row=3)
        self.email_entry = self.create_entry(registration_frame, "Email:", row=4)

        # Button to add student
        add_button = tk.Button(registration_frame, text="Add Student", command=self.add_student)
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Button to train face recognition
        train_face_button = tk.Button(registration_frame, text="Train Face", command=self.train_face_recognition)
        train_face_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Button to delete selected student
        delete_button = tk.Button(registration_frame, text="Delete Selected", command=self.delete_selected_student)
        delete_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Create a frame for displaying student details
        details_frame = tk.Frame(self.master, bd=5, relief=tk.RIDGE)
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Treeview to display student details
        self.student_table = ttk.Treeview(
            details_frame,
            columns=("First Name", "Last Name", "Contact", "Email"),
            show="headings"
        )

        # Define column headings
        self.student_table.heading("First Name", text="First Name", anchor=tk.CENTER)
        self.student_table.heading("Last Name", text="Last Name", anchor=tk.CENTER)
        self.student_table.heading("Contact", text="Contact", anchor=tk.CENTER)
        self.student_table.heading("Email", text="Email", anchor=tk.CENTER)

        # Pack the Treeview
        self.student_table.pack(fill=tk.BOTH, expand=1)

        # Populate the initial student details
        self.populate_student_details()

    def create_entry(self, frame, label_text, row):
        label = tk.Label(frame, text=label_text)
        label.grid(row=row, column=0, sticky="w", pady=5)

        entry = tk.Entry(frame)
        entry.grid(row=row, column=1, sticky="w", pady=5)

        return entry

    def create_students_table(self):
        # Create a 'students' table if not exists
        query = '''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            contact TEXT NOT NULL,
            email TEXT NOT NULL
        );
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_student(self):
        # Get values from entry widgets
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        contact = self.contact_entry.get()
        email = self.email_entry.get()

        # Validate email format
        if not self.is_valid_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        # Validate contact (numeric only)
        if not self.is_valid_contact(contact):
            messagebox.showerror("Invalid Contact", "Please enter a valid numeric contact number.")
            return

        # Insert data into 'students' table
        query = "INSERT INTO students (first_name, last_name, contact, email) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (first_name, last_name, contact, email))
        self.conn.commit()

        # Clear entry widgets
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

        # Update the displayed student details
        self.populate_student_details()

        messagebox.showinfo("Student Added", "Student information added successfully.")

    def is_valid_email(self, email):
        # Simple email validation using a regular expression
        return "@" in email and "." in email

    def is_valid_contact(self, contact):
        # Check if the contact is numeric
        return contact.isdigit()

    def train_face_recognition(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        faces = []
        labels = []

        # Fetch student details from the database
        query = "SELECT * FROM students"
        students = self.conn.execute(query).fetchall()

        for student in students:
            face_id = student[0]
            face_path = f"faces/{student[1]}_{face_id}.jpg"

            if not os.path.exists(face_path):
                # Capture student face and save it
                camera = cv2.VideoCapture(0)
                _, frame = camera.read()
                camera.release()

                # Detect faces in the captured frame
                faces_detected = detector.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces_detected:
                    face = frame[y:y+h, x:x+w]
                    cv2.imwrite(face_path, cv2.cvtColor(face, cv2.COLOR_BGR2GRAY))
                    break

            face_image = cv2.imread(face_path, cv2.IMREAD_GRAYSCALE)

            # Detect faces in the image
            faces_detected = detector.detectMultiScale(face_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces_detected:
                faces.append(face_image[y:y+h, x:x+w])
                labels.append(face_id)

        if faces and labels:
            recognizer.train(faces, np.array(labels))
            recognizer.save('trainer.yml')
            messagebox.showinfo("Success", "Student added and Face captured successfully.")

    def delete_selected_student(self):
        # Get the selected item from the Treeview
        selected_item = self.student_table.selection()

        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student to delete.")
            return

        # Get the student details from the selected item
        student_details = self.student_table.item(selected_item, 'values')

        # Confirm deletion with a messagebox
        confirmation = messagebox.askyesno("Delete Student", "Are you sure you want to delete this student?")

        if confirmation:
            try:
                # Fetch the corresponding student ID from the database
                query = "SELECT id FROM students WHERE first_name=? AND last_name=? AND contact=? AND email=?"
                result = self.conn.execute(query, student_details).fetchone()

                if result:
                    student_id = result[0]

                    # Delete the selected student from the database
                    delete_query = "DELETE FROM students WHERE id=?"
                    self.conn.execute(delete_query, (student_id,))
                    self.conn.commit()

                    # Update the displayed student details
                    self.populate_student_details()

                    messagebox.showinfo("Student Deleted", "Student information deleted successfully.")
                else:
                    messagebox.showwarning("No Matching Student", "No matching student found in the database.")
            except Exception as e:
                print(f"Error deleting student: {e}")

    def populate_student_details(self):
        # Clear existing data in the Treeview
        for row in self.student_table.get_children():
            self.student_table.delete(row)

        # Fetch student details from the database
        query = "SELECT * FROM students"
        students = self.conn.execute(query).fetchall()

        # Display student details in the Treeview
        for student in students:
            self.student_table.insert("", tk.END, values=student[1:])

class AdminPanel:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Admin Panel")

        # Connect to the SQLite database
        self.conn = sqlite3.connect('attendance.db')
        self.create_students_table()

        # Welcome label
        welcome_label = tk.Label(self.root, text="Welcome to Admin Panel", font=("Arial", 16))
        welcome_label.pack(pady=20)

        # Buttons
        btn_students = self.create_custom_button("Students", self.open_students)
        btn_students.pack(pady=10)

        btn_face_detector = self.create_custom_button("Face Detector", self.open_live_face_detector)
        btn_face_detector.pack(pady=10)


    def create_custom_button(self, text, command):
        return tk.Button(
            self.root,
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
            email TEXT NOT NULL
        );
        '''
        self.conn.execute(query)
        self.conn.commit()

    def open_students(self):
        # Open the Students Detail window
        students_detail_window = tk.Toplevel(self.root)
        students_detail = StudentsDetailWindow(students_detail_window, self.conn)

    def open_live_face_detector(self):
    # Load the trained model
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer.yml')

    # Load the cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open the webcam
        cap = cv2.VideoCapture(0)

    # Pass the connection to the StudentsDetailWindow instance
        students_detail_window = tk.Toplevel(self.root)
        students_detail = StudentsDetailWindow(students_detail_window, self.conn)

        while students_detail_window.winfo_exists():  # Check if the window exists
            ret, frame = cap.read()

        # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
            # Recognize the face
                id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            # Check if the confidence is within a certain threshold
                if confidence < 50:
                # Fetch the name from the database using the recognized ID
                    query = "SELECT first_name FROM students WHERE id=?"
                    result = students_detail.conn.execute(query, (id_,)).fetchone()

                    if result:
                        student_name = result[0]
                    else:
                        student_name = "Unknown"

                # Draw a rectangle around the face and display the name
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cv2.putText(frame, student_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Display the frame
            cv2.imshow('Face Detection', frame)

        # Break the loop when 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the webcam and close the window
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Create 'faces' directory if not exists
    if not os.path.exists('faces'):
        os.makedirs('faces')

    admin_panel = AdminPanel()
    admin_panel.root.mainloop()