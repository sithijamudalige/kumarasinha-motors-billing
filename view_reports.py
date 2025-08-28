# view_reports.py
import tkinter as tk
from tkinter import ttk

class ViewReports(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.config(bg='#f0f0f0')  # Set background color
        
        # Main title
        title_label = tk.Label(self, text="Reports Dashboard", font=("Arial", 18, "bold"), bg='#f0f0f0')
        title_label.pack(pady=(20, 30))
        
        # Create a container for the report buttons
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Button styling
        button_style = {
            'font': ('Arial', 12),
            'width': 20,
            'height': 2,
            'bg': '#4CAF50',
            'fg': 'white',
            'relief': tk.FLAT,
            'cursor': 'hand2'
        }
        
        # Button to view parts table
        parts_btn = tk.Button(button_frame, text="Parts Table", 
                             command=lambda: switch_frame("view_parts_table"), **button_style)
        parts_btn.pack(pady=10)
        parts_btn.bind("<Enter>", lambda e: parts_btn.config(bg='#45a049'))
        parts_btn.bind("<Leave>", lambda e: parts_btn.config(bg='#4CAF50'))
        
        # Button to view login history
        login_btn = tk.Button(button_frame, text="Login History", 
                             command=lambda: switch_frame("view_login_history"), **button_style)
        login_btn.pack(pady=10)
        login_btn.config(bg='#2196F3')
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg='#0b7dda'))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg='#2196F3'))
        
        # Button to view sales history
        sales_btn = tk.Button(button_frame, text="Sales History", 
                             command=lambda: switch_frame("view_sales_history"), **button_style)
        sales_btn.pack(pady=10)
        sales_btn.config(bg='#ff9800')
        sales_btn.bind("<Enter>", lambda e: sales_btn.config(bg='#e68a00'))
        sales_btn.bind("<Leave>", lambda e: sales_btn.config(bg='#ff9800'))
        
        # Back button
        back_btn = tk.Button(self, text="Back to Dashboard", 
                            command=lambda: switch_frame("admin_dashboard"),
                            font=('Arial', 10), width=15, height=1,
                            bg='#f44336', fg='white', relief=tk.FLAT)
        back_btn.pack(pady=20)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg='#d32f2f'))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg='#f44336'))