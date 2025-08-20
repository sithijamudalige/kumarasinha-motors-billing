# user_dashboard.py
import tkinter as tk

class UserDashboard(tk.Frame):
    def __init__(self, master, switch_frame, user):
        super().__init__(master)
        tk.Label(self, text=f"Welcome, {user}", font=("Arial", 16)).pack(pady=20)

        tk.Button(self, text="Logout", command=lambda: switch_frame("welcome")).pack(pady=10)
        tk.Button(self,text="Admin Login", command=lambda:switch_frame("adminlogin")).pack(pady=10)
        tk.Button(self,text="Billing System",command=lambda:switch_frame("billing_system")).pack(padx=10)
        tk.Button(self, text="Inventory Creation", command=lambda: switch_frame("inventory_creation")).pack(padx=10)
