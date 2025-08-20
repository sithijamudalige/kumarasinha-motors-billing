# signup.py
import tkinter as tk
from tkinter import messagebox
from auth import create_user

class SignUpScreen(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        tk.Label(self, text="Sign Up", font=("Arial", 14)).pack(pady=10)
        self.bind_all("<Return>", lambda event: self.signup())

        self.username = tk.Entry(self)
        self.username.pack(pady=5)
        self.username.insert(0, "Username")

        self.password = tk.Entry(self, show="*")
        self.password.pack(pady=5)
        self.password.insert(0, "Password")

        self.confirm_password = tk.Entry(self, show="*")
        self.confirm_password.pack(pady=5)
        self.confirm_password.insert(0, "Confirm Password")

        tk.Button(self, text="Sign Up", command=self.signup).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: switch_frame("welcome")).pack()

        self.switch_frame = switch_frame

    def signup(self):
        u = self.username.get().strip()
        p = self.password.get().strip()
        cp = self.confirm_password.get().strip()

        # Basic field validation
        if not u or not p or not cp:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Check password match
        if p != cp:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Password strength check
        if len(p) < 6 or not any(char.isdigit() for char in p):
            messagebox.showerror("Error", "Password must be at least 6 characters and contain a number.")
            return

        # Create user
        success, msg = create_user(u, p)
        if success:
            messagebox.showinfo("Success", msg)
            self.switch_frame("login")  # Redirect to login if needed
        else:
            messagebox.showerror("Error", msg)
