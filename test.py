import tkinter as tk
from tkinter import messagebox
import sqlite3
from admin_panel import AdminPanel
from teacher_panel import TeachersPanel

class LoginPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login Page")

        # Connect to the SQLite database
        self.conn = sqlite3.connect('attendance.db')
        self.create_users_table()

        # Welcome label
        welcome_label = tk.Label(self.root, text="Welcome to the Login Page", font=("Arial", 16))
        welcome_label.pack(pady=20)

        # Buttons for teacher and admin login
        btn_teacher_login = self.create_custom_button("Teacher's Login", "teacher")
        btn_teacher_login.pack(pady=10)

        btn_admin_login = self.create_custom_button("Admin Login", "admin")
        btn_admin_login.pack(pady=10)

    def create_custom_button(self, text, role):
        return tk.Button(
            self.root,
            text=text,
            command=lambda: self.open_login_form(role),
            font=("Arial", 12),
            relief=tk.GROOVE,
            bg="#3498db",     # Blue color
            fg="white",
            padx=20,
            pady=10,
            activebackground="#2980b9"  # Darker blue color when active
        )

    def create_users_table(self):
        # Create a 'users' table if not exists
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        );
        '''
        self.conn.execute(query)
        self.conn.commit()

    def open_login_form(self, role):
        login_form = LoginForm(self.root, role, self.conn, self)
        login_form.run()

    def run(self):
        self.root.mainloop()

class LoginForm:
    def __init__(self, master, role, conn, login_page):
        self.master = master
        self.master.withdraw()  # Hide the main window temporarily

        self.login_form = tk.Toplevel(self.master)
        self.login_form.title(f"{role.capitalize()} Login")

        self.role = role
        self.conn = conn
        self.login_page = login_page

        # Entry widgets for username and password
        self.create_label("Username:")
        self.username_entry = self.create_entry()

        self.create_label("Password:")
        self.password_entry = self.create_entry(is_password=True)

        # Button for login
        btn_login = tk.Button(
            self.login_form,
            text="Login",
            command=self.login,
            font=("Arial", 12),
            relief=tk.GROOVE,
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10,
            activebackground="#2980b9"
        )
        btn_login.pack(pady=10)

    def create_label(self, text):
        label = tk.Label(self.login_form, text=text, font=("Arial", 12))
        label.pack(pady=5)

    def create_entry(self, is_password=False):
        entry = tk.Entry(self.login_form, show='*' if is_password else None, font=("Arial", 12))
        entry.pack(pady=10)
        return entry

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check the role of the user from the database
        query = "SELECT role FROM users WHERE username=? AND password=?"
        result = self.conn.execute(query, (username, password)).fetchone()

        if result:
            role = result[0]

            if role == "admin":
                # Open the Admin Panel
                self.open_admin_panel()
            elif role == "teacher":
                # Open the Teacher Panel
                self.open_teacher_panel()
            else:
                messagebox.showerror("Invalid Role", "Invalid role for the user.")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_admin_panel(self):
        self.login_form.destroy()  # Close the login window
        AdminPanel()

    def open_teacher_panel(self):
        self.login_form.destroy()  # Close the login window
        TeachersPanel()

    def run(self):
        self.master.wait_window(self.login_form)

if __name__ == "__main__":
    login_page = LoginPage()
    login_page.run()
