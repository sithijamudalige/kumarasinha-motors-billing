# adminlogin.py
import tkinter as tk
from tkinter import ttk, messagebox


class AdminLoginScreen(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master, bg="#eaf0f6")
        self.switch_frame = switch_frame
        self.bind_all("<Return>", lambda event: self.login())

        # Main container (card style)
        container = tk.Frame(self, bg="#ffffff", bd=3, relief="ridge")
        container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=350)

        # Title
        tk.Label(
            container,
            text="👑 Admin Login",
            font=("Segoe UI", 20, "bold"),
            bg="#ffffff",
            fg="#1e3d59"
        ).pack(pady=(25, 20))

        # Username Entry with placeholder
        self.username = ttk.Entry(container, font=("Segoe UI", 12))
        self.username.pack(pady=12, ipady=6, ipadx=6, fill="x", padx=40)
        self._add_placeholder(self.username, "Admin Username")

        # Password Entry with placeholder
        self.password = ttk.Entry(container, font=("Segoe UI", 12))
        self.password.pack(pady=12, ipady=6, ipadx=6, fill="x", padx=40)
        self._add_placeholder(self.password, "Password", is_password=True)

        # Button Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Admin.TButton",
            font=("Segoe UI", 13, "bold"),
            padding=10,
            background="#e67e22",
            foreground="#ffffff"
        )
        style.map(
            "Admin.TButton",
            background=[("active", "#ca6f1e"), ("pressed", "#af601a")],
            foreground=[("active", "#ffffff")]
        )

        # Login Button
        ttk.Button(container, text="Login", style="Admin.TButton",
                   command=self.login).pack(pady=15, fill="x", padx=60)

        # Back Button
        ttk.Button(container, text="⬅ Back", style="Admin.TButton",
                   command=lambda: self.switch_frame("welcome")).pack(pady=5, fill="x", padx=60)

        # Footer
        tk.Label(
            container,
            text="Admin access only.",
            font=("Segoe UI", 9, "italic"),
            bg="#ffffff",
            fg="#7f8c8d"
        ).pack(side="bottom", pady=10)

    def _add_placeholder(self, entry, placeholder, is_password=False):
        """Adds placeholder text to an Entry widget."""
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(foreground="black")
                if is_password:
                    entry.config(show="*")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(foreground="grey")
                if is_password:
                    entry.config(show="")

        entry.insert(0, placeholder)
        entry.config(foreground="grey")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def login(self):
        u = self.username.get().strip()
        p = self.password.get().strip()

        # If placeholders are still there, treat them as empty
        if u == "Admin Username":
            u = ""
        if p == "Password":
            p = ""

        if u == "admin" and p == "admin123":
            messagebox.showinfo("Login Success", "Welcome, Admin!")
            self.switch_frame("admin_dashboard", u)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")
