import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from datetime import datetime
from tkcalendar import DateEntry   # ✅ new import

DB_NAME = "inventory.db"

class ViewLoginHistory(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame

        # Title
        tk.Label(self, text="Login History", font=("Arial", 16)).grid(row=0, column=0, columnspan=6, pady=10)

        # Filters
        tk.Label(self, text="Username:").grid(row=1, column=0, padx=5, sticky="e")
        self.username_var = tk.StringVar()
        tk.Entry(self, textvariable=self.username_var).grid(row=1, column=1, padx=5)

        # From Date Calendar
        tk.Label(self, text="From Date:").grid(row=1, column=2, padx=5, sticky="e")
        self.from_date = DateEntry(self, width=12, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern="yyyy-mm-dd")
        self.from_date.grid(row=1, column=3, padx=5)

        # To Date Calendar
        tk.Label(self, text="To Date:").grid(row=1, column=4, padx=5, sticky="e")
        self.to_date = DateEntry(self, width=12, background='darkblue',
                                 foreground='white', borderwidth=2, date_pattern="yyyy-mm-dd")
        self.to_date.grid(row=1, column=5, padx=5)

        tk.Button(self, text="Search", command=self.search).grid(row=1, column=6, padx=5)
        tk.Button(self, text="Clear", command=self.load_history).grid(row=1, column=7, padx=5)

        # Table
        columns = ("ID", "Username", "Login Time")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=20)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        self.tree.grid(row=2, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

        # Scrollbar
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vsb.grid(row=2, column=6, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        # Buttons
        tk.Button(self, text="Generate Report", command=self.generate_report).grid(row=3, column=0, pady=10)
        tk.Button(self, text="⬅ Back to Admin Dashboard",
                  command=lambda: self.switch_frame("admin_dashboard"),
                  bg="lightgray").grid(row=3, column=1, pady=10)

        # For filtered data storage
        self.filtered_rows = None

        # Load data
        self.load_history()

    def load_history(self):
        """Load all login history records"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, login_time FROM login_history ORDER BY login_time DESC")
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            self.tree.insert("", "end", values=r)

        self.filtered_rows = rows  # store for report

    def search(self):
        """Apply filters to login history"""
        username = self.username_var.get().strip()
        from_date = self.from_date.get_date().strftime("%Y-%m-%d")  # ✅ calendar value
        to_date = self.to_date.get_date().strftime("%Y-%m-%d")      # ✅ calendar value

        query = "SELECT id, username, login_time FROM login_history WHERE 1=1"
        params = []

        if username:
            query += " AND username LIKE ?"
            params.append(f"%{username}%")
        if from_date:
            query += " AND DATE(login_time) >= ?"
            params.append(from_date)
        if to_date:
            query += " AND DATE(login_time) <= ?"
            params.append(to_date)

        query += " ORDER BY login_time DESC"

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        # Update tree
        for row in self.tree.get_children():
            self.tree.delete(row)
        for r in rows:
            self.tree.insert("", "end", values=r)

        self.filtered_rows = rows  # save for report

    def generate_report(self):
        """Generate PDF report (filtered or full)"""
        if not self.filtered_rows:
            messagebox.showwarning("No Data", "No records to generate report.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Login History Report As"
        )
        if not file_path:
            return

        # Create PDF
        c = canvas.Canvas(file_path, pagesize=landscape(A4))
        width, height = landscape(A4)

        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(30, height - 40, "Login History Report")
        c.setFont("Helvetica", 10)
        c.drawString(30, height - 60, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Table headers
        y = height - 100
        headers = ["ID", "Username", "Login Time"]
        col_widths = [50, 200, 200]

        x = 30
        for i, h in enumerate(headers):
            c.drawString(x, y, h)
            x += col_widths[i]
        y -= 20

        # Rows
        for row in self.filtered_rows:
            x = 30
            for i, value in enumerate(row):
                c.drawString(x, y, str(value))
                x += col_widths[i]
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50

        c.save()
        messagebox.showinfo("Success", f"Report saved to {file_path}")
