# admin_dashboard.py
import tkinter as tk

class AdminDashboard(tk.Frame):
    def __init__(self, master, switch_frame,user):
        super().__init__(master)
        
        tk.Label(self, text="Admin Dashboard", font=("Arial", 16)).pack(pady=20)

        tk.Button(self, text="Logout", command=lambda: switch_frame("welcome")).pack(pady=10)


        tk.Button(self,text="User Management",command=lambda:switch_frame("user_management")).pack(padx=10)
        tk.Button(self,text="Parts Management",command=lambda:switch_frame("Parts_management")).pack(padx=10)
        tk.Button(self, text="View & Reports", command=lambda: switch_frame("view_reports")).pack(padx=10)
        
