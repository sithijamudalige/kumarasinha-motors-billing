# adminlogin.py
import tkinter as tk
from tkinter import messagebox  # <- Needed to avoid error

class AdminLoginScreen(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame
        self.bind_all("<Return>", lambda event: self.login())
        tk.Label(self, text="Admin Login", font=("Arial", 14)).pack(pady=10)

        self.username = tk.Entry(self)
        self.username.pack(pady=5)
        self.username.insert(0, "Admin Username")

        self.password = tk.Entry(self, show="*")
        self.password.pack(pady=5)
        self.password.insert(0, "Password")

        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: self.switch_frame("welcome")).pack()

    def login(self):
        u = self.username.get()
        p = self.password.get()
        if u == "admin" and p == "admin123":
            messagebox.showinfo("Login Success", "Welcome, Admin!")
            self.switch_frame("admin_dashboard",u)  # <- switch to dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")
