# welcome.py
import tkinter as tk
from tkinter import ttk

class WelcomeScreen(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master, bg="#f8fafc")

        # Responsive root grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main container with gradient-like effect
        self.container = tk.Frame(self, bg="#ffffff", bd=0, relief="flat")
        self.container.grid(row=0, column=0, sticky="nsew", padx=60, pady=40)
        
        # Add shadow effect frame
        shadow_frame = tk.Frame(self, bg="#e2e8f0", bd=0)
        shadow_frame.grid(row=0, column=0, sticky="nsew", padx=65, pady=45)
        
        # Ensure container is on top
        self.container.lift()

        # Build UI
        self.build_ui(switch_frame)

    def build_ui(self, switch_frame):
        # Clear previous widgets
        for widget in self.container.winfo_children():
            widget.destroy()

        # Header section with gradient background simulation
        header_frame = tk.Frame(self.container, bg="#ffffff", height=120)
        header_frame.pack(fill="x", pady=(30, 20))
        header_frame.pack_propagate(False)

        # Main title with better styling
        title_label = tk.Label(
            header_frame,
            text="🏪 Welcome to POS System",
            font=("Segoe UI", 28, "bold"),
            bg="#ffffff",
            fg="#1a202c"
        )
        title_label.pack(pady=(20, 5))

        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Streamline Your Business Operations",
            font=("Segoe UI", 14),
            bg="#ffffff",
            fg="#718096"
        )
        subtitle_label.pack()

        # Custom styles for modern buttons
        style = ttk.Style()
        style.theme_use("clam")
        
        # Primary button style
        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 14, "bold"),
            padding=(25, 20),
            relief="flat",
            background="#4299e1",
            foreground="#ffffff",
            borderwidth=0,
            focuscolor="none"
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#3182ce"), ("pressed", "#2c5282")],
            foreground=[("active", "#ffffff"), ("pressed", "#ffffff")],
            relief=[("pressed", "flat"), ("!pressed", "flat")]
        )

        # Secondary button style  
        style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 14, "bold"),
            padding=(25, 20),
            relief="flat",
            background="#48bb78",
            foreground="#ffffff",
            borderwidth=0,
            focuscolor="none"
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#38a169"), ("pressed", "#2f855a")],
            foreground=[("active", "#ffffff"), ("pressed", "#ffffff")],
            relief=[("pressed", "flat"), ("!pressed", "flat")]
        )

        # Admin button style
        style.configure(
            "Admin.TButton",
            font=("Segoe UI", 14, "bold"),
            padding=(25, 20),
            relief="flat",
            background="#ed8936",
            foreground="#ffffff",
            borderwidth=0,
            focuscolor="none"
        )
        style.map(
            "Admin.TButton",
            background=[("active", "#dd6b20"), ("pressed", "#c05621")],
            foreground=[("active", "#ffffff"), ("pressed", "#ffffff")],
            relief=[("pressed", "flat"), ("!pressed", "flat")]
        )

        # Main content frame
        content_frame = tk.Frame(self.container, bg="#ffffff")
        content_frame.pack(expand=True, fill="both", padx=40, pady=30)

        # Button container with better spacing
        btn_container = tk.Frame(content_frame, bg="#ffffff")
        btn_container.pack(expand=True)

        # Grid configuration for responsive buttons
        for col in range(3):
            btn_container.grid_columnconfigure(col, weight=1, uniform="button_col")
        btn_container.grid_rowconfigure(0, weight=1)

        # Create card-style button frames
        login_card = tk.Frame(btn_container, bg="#f7fafc", bd=1, relief="solid", padx=20, pady=30)
        login_card.grid(row=0, column=0, padx=15, pady=10, sticky="nsew")
        
        signup_card = tk.Frame(btn_container, bg="#f7fafc", bd=1, relief="solid", padx=20, pady=30)
        signup_card.grid(row=0, column=1, padx=15, pady=10, sticky="nsew")
        
        admin_card = tk.Frame(btn_container, bg="#f7fafc", bd=1, relief="solid", padx=20, pady=30)
        admin_card.grid(row=0, column=2, padx=15, pady=10, sticky="nsew")

        # Login section
        tk.Label(
            login_card,
            text="🔐",
            font=("Segoe UI", 32),
            bg="#f7fafc",
            fg="#4299e1"
        ).pack(pady=(10, 15))
        
        tk.Label(
            login_card,
            text="User Login",
            font=("Segoe UI", 16, "bold"),
            bg="#f7fafc",
            fg="#2d3748"
        ).pack(pady=(0, 5))
        
        tk.Label(
            login_card,
            text="Access your account\nand start selling",
            font=("Segoe UI", 11),
            bg="#f7fafc",
            fg="#718096",
            justify="center"
        ).pack(pady=(0, 20))
        
        login_btn = ttk.Button(
            login_card,
            text="LOGIN",
            style="Primary.TButton",
            command=lambda: switch_frame("login")
        )
        login_btn.pack(pady=10)

        # Sign up section
        tk.Label(
            signup_card,
            text="📋",
            font=("Segoe UI", 32),
            bg="#f7fafc",
            fg="#48bb78"
        ).pack(pady=(10, 15))
        
        tk.Label(
            signup_card,
            text="New User",
            font=("Segoe UI", 16, "bold"),
            bg="#f7fafc",
            fg="#2d3748"
        ).pack(pady=(0, 5))
        
        tk.Label(
            signup_card,
            text="Create your account\nand get started",
            font=("Segoe UI", 11),
            bg="#f7fafc",
            fg="#718096",
            justify="center"
        ).pack(pady=(0, 20))
        
        signup_btn = ttk.Button(
            signup_card,
            text="SIGN UP",
            style="Secondary.TButton",
            command=lambda: switch_frame("signup")
        )
        signup_btn.pack(pady=10)

        # Admin section
        tk.Label(
            admin_card,
            text="⚡",
            font=("Segoe UI", 32),
            bg="#f7fafc",
            fg="#ed8936"
        ).pack(pady=(10, 15))
        
        tk.Label(
            admin_card,
            text="Admin Panel",
            font=("Segoe UI", 16, "bold"),
            bg="#f7fafc",
            fg="#2d3748"
        ).pack(pady=(0, 5))
        
        tk.Label(
            admin_card,
            text="Manage system\nsettings & users",
            font=("Segoe UI", 11),
            bg="#f7fafc",
            fg="#718096",
            justify="center"
        ).pack(pady=(0, 20))
        
        admin_btn = ttk.Button(
            admin_card,
            text="ADMIN",
            style="Admin.TButton",
            command=lambda: switch_frame("adminlogin")
        )
        admin_btn.pack(pady=10)

        # Footer with additional info
        footer_frame = tk.Frame(self.container, bg="#ffffff", height=80)
        footer_frame.pack(side="bottom", fill="x", pady=(30, 20))
        footer_frame.pack_propagate(False)

        # Version info
        tk.Label(
            footer_frame,
            text="Version 2.0.1",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg="#a0aec0"
        ).pack(side="right", padx=(0, 20), pady=10)

        # Copyright
        tk.Label(
            footer_frame,
            text="© 2025 Modern POS System | Powered by Advanced Retail Solutions",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#718096"
        ).pack(side="left", padx=20, pady=10)

        # Add separator line
        separator = tk.Frame(footer_frame, bg="#e2e8f0", height=1)
        separator.pack(fill="x", padx=20, pady=(0, 10))