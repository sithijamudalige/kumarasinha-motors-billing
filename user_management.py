# user_management.py
import tkinter as tk
from tkinter import messagebox
import sqlite3

DB = "inventory.db"

class UserManagement(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame
        tk.Label(self, text="User Management", font=("Arial", 16)).pack(pady=10)

        self.user_frame = tk.Frame(self)
        self.user_frame.pack(pady=10)

        self.display_users()

        # Add User Form
        tk.Label(self, text="Add New User", font=("Arial", 12)).pack(pady=5)

        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)
        self.username_entry.insert(0, "Username")

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)
        self.password_entry.insert(0, "Password")

        tk.Button(self, text="Add User", command=self.add_user).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: switch_frame("admin_dashboard")).pack()

    def display_users(self):
        # Clear old widgets
        for widget in self.user_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM users")
        users = cursor.fetchall()
        conn.close()

        # Table Header
        header = tk.Frame(self.user_frame)
        header.pack(fill="x")
        tk.Label(header, text="ID", width=5).pack(side="left")
        tk.Label(header, text="Username", width=20).pack(side="left")
        tk.Label(header, text="Actions", width=20).pack(side="left")

        for user in users:
            row = tk.Frame(self.user_frame)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=user[0], width=5).pack(side="left")
            tk.Label(row, text=user[1], width=20).pack(side="left")

            tk.Button(row, text="Edit", command=lambda u=user: self.edit_user(u)).pack(side="left", padx=5)
            tk.Button(row, text="Delete", command=lambda u=user: self.delete_user(u[0])).pack(side="left")

    def add_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Missing Fields", "Please fill in both fields.")
            return

        try:
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "User added successfully.")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.display_users()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")

    def delete_user(self, user_id):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this user?")
        if confirm:
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            self.display_users()

    def edit_user(self, user):
        edit_win = tk.Toplevel(self)
        edit_win.title("Edit User")

        tk.Label(edit_win, text="Username").pack()
        username_entry = tk.Entry(edit_win)
        username_entry.pack()
        username_entry.insert(0, user[1])

        tk.Label(edit_win, text="Password").pack()
        password_entry = tk.Entry(edit_win, show="*")
        password_entry.pack()

        def save_changes():
            new_username = username_entry.get()
            new_password = password_entry.get()
            if new_username:
                conn = sqlite3.connect(DB)
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET username = ?, password = ? WHERE id = ?",
                               (new_username, new_password, user[0]))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "User updated successfully.")
                edit_win.destroy()
                self.display_users()
            else:
                messagebox.showerror("Error", "Username cannot be empty.")

        tk.Button(edit_win, text="Save", command=save_changes).pack(pady=10)
