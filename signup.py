# signup.py
import tkinter as tk
from tkinter import ttk, messagebox
from auth import create_user


class SignUpScreen(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master, bg="#eaf0f6")
        self.switch_frame = switch_frame
        self.bind_all("<Return>", lambda event: self.signup())

        # Main container (card style)
        container = tk.Frame(self, bg="#ffffff", bd=3, relief="ridge")
        container.place(relx=0.5, rely=0.5, anchor="center", width=420, height=420)

        # Title
        tk.Label(
            container,
            text="📝 Create Account",
            font=("Segoe UI", 20, "bold"),
            bg="#ffffff",
            fg="#1e3d59"
        ).pack(pady=(25, 20))

        # Username Entry with placeholder
        self.username = ttk.Entry(container, font=("Segoe UI", 12))
        self.username.pack(pady=10, ipady=6, ipadx=6, fill="x", padx=50)
        self._add_placeholder(self.username, "Username")

        # Password Entry with placeholder
        self.password = ttk.Entry(container, font=("Segoe UI", 12))
        self.password.pack(pady=10, ipady=6, ipadx=6, fill="x", padx=50)
        self._add_placeholder(self.password, "Password", is_password=True)

        # Confirm Password Entry with placeholder
        self.confirm_password = ttk.Entry(container, font=("Segoe UI", 12))
        self.confirm_password.pack(pady=10, ipady=6, ipadx=6, fill="x", padx=50)
        self._add_placeholder(self.confirm_password, "Confirm Password", is_password=True)

        # Button Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Sign.TButton",
            font=("Segoe UI", 13, "bold"),
            padding=10,
            background="#27ae60",
            foreground="#ffffff"
        )
        style.map(
            "Sign.TButton",
            background=[("active", "#219150"), ("pressed", "#1e8449")],
            foreground=[("active", "#ffffff")]
        )

        # Sign Up Button
        ttk.Button(container, text="✅ Sign Up", style="Sign.TButton",
                   command=self.signup).pack(pady=15, fill="x", padx=70)

        # Back Button
        ttk.Button(container, text="⬅ Back", style="Sign.TButton",
                   command=lambda: switch_frame("welcome")).pack(pady=5, fill="x", padx=70)

        # Footer Note
        tk.Label(
            container,
            text="Already have an account? Go back to Login.",
            font=("Segoe UI", 9, "italic"),
            bg="#ffffff",
            fg="#7f8c8d"
        ).pack(side="bottom", pady=15)

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

    def signup(self):
        u = self.username.get().strip()
        p = self.password.get().strip()
        cp = self.confirm_password.get().strip()

        # If placeholders are still there, treat them as empty
        if u == "Username":
            u = ""
        if p == "Password":
            p = ""
        if cp == "Confirm Password":
            cp = ""

        # Basic field validation
        if not u or not p or not cp:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Check password match
        if p != cp:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Password strength check
        if len(p) < 6 or not any(char.isdigit() for char in p):
            messagebox.showerror("Error", "Password must be at least 6 characters and contain a number.")
            return

        # Create user
        success, msg = create_user(u, p)
        if success:
            messagebox.showinfo("Success", msg)
            self.switch_frame("login")
        else:
            messagebox.showerror("Error", msg)
