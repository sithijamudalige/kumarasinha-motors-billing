import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from datetime import datetime

DB_NAME = "inventory.db"

class ViewPartsTable(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame

        # --- Filters ---
        tk.Label(self, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        tk.Entry(self, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Model:").grid(row=0, column=2, padx=5, pady=5)
        self.model_var = tk.StringVar()
        tk.Entry(self, textvariable=self.model_var).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self, text="Min Qty:").grid(row=0, column=4, padx=5, pady=5)
        self.min_qty_var = tk.StringVar()
        tk.Entry(self, textvariable=self.min_qty_var, width=6).grid(row=0, column=5, padx=5, pady=5)

        tk.Label(self, text="Max Qty:").grid(row=0, column=6, padx=5, pady=5)
        self.max_qty_var = tk.StringVar()
        tk.Entry(self, textvariable=self.max_qty_var, width=6).grid(row=0, column=7, padx=5, pady=5)

        tk.Button(self, text="Search", command=self.load_parts).grid(row=0, column=8, padx=5, pady=5)
        tk.Button(self, text="Generate Report", command=self.generate_report).grid(row=0, column=9, padx=5, pady=5)

        # --- Table ---
        columns = ("ID", "Name", "Model", "Size", "Buy Price", "Sell Price", "Qty", "Total Cost")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=20)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.grid(row=1, column=0, columnspan=10, sticky="nsew", padx=10, pady=10)

        # Scrollbars
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=10, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(9, weight=1)

        # --- Back button ---
        tk.Button(self, text="⬅ Back to Admin Dashboard", command=lambda: self.switch_frame("admin_dashboard"),
                  bg="lightgray").grid(row=2, column=0, columnspan=11, pady=10)

        # Load data
        self.load_parts()

    def load_parts(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        query = "SELECT part_id, part_name, part_model, part_size, buy_price, selling_price, quantity, total_cost FROM parts WHERE 1=1"
        params = []

        if self.name_var.get():
            query += " AND part_name LIKE ?"
            params.append(f"%{self.name_var.get()}%")

        if self.model_var.get():
            query += " AND part_model LIKE ?"
            params.append(f"%{self.model_var.get()}%")

        if self.min_qty_var.get().isdigit():
            query += " AND quantity >= ?"
            params.append(int(self.min_qty_var.get()))

        if self.max_qty_var.get().isdigit():
            query += " AND quantity <= ?"
            params.append(int(self.max_qty_var.get()))

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            tag = "low_stock" if r[6] < 5 else ""
            self.tree.insert("", "end", values=r, tags=(tag,))

        self.tree.tag_configure("low_stock", background="red", foreground="white")

    def generate_report(self):
        # Ask where to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Report As"
        )
        if not file_path:
            return

        # Fetch current filtered data
        query = "SELECT part_id, part_name, part_model, part_size, buy_price, selling_price, quantity, total_cost FROM parts WHERE 1=1"
        params = []

        if self.name_var.get():
            query += " AND part_name LIKE ?"
            params.append(f"%{self.name_var.get()}%")

        if self.model_var.get():
            query += " AND part_model LIKE ?"
            params.append(f"%{self.model_var.get()}%")

        if self.min_qty_var.get().isdigit():
            query += " AND quantity >= ?"
            params.append(int(self.min_qty_var.get()))

        if self.max_qty_var.get().isdigit():
            query += " AND quantity <= ?"
            params.append(int(self.max_qty_var.get()))

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        # --- Create PDF ---
        c = canvas.Canvas(file_path, pagesize=landscape(A4))
        width, height = landscape(A4)

        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(30, height - 40, "Parts Report")
        c.setFont("Helvetica", 10)
        c.drawString(30, height - 60, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Table
        y = height - 100
        headers = ["ID", "Name", "Model", "Size", "Buy Price", "Sell Price", "Qty", "Total Cost"]
        col_widths = [50, 120, 100, 80, 80, 80, 60, 100]

        # Print headers
        x = 30
        for i, h in enumerate(headers):
            c.drawString(x, y, h)
            x += col_widths[i]
        y -= 20

        # Print rows
        for row in rows:
            x = 30
            for i, value in enumerate(row):
                c.drawString(x, y, str(value))
                x += col_widths[i]
            y -= 20
            if y < 50:  # new page
                c.showPage()
                y = height - 50

        c.save()
        messagebox.showinfo("Success", f"Report saved to {file_path}")
