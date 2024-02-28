import unittest
import sqlite3
from unittest.mock import patch
from tkinter import Tk
from unittest.mock import patch, MagicMock
from datetime import datetime
from teacher_panel import TeachersPanel
from admin_panel import StudentsDetailWindow
from test import LoginPage

class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.login_page = LoginPage()

    def tearDown(self):
        self.login_page.root.destroy()

    def test_create_users_table(self):
        # Create a temporary in-memory SQLite database for testing
        self.login_page.conn = sqlite3.connect(':memory:')
        # Call the method to create the users table
        self.login_page.create_users_table()

        # Fetch table information from SQLite and assert if it's created correctly
        cursor = self.login_page.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        result = cursor.fetchone()
        self.assertIsNotNone(result, "Users table should exist")

    @patch('tkinter.Tk.mainloop')
    def test_run(self, mock_mainloop):
        self.login_page.run()
        mock_mainloop.assert_called_once()



class TestTeachersPanel(unittest.TestCase):

    @patch('cv2.VideoCapture')
    @patch('cv2.CascadeClassifier')
    @patch('cv2.face_LBPHFaceRecognizer.create')
    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.Tk')
    @patch('sqlite3.connect')
    def test_do_attendance(self, mock_conn, mock_tk, mock_messagebox, mock_recognizer_create, mock_cascade, mock_video_capture):
        # Setup mocks
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cap = MagicMock()
        mock_video_capture.return_value = mock_cap
        mock_recognizer = MagicMock()
        mock_recognizer.read.return_value = None
        mock_recognizer.predict.return_value = (1, 0)  # Assuming recognized face ID is 1 with confidence 0
        mock_recognizer_create.return_value = mock_recognizer

        # Create instance of TeachersPanel
        panel = TeachersPanel()

        pass



class TestStudentsDetailWindow(unittest.TestCase):

    def setUp(self):
        # Create a mock master object
        self.master = MagicMock()
        # Create a mock SQLite connection
        self.conn = MagicMock(spec=sqlite3.Connection)
        # Initialize StudentsDetailWindow with the mock master and connection
        self.window = StudentsDetailWindow(master=self.master, conn=self.conn)

    def test_is_valid_email(self):
        valid_email = "test@example.com"
        invalid_email = "invalid_email"

        self.assertTrue(self.window.is_valid_email(valid_email))
        self.assertFalse(self.window.is_valid_email(invalid_email))

    def test_is_valid_contact(self):
        valid_contact = "1234567890"
        invalid_contact = "abc"

        self.assertTrue(self.window.is_valid_contact(valid_contact))
        self.assertFalse(self.window.is_valid_contact(invalid_contact))

    def test_add_student(self):
        pass

if __name__ == '__main__':
    unittest.main()
