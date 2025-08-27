# login.py
import tkinter as tk
from tkinter import ttk, messagebox
from auth import login_user
import sqlite3

class LoginScreen(tk.Frame):
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
            text="🔐 User Login", 
            font=("Segoe UI", 20, "bold"), 
            bg="#ffffff", 
            fg="#1e3d59"
        ).pack(pady=(25, 20))

        # Username Entry with placeholder
        self.username = ttk.Entry(container, font=("Segoe UI", 12))
        self.username.pack(pady=12, ipady=6, ipadx=6, fill="x", padx=40)
        self._add_placeholder(self.username, "Username")

        # Password Entry with placeholder
        self.password = ttk.Entry(container, font=("Segoe UI", 12))
        self.password.pack(pady=12, ipady=6, ipadx=6, fill="x", padx=40)
        self._add_placeholder(self.password, "Password", is_password=True)

        # Button Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Login.TButton",
            font=("Segoe UI", 13, "bold"),
            padding=10,
            background="#3498db",
            foreground="#ffffff"
        )
        style.map(
            "Login.TButton",
            background=[("active", "#2980b9"), ("pressed", "#2471a3")],
            foreground=[("active", "#ffffff")]
        )

        # Login Button
        ttk.Button(container, text="Login", style="Login.TButton", 
                   command=self.login).pack(pady=15, fill="x", padx=60)

        # Back Button
        ttk.Button(container, text="⬅ Back", style="Login.TButton",
                   command=lambda: switch_frame("welcome")).pack(pady=5, fill="x", padx=60)

        # Footer
        tk.Label(
            container,
            text="Forgot password? Contact admin.",
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
        if u == "Username":
            u = ""
        if p == "Password":
            p = ""

        success, msg = login_user(u, p)
        if success:
            self.record_login(u)
            messagebox.showinfo("Success", msg)
            self.switch_frame("user_dashboard", user=u)
        else:
            messagebox.showerror("Error", msg)

    def record_login(self, username):
        try:
            with sqlite3.connect("inventory.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO login_history (username, login_time) VALUES (?, datetime('now', 'localtime'))",
                    (username,)
                )
                conn.commit()
        except Exception as e:
            print("Failed to record login:", e)
