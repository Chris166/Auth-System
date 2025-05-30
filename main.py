import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import bcrypt
import secrets
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import time
import sys
from pathlib import Path

class AuthSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Authentication System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f2f5")
        
        # Configure styles
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f0f2f5")
        style.configure("Custom.TButton",
                       padding=10,
                       font=("Helvetica", 12),
                       background="#1a73e8",
                       foreground="white")
        style.configure("Custom.TLabel",
                       font=("Helvetica", 12),
                       background="#f0f2f5")
        style.configure("Custom.TEntry",
                       padding=10,
                       font=("Helvetica", 12))

        self.current_user = None
        self.setup_main_menu()

    def setup_main_menu(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create main container
        container = ttk.Frame(self.root, style="Custom.TFrame")
        container.pack(expand=True, fill="both", padx=50, pady=50)

        # Title
        title = ttk.Label(
            container,
            text="Welcome to Advanced Auth System",
            font=("Helvetica", 24, "bold"),
            style="Custom.TLabel"
        )
        title.pack(pady=20)

        # Buttons container
        buttons_frame = ttk.Frame(container, style="Custom.TFrame")
        buttons_frame.pack(pady=20)

        # Menu buttons
        ttk.Button(
            buttons_frame,
            text="Login",
            command=self.show_login,
            style="Custom.TButton"
        ).pack(pady=10, ipadx=20)

        ttk.Button(
            buttons_frame,
            text="Register",
            command=self.show_register,
            style="Custom.TButton"
        ).pack(pady=10, ipadx=20)

        ttk.Button(
            buttons_frame,
            text="Exit",
            command=self.exit_application,
            style="Custom.TButton"
        ).pack(pady=10, ipadx=20)

    def show_login(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        container = ttk.Frame(self.root, style="Custom.TFrame")
        container.pack(expand=True, fill="both", padx=50, pady=50)

        ttk.Label(
            container,
            text="Login",
            font=("Helvetica", 24, "bold"),
            style="Custom.TLabel"
        ).pack(pady=20)

        # Login form
        form_frame = ttk.Frame(container, style="Custom.TFrame")
        form_frame.pack(pady=20)

        ttk.Label(
            form_frame,
            text="Username:",
            style="Custom.TLabel"
        ).pack()
        username_entry = ttk.Entry(form_frame, style="Custom.TEntry")
        username_entry.pack(pady=5)

        ttk.Label(
            form_frame,
            text="Password:",
            style="Custom.TLabel"
        ).pack()
        password_entry = ttk.Entry(form_frame, show="*", style="Custom.TEntry")
        password_entry.pack(pady=5)

        ttk.Button(
            form_frame,
            text="Login",
            command=lambda: self.process_login(username_entry.get(), password_entry.get()),
            style="Custom.TButton"
        ).pack(pady=20)

        ttk.Button(
            form_frame,
            text="Back to Menu",
            command=self.setup_main_menu,
            style="Custom.TButton"
        ).pack()

    def show_register(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        container = ttk.Frame(self.root, style="Custom.TFrame")
        container.pack(expand=True, fill="both", padx=50, pady=50)

        ttk.Label(
            container,
            text="Register New Account",
            font=("Helvetica", 24, "bold"),
            style="Custom.TLabel"
        ).pack(pady=20)

        # Registration form
        form_frame = ttk.Frame(container, style="Custom.TFrame")
        form_frame.pack(pady=20)

        fields = {}
        for field in ["Username", "First Name", "Surname", "Email", "Password", "Confirm Password"]:
            ttk.Label(
                form_frame,
                text=f"{field}:",
                style="Custom.TLabel"
            ).pack()
            
            entry = ttk.Entry(
                form_frame,
                style="Custom.TEntry",
                show="*" if "Password" in field else ""
            )
            entry.pack(pady=5)
            fields[field.lower().replace(" ", "_")] = entry

        ttk.Button(
            form_frame,
            text="Register",
            command=lambda: self.process_registration(fields),
            style="Custom.TButton"
        ).pack(pady=20)

        ttk.Button(
            form_frame,
            text="Back to Menu",
            command=self.setup_main_menu,
            style="Custom.TButton"
        ).pack()

    def process_login(self, username, password):
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        with sqlite3.connect("main.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT userID, password_hash, firstname FROM info WHERE username = ?", [username])
            result = cursor.fetchone()

            if result and bcrypt.checkpw(password.encode('utf-8'), result[1]):
                self.current_user = {
                    'id': result[0],
                    'name': result[2],
                    'username': username
                }
                
                # Update last login
                cursor.execute(
                    "UPDATE info SET last_login = CURRENT_TIMESTAMP WHERE userID = ?",
                    [result[0]]
                )
                
                # Create session
                token = secrets.token_hex(32)
                expires_at = datetime.now() + timedelta(days=1)
                cursor.execute(
                    "INSERT INTO sessions (user_id, token, expires_at) VALUES (?, ?, ?)",
                    [result[0], token, expires_at]
                )
                
                db.commit()
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Invalid username or password")

    def process_registration(self, fields):
        # Validate fields
        for field_name, entry in fields.items():
            if not entry.get():
                messagebox.showerror("Error", f"Please fill in {field_name.replace('_', ' ')}")
                return

        if fields['password'].get() != fields['confirm_password'].get():
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            with sqlite3.connect("main.db") as db:
                cursor = db.cursor()
                
                # Check if username exists
                cursor.execute("SELECT username FROM info WHERE username = ?", [fields['username'].get()])
                if cursor.fetchone():
                    messagebox.showerror("Error", "Username already exists")
                    return

                # Hash password
                password_hash = bcrypt.hashpw(
                    fields['password'].get().encode('utf-8'),
                    bcrypt.gensalt()
                )

                # Insert new user
                cursor.execute('''
                INSERT INTO info (username, firstname, surname, password_hash, email)
                VALUES (?, ?, ?, ?, ?)
                ''', [
                    fields['username'].get(),
                    fields['first_name'].get(),
                    fields['surname'].get(),
                    password_hash,
                    fields['email'].get()
                ])
                
                db.commit()
                messagebox.showinfo("Success", "Registration successful! Please login.")
                self.show_login()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")

    def show_dashboard(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        container = ttk.Frame(self.root, style="Custom.TFrame")
        container.pack(expand=True, fill="both", padx=50, pady=50)

        ttk.Label(
            container,
            text=f"Welcome, {self.current_user['name']}!",
            font=("Helvetica", 24, "bold"),
            style="Custom.TLabel"
        ).pack(pady=20)

        # Dashboard options
        options_frame = ttk.Frame(container, style="Custom.TFrame")
        options_frame.pack(pady=20)

        ttk.Button(
            options_frame,
            text="Update Profile",
            command=self.show_profile_update,
            style="Custom.TButton"
        ).pack(pady=10)

        ttk.Button(
            options_frame,
            text="Change Password",
            command=self.show_password_change,
            style="Custom.TButton"
        ).pack(pady=10)

        ttk.Button(
            options_frame,
            text="View Login History",
            command=self.show_login_history,
            style="Custom.TButton"
        ).pack(pady=10)

        ttk.Button(
            options_frame,
            text="Logout",
            command=self.logout,
            style="Custom.TButton"
        ).pack(pady=10)

    def show_profile_update(self):
        # Implementation for profile update form
        pass

    def show_password_change(self):
        # Implementation for password change form
        pass

    def show_login_history(self):
        # Implementation for login history view
        pass

    def logout(self):
        if self.current_user:
            with sqlite3.connect("main.db") as db:
                cursor = db.cursor()
                cursor.execute(
                    "DELETE FROM sessions WHERE user_id = ?",
                    [self.current_user['id']]
                )
                db.commit()

        self.current_user = None
        self.setup_main_menu()

    def exit_application(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.quit()
            sys.exit()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AuthSystem()
    app.run()