# view_reports.py
import tkinter as tk
from tkinter import ttk

class ViewReports(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        tk.Label(self, text="Reports", font=("Arial", 16)).pack(pady=20)

        # Button to view parts table
        tk.Button(self,text="Parts Table",command=lambda:switch_frame("view_parts_table")).pack(padx=10)
        # Button to view login history
        tk.Button(self, text="Login History",command=lambda:switch_frame("view_login_history")).pack(padx=10) 
        # Button to view sales history
        tk.Button(self, text="Sales History",command=lambda:switch_frame("view_sales_history")).pack(padx=10)  

        # Back button
        tk.Button(self, text="Back", width=20, command=lambda: switch_frame("admin_dashboard")).pack(pady=20)

    