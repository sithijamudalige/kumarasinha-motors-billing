# login.py
import tkinter as tk
from tkinter import messagebox
from auth import login_user
import sqlite3

class LoginScreen(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame
        self.bind_all("<Return>", lambda event: self.login())
        tk.Label(self, text="Login", font=("Arial", 14)).pack(pady=10)

        self.username = tk.Entry(self)
        self.username.pack(pady=5)
        self.username.insert(0, "Username")

        self.password = tk.Entry(self, show="*")
        self.password.pack(pady=5)
        self.password.insert(0, "Password")

        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: switch_frame("welcome")).pack()

    def login(self):
        u = self.username.get()
        p = self.password.get()
        success, msg = login_user(u, p)
        if success:
            self.record_login(u)  # ✅ Record the login
            messagebox.showinfo("Success", msg)
            self.switch_frame("user_dashboard", user=u)  # ✅ Pass username
        else:
            messagebox.showerror("Error", msg)

    def record_login(self, username):
        try:
            with sqlite3.connect("inventory.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO login_history (username, login_time) VALUES (?, datetime('now', 'localtime'))", (username,))
                conn.commit()
        except Exception as e:
            print("Failed to record login:", e)
