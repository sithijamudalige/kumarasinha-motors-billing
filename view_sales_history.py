import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from datetime import datetime
from tkcalendar import DateEntry

DB_NAME = "inventory.db"

class ViewSalesHistory(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame

        # Title
        tk.Label(self, text="Sales History", font=("Arial", 16)).grid(row=0, column=0, columnspan=6, pady=10)

        # Filters
        tk.Label(self, text="Sold By (Username):").grid(row=1, column=0, padx=5, sticky="e")
        self.sold_by_var = tk.StringVar()
        tk.Entry(self, textvariable=self.sold_by_var).grid(row=1, column=1, padx=5)

        tk.Label(self, text="From Date:").grid(row=1, column=2, padx=5, sticky="e")
        self.from_date = DateEntry(self, width=12, background='darkblue', foreground='white',
                                   borderwidth=2, date_pattern="yyyy-mm-dd")
        self.from_date.grid(row=1, column=3, padx=5)

        tk.Label(self, text="To Date:").grid(row=1, column=4, padx=5, sticky="e")
        self.to_date = DateEntry(self, width=12, background='darkblue', foreground='white',
                                 borderwidth=2, date_pattern="yyyy-mm-dd")
        self.to_date.grid(row=1, column=5, padx=5)

        tk.Button(self, text="Search", command=self.search).grid(row=1, column=6, padx=5)
        tk.Button(self, text="Clear", command=self.load_sales).grid(row=1, column=7, padx=5)

        # Table
        columns = ("Sale ID", "Part ID", "Part Name", "Quantity", "Price", "Total", "Sale Date", "Sale Time", "Sold By")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=20)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120 if col not in ("Part Name", "Sold By") else 180)

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

        # Store filtered rows for report
        self.filtered_rows = None

        # Load data
        self.load_sales()

    def load_sales(self):
        """Load all sales records"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""SELECT sale_id, part_id, part_name, quantity, price, total, sale_date, sale_time, sold_by
                          FROM sales_history ORDER BY sale_date DESC, sale_time DESC""")
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            self.tree.insert("", "end", values=r)

        self.filtered_rows = rows

    def search(self):
        """Apply filters to sales history"""
        sold_by = self.sold_by_var.get().strip()
        from_date = self.from_date.get_date().strftime("%Y-%m-%d")
        to_date = self.to_date.get_date().strftime("%Y-%m-%d")

        query = "SELECT sale_id, part_id, part_name, quantity, price, total, sale_date, sale_time, sold_by FROM sales_history WHERE 1=1"
        params = []

        if sold_by:
            query += " AND sold_by LIKE ?"
            params.append(f"%{sold_by}%")
        if from_date:
            query += " AND DATE(sale_date) >= ?"
            params.append(from_date)
        if to_date:
            query += " AND DATE(sale_date) <= ?"
            params.append(to_date)

        query += " ORDER BY sale_date DESC, sale_time DESC"

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

        self.filtered_rows = rows

    def generate_report(self):
        """Generate PDF report"""
        if not self.filtered_rows:
            messagebox.showwarning("No Data", "No records to generate report.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Sales History Report As"
        )
        if not file_path:
            return

        # Create PDF
        c = canvas.Canvas(file_path, pagesize=landscape(A4))
        width, height = landscape(A4)

        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(30, height - 40, "Sales History Report")
        c.setFont("Helvetica", 10)
        c.drawString(30, height - 60, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Table headers
        y = height - 100
        headers = ["Sale ID", "Part ID", "Part Name", "Quantity", "Price", "Total", "Sale Date", "Sale Time", "Sold By"]
        col_widths = [50, 50, 150, 50, 50, 60, 70, 70, 100]

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
