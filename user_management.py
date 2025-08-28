# user_management.py
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB = "inventory.db"

class UserManagement(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.configure(bg='#f5f7fa')
        self.create_widgets()
        self.display_users()

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
                            font=("Arial", 11, "bold"),
                            padding=10,
                            focuscolor=self.secondary_color)
        
        self.style.configure("Secondary.TButton", 
                            background=self.primary_color,
                            foreground="white",
                            font=("Arial", 10),
                            padding=8,
                            focuscolor=self.primary_color)
        
        self.style.configure("Accent.TButton", 
                            background=self.accent_color,
                            foreground="white",
                            font=("Arial", 10),
                            padding=8,
                            focuscolor=self.accent_color)
        
        self.style.configure("Success.TButton", 
                            background=self.success_color,
                            foreground="white",
                            font=("Arial", 11, "bold"),
                            padding=10,
                            focuscolor=self.success_color)
        
        self.style.map("Primary.TButton", 
                      background=[('active', '#2980b9')])
        self.style.map("Secondary.TButton", 
                      background=[('active', '#34495e')])
        self.style.map("Accent.TButton", 
                      background=[('active', '#c0392b')])
        self.style.map("Success.TButton", 
                      background=[('active', '#27ae60')])

    def create_widgets(self):
        # Main container with padding
        main_container = tk.Frame(self, bg=self.light_bg)
        main_container.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header
        header_frame = tk.Frame(main_container, bg=self.primary_color, height=80)
        header_frame.pack(fill="x", pady=(0, 25))
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="👥 User Management System", 
                               bg=self.primary_color, fg="white", 
                               font=("Arial", 20, "bold"))
        header_label.pack(expand=True)
        
        # Content area with left-right split
        content_frame = tk.Frame(main_container, bg=self.light_bg)
        content_frame.pack(fill="both", expand=True)
        
        # Left side - User List (wider)
        left_frame = tk.Frame(content_frame, bg=self.card_bg, relief="raised", bd=1)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 15), pady=5)
        left_frame.configure(highlightbackground="#ddd", highlightthickness=1)
        
        # Left side header
        left_header = tk.Frame(left_frame, bg=self.primary_color, height=50)
        left_header.pack(fill="x", pady=(0, 15))
        left_header.pack_propagate(False)
        
        tk.Label(left_header, text="👥 Existing Users", 
                bg=self.primary_color, fg="white",
                font=("Arial", 14, "bold")).pack(expand=True)
        
        # User list container with scrollbar
        list_container = tk.Frame(left_frame, bg=self.card_bg)
        list_container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Create treeview for users
        columns = ("ID", "Username")
        self.tree = ttk.Treeview(list_container, columns=columns, show="headings", height=18)
        
        # Define headings
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Username", text="Username", anchor="w")
        
        # Define columns (wider)
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Username", width=250, anchor="w")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid treeview and scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(0, weight=1)
        
        # Action buttons for user list
        action_frame = tk.Frame(left_frame, bg=self.card_bg, height=60)
        action_frame.pack(fill="x", padx=15, pady=15)
        action_frame.pack_propagate(False)
        
        ttk.Button(action_frame, text="Refresh List", 
                  style="Secondary.TButton",
                  command=self.display_users).pack(side="left", padx=8)
        
        ttk.Button(action_frame, text="Edit Selected", 
                  style="Primary.TButton",
                  command=self.edit_selected_user).pack(side="left", padx=8)
        
        ttk.Button(action_frame, text="Delete Selected", 
                  style="Accent.TButton",
                  command=self.delete_selected_user).pack(side="left", padx=8)
        ttk.Button(action_frame, text="Back to Dashboard",
                  style="Secondary.TButton",
                  command=lambda: self.switch_frame("admin_dashboard")).pack(side="right", padx=8)
        
        # Right side - Add User Form (wider)
        right_frame = tk.Frame(content_frame, bg=self.card_bg, relief="raised", bd=1, width=400)
        right_frame.pack(side="right", fill="both", padx=(15, 0), pady=5)
        right_frame.pack_propagate(False)
        right_frame.configure(highlightbackground="#ddd", highlightthickness=1)
        
        # Right side header
        right_header = tk.Frame(right_frame, bg=self.primary_color, height=50)
        right_header.pack(fill="x", pady=(0, 20))
        right_header.pack_propagate(False)
        
        tk.Label(right_header, text="➕ Add New User", 
                bg=self.primary_color, fg="white",
                font=("Arial", 14, "bold")).pack(expand=True)
        
        # Form container
        form_container = tk.Frame(right_frame, bg=self.card_bg)
        form_container.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Username field
        tk.Label(form_container, text="Username:", 
                bg=self.card_bg, fg=self.primary_color,
                font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        self.username_entry = tk.Entry(form_container, font=("Arial", 11), 
                                      relief="solid", bd=1, width=30)
        self.username_entry.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.username_entry.insert(0, "Enter username")
        self.username_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, "username"))
        
        # Password field
        tk.Label(form_container, text="Password:", 
                bg=self.card_bg, fg=self.primary_color,
                font=("Arial", 11, "bold")).grid(row=2, column=0, sticky="w", pady=(0, 8))
        
        self.password_entry = tk.Entry(form_container, font=("Arial", 11), 
                                      show="*", relief="solid", bd=1, width=30)
        self.password_entry.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        self.password_entry.insert(0, "Enter password")
        self.password_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, "password"))
        
        # Add user button
        ttk.Button(form_container, text="Add User", 
                  style="Success.TButton",
                  command=self.add_user).grid(row=4, column=0, pady=10)
        
        # Configure grid weights
        form_container.columnconfigure(0, weight=1)
        
        # Navigation buttons at bottom
        nav_frame = tk.Frame(main_container, bg=self.light_bg, height=60)
        nav_frame.pack(fill="x", pady=(20, 0))
        nav_frame.pack_propagate(False)
        
        ttk.Button(nav_frame, text="← Back to Dashboard", 
                  style="Secondary.TButton",
                  command=lambda: self.switch_frame("admin_dashboard")).pack(side="left", padx=20, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(main_container, textvariable=self.status_var, 
                             bg=self.light_bg, fg="#7f8c8d", font=("Arial", 9),
                             anchor="e")
        status_bar.pack(fill="x", pady=(10, 0))

    def clear_placeholder(self, event, field_type):
        if field_type == "username" and self.username_entry.get() == "Enter username":
            self.username_entry.delete(0, tk.END)
            self.username_entry.config(fg="black")  # Change text color to black
        elif field_type == "password" and self.password_entry.get() == "Enter password":
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(show="*", fg="black")  # Change text color to black

    def display_users(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM users ORDER BY id")
        users = cursor.fetchall()
        conn.close()

        # Add users to treeview
        for user in users:
            self.tree.insert("", "end", values=user)
            
        self.status_var.set(f"Loaded {len(users)} users")

    def add_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or username == "Enter username":
            messagebox.showwarning("Missing Field", "Please enter a username.")
            return
            
        if not password or password == "Enter password":
            messagebox.showwarning("Missing Field", "Please enter a password.")
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
            self.status_var.set(f"User '{username}' added successfully")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
            self.status_var.set("Error: Username already exists")

    def delete_selected_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a user to delete.")
            return
            
        user_id = self.tree.item(selected[0])['values'][0]
        username = self.tree.item(selected[0])['values'][1]
        
        confirm = messagebox.askyesno("Confirm Deletion", 
                                     f"Are you sure you want to delete user '{username}'?")
        if confirm:
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "User deleted successfully.")
            self.display_users()
            self.status_var.set(f"User '{username}' deleted")

    def edit_selected_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a user to edit.")
            return
            
        user_id = self.tree.item(selected[0])['values'][0]
        username = self.tree.item(selected[0])['values'][1]
        
        self.edit_user((user_id, username))

    def edit_user(self, user):
        edit_win = tk.Toplevel(self)
        edit_win.title("Edit User")
        edit_win.geometry("400x300")
        edit_win.configure(bg=self.light_bg)
        edit_win.resizable(False, False)
        
        # Center the window
        edit_win.transient(self)
        edit_win.grab_set()
        
        # Position in center of parent
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - 400) // 2
        y = self.winfo_y() + (self.winfo_height() - 300) // 2
        edit_win.geometry(f"+{x}+{y}")
        
        header = tk.Frame(edit_win, bg=self.primary_color, height=60)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        tk.Label(header, text=f"Edit User: {user[1]}", 
                bg=self.primary_color, fg="white",
                font=("Arial", 14, "bold")).pack(expand=True)
        
        form_frame = tk.Frame(edit_win, bg=self.light_bg)
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(form_frame, text="Username:", 
                bg=self.light_bg, fg=self.primary_color,
                font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 8))
        
        username_entry = tk.Entry(form_frame, font=("Arial", 11), 
                                 relief="solid", bd=1, width=30)
        username_entry.pack(fill="x", pady=(0, 20))
        username_entry.insert(0, user[1])
        
        tk.Label(form_frame, text="Password:", 
                bg=self.light_bg, fg=self.primary_color,
                font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 8))
        
        password_entry = tk.Entry(form_frame, font=("Arial", 11), 
                                 show="*", relief="solid", bd=1, width=30)
        password_entry.pack(fill="x", pady=(0, 20))
        password_entry.insert(0, "Enter new password (leave blank to keep current)")
        password_entry.bind("<FocusIn>", lambda e: password_entry.delete(0, tk.END) if password_entry.get().startswith("Enter new password") else None)
        
        # Define save_changes function first
        def save_changes():
            new_username = username_entry.get().strip()
            new_password = password_entry.get().strip()
            
            if not new_username:
                messagebox.showerror("Error", "Username cannot be empty.")
                return
                
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()
            
            if new_password and not new_password.startswith("Enter new password"):
                cursor.execute("UPDATE users SET username = ?, password = ? WHERE id = ?",
                               (new_username, new_password, user[0]))
            else:
                cursor.execute("UPDATE users SET username = ? WHERE id = ?",
                               (new_username, user[0]))
                               
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "User updated successfully.")
            edit_win.destroy()
            self.display_users()
            self.status_var.set(f"User '{new_username}' updated")

        # Now create the Update button after the function is defined
        update_btn = ttk.Button(form_frame, text="Update", style="Primary.TButton", command=save_changes)
        update_btn.pack(fill="x", pady=(0, 10))

        button_frame = tk.Frame(form_frame, bg=self.light_bg)
        button_frame.pack(fill="x", pady=20)
        
        ttk.Button(button_frame, text="Save Changes", 
                  style="Success.TButton",
                  command=save_changes).pack(side="right", padx=8)
        
        ttk.Button(button_frame, text="Cancel", 
                  style="Secondary.TButton",
                  command=edit_win.destroy).pack(side="right", padx=8)