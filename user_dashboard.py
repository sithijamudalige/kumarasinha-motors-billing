import tkinter as tk
from tkinter import ttk

class UserDashboard(tk.Frame):
    def __init__(self, master, switch_frame, user):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.switch_frame = switch_frame
        self.user = user
        
        self.setup_ui()
    
    def setup_ui(self):
        # Configure grid weights for responsive layout
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Main content
        self.grid_rowconfigure(2, weight=0)  # Footer
        self.grid_columnconfigure(0, weight=1)
        
        # Header Frame
        header_frame = tk.Frame(self, bg="#2c3e50", height=80)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)
        
        # Welcome Label
        welcome_label = tk.Label(
            header_frame, 
            text=f"Welcome, {self.user}",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        welcome_label.grid(row=0, column=0, pady=20, padx=(20, 0), sticky="w")
        
        # Logout Button in Navbar (Rounded corners)
        logout_nav_button = tk.Button(
            header_frame,
            text="🚪 Logout",
            command=lambda: self.switch_frame("welcome"),
            font=("Arial", 10, "bold"),
            width=10,
            height=1,
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            bd=2,
            highlightthickness=2,
            highlightcolor="#c0392b"
        )
        logout_nav_button.grid(row=0, column=1, pady=20, padx=(0, 20), sticky="e")
        
        # Main Content Frame
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=40)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Dashboard Title
        dashboard_title = tk.Label(
            main_frame,
            text="Dashboard",
            font=("Arial", 16, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        dashboard_title.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Button styling configuration - Box style (rectangular)
        box_button_style = {
            "font": ("Arial", 12, "bold"),
            "width": 20,
            "height": 3,
            "relief": "raised",
            "cursor": "hand2",
            "bd": 3,
            "highlightthickness": 0
        }
        
        # Primary Action Buttons (Box style - rectangular)
        billing_button = tk.Button(
            main_frame,
            text="💰 Billing System",
            command=lambda: self.switch_frame("billing_system"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            **box_button_style
        )
        billing_button.grid(row=1, column=0, padx=15, pady=15, sticky="ew")
        
        inventory_button = tk.Button(
            main_frame,
            text="📦 Inventory Creation",
            command=lambda: self.switch_frame("inventory_creation"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            **box_button_style
        )
        inventory_button.grid(row=1, column=1, padx=15, pady=15, sticky="ew")
        
        # Secondary Action Button (Box style - rectangular)
        admin_button = tk.Button(
            main_frame,
            text="🔐 Admin Login",
            command=lambda: self.switch_frame("adminlogin"),
            bg="#f39c12",
            fg="white",
            activebackground="#e67e22",
            activeforeground="white",
            **box_button_style
        )
        admin_button.grid(row=2, column=0, columnspan=2, padx=15, pady=15, sticky="ew")
        
        # Add hover effects to main buttons and navbar logout button
        self.add_button_hover_effects([billing_button, inventory_button, admin_button])
        self.add_navbar_button_hover_effect(logout_nav_button)
        
        # Footer Frame
        footer_frame = tk.Frame(self, bg="#ecf0f1", height=40)
        footer_frame.grid(row=2, column=0, sticky="ew")
        footer_frame.grid_propagate(False)
        footer_frame.grid_columnconfigure(0, weight=1)
        
        # Status or info label
        status_label = tk.Label(
            footer_frame,
            text="User Dashboard - Ready",
            font=("Arial", 9),
            fg="#7f8c8d",
            bg="#ecf0f1"
        )
        status_label.grid(row=0, column=0, pady=10)
    
    def add_button_hover_effects(self, buttons):
        """Add hover effects to main dashboard buttons (box style)"""
        def on_enter(event, button, hover_color):
            button.config(bg=hover_color, relief="sunken")
        
        def on_leave(event, button, normal_color):
            button.config(bg=normal_color, relief="raised")
        
        # Define hover colors for each button type
        hover_colors = {
            "💰 Billing System": ("#2980b9", "#3498db"),
            "📦 Inventory Creation": ("#229954", "#27ae60"),
            "🔐 Admin Login": ("#e67e22", "#f39c12")
        }
        
        for button in buttons:
            button_text = button.cget("text")
            if button_text in hover_colors:
                hover_color, normal_color = hover_colors[button_text]
                button.bind("<Enter>", lambda e, b=button, hc=hover_color: on_enter(e, b, hc))
                button.bind("<Leave>", lambda e, b=button, nc=normal_color: on_leave(e, b, nc))
    
    def add_navbar_button_hover_effect(self, button):
        """Add hover effect to navbar logout button (rounded style)"""
        def on_enter(event):
            button.config(bg="#c0392b", highlightbackground="#a93226")
        
        def on_leave(event):
            button.config(bg="#e74c3c", highlightbackground="#c0392b")
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)