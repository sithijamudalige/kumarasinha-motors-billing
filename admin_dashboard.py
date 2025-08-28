# admin_dashboard.py
import tkinter as tk
from tkinter import ttk, Frame, Label, Button

class AdminDashboard(tk.Frame):
    def __init__(self, master, switch_frame, user):
        super().__init__(master)
        self.configure(bg='#f5f7fa')
        self.switch_frame = switch_frame
        self.user = user
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.create_widgets()
        
    def configure_styles(self):
        # Color scheme
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.accent_color = "#e74c3c"
        self.success_color = "#2ecc71"
        self.light_bg = "#ecf0f1"
        self.card_bg = "#ffffff"
        
        # Configure styles
        self.style.configure("Header.TLabel", 
                            background=self.primary_color, 
                            foreground="white", 
                            font=("Arial", 18, "bold"),
                            padding=15)
        
        self.style.configure("Card.TFrame", 
                            background=self.card_bg,
                            relief="raised",
                            borderwidth=1)
        
        self.style.configure("Primary.TButton", 
                            background=self.secondary_color,
                            foreground="white",
                            font=("Arial", 12, "bold"),
                            padding=10,
                            focuscolor=self.secondary_color)
        
        self.style.configure("Secondary.TButton", 
                            background=self.primary_color,
                            foreground="white",
                            font=("Arial", 11),
                            padding=8,
                            focuscolor=self.primary_color)
        
        self.style.configure("Accent.TButton", 
                            background=self.accent_color,
                            foreground="white",
                            font=("Arial", 11),
                            padding=8,
                            focuscolor=self.accent_color)
        
        self.style.map("Primary.TButton", 
                      background=[('active', '#2980b9')])
        self.style.map("Secondary.TButton", 
                      background=[('active', '#34495e')])
        self.style.map("Accent.TButton", 
                      background=[('active', '#c0392b')])

    def create_widgets(self):
        # Header
        header_frame = Frame(self, bg=self.primary_color)
        header_frame.pack(fill="x", pady=(0, 20))
        
        Label(header_frame, text="Admin Dashboard", 
              bg=self.primary_color, fg="white", 
              font=("Arial", 18, "bold")).pack(pady=15)
        
        # Welcome message
        welcome_frame = Frame(self, bg=self.light_bg, padx=20, pady=10)
        welcome_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        welcome_text = f"Welcome, {self.user}!" if self.user else "Welcome, Administrator!"
        Label(welcome_frame, text=welcome_text, 
              bg=self.light_bg, fg=self.primary_color,
              font=("Arial", 12)).pack(side="left")
        
        # Logout button
        ttk.Button(welcome_frame, text="Logout", 
                  style="Accent.TButton",
                  command=lambda: self.switch_frame("welcome")).pack(side="right")
        
        # Main content area
        content_frame = Frame(self, bg='#f5f7fa')
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Dashboard cards
        cards_frame = Frame(content_frame, bg='#f5f7fa')
        cards_frame.pack(fill="both", expand=True)
        
        # Card 1: User Management
        user_card = Frame(cards_frame, bg=self.card_bg, relief="raised", bd=1)
        user_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        user_card.configure(highlightbackground="#ddd", highlightthickness=1)
        
        Label(user_card, text="👥 User Management", 
              bg=self.card_bg, fg=self.primary_color,
              font=("Arial", 14, "bold")).pack(pady=(20, 10))
        
        Label(user_card, text="Manage system users, roles and permissions", 
              bg=self.card_bg, fg="#7f8c8d",
              font=("Arial", 10), wraplength=200).pack(pady=(0, 20), padx=15)
        
        ttk.Button(user_card, text="Manage Users", 
                  style="Secondary.TButton",
                  command=lambda: self.switch_frame("user_management")).pack(pady=(0, 20))
        
        # Card 2: Parts Management
        parts_card = Frame(cards_frame, bg=self.card_bg, relief="raised", bd=1)
        parts_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        parts_card.configure(highlightbackground="#ddd", highlightthickness=1)
        
        Label(parts_card, text="🔧 Parts Management", 
              bg=self.card_bg, fg=self.primary_color,
              font=("Arial", 14, "bold")).pack(pady=(20, 10))
        
        Label(parts_card, text="Manage inventory, parts and stock levels", 
              bg=self.card_bg, fg="#7f8c8d",
              font=("Arial", 10), wraplength=200).pack(pady=(0, 20), padx=15)
        
        ttk.Button(parts_card, text="Manage Parts", 
                  style="Secondary.TButton",
                  command=lambda: self.switch_frame("Parts_management")).pack(pady=(0, 20))
        
        # Card 3: Reports
        reports_card = Frame(cards_frame, bg=self.card_bg, relief="raised", bd=1)
        reports_card.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        reports_card.configure(highlightbackground="#ddd", highlightthickness=1)
        
        Label(reports_card, text="📊 View & Reports", 
              bg=self.card_bg, fg=self.primary_color,
              font=("Arial", 14, "bold")).pack(pady=(20, 10))
        
        Label(reports_card, text="Generate reports and view system analytics", 
              bg=self.card_bg, fg="#7f8c8d",
              font=("Arial", 10), wraplength=200).pack(pady=(0, 20), padx=15)
        
        ttk.Button(reports_card, text="View Reports", 
                  style="Secondary.TButton",
                  command=lambda: self.switch_frame("view_reports")).pack(pady=(0, 20))
        
        # Configure grid weights for responsive layout
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.columnconfigure(2, weight=1)
        cards_frame.rowconfigure(0, weight=1)
        
        # Quick stats or additional info can be added here
        stats_frame = Frame(content_frame, bg=self.light_bg, padx=15, pady=10)
        stats_frame.pack(fill="x", pady=(20, 0))
        
        Label(stats_frame, text="System Status: All systems operational", 
              bg=self.light_bg, fg=self.success_color,
              font=("Arial", 10, "italic")).pack(side="left")
        
        # Footer
        footer_frame = Frame(self, bg=self.primary_color, height=30)
        footer_frame.pack(fill="x", side="bottom")
        Label(footer_frame, text="© 2023 Inventory Management System - Admin Panel", 
              bg=self.primary_color, fg="white",
              font=("Arial", 9)).pack(pady=5)