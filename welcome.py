# welcome.py
import tkinter as tk

class WelcomeScreen(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        tk.Label(self, text="Welcome to POS System", font=("Arial", 16)).pack(pady=30)
        tk.Button(self, text="Login", width=20, command=lambda: switch_frame("login")).pack(pady=10)
        tk.Button(self, text="Sign Up", width=20, command=lambda: switch_frame("signup")).pack(pady=10)
        tk.Button(self, text="Admin Login", width=20, command=lambda: switch_frame("adminlogin")).pack(pady=10)