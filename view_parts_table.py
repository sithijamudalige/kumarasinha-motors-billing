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
        self.config(bg='#f5f5f7')  # Light gray background
        
        # Main container with padding
        main_container = tk.Frame(self, bg='#f5f5f7')
        main_container.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Header section
        header_frame = tk.Frame(main_container, bg='#f5f5f7')
        header_frame.pack(fill='x', pady=(0, 15))
        
        title_label = tk.Label(header_frame, text="Parts Inventory", 
                              font=("Segoe UI", 18, "bold"), bg='#f5f5f7', fg='#2c3e50')
        title_label.pack(side='left')
        
        # Back button in header
        back_btn = tk.Button(header_frame, text="← Back to Dashboard", 
                            command=lambda: self.switch_frame("admin_dashboard"),
                            font=('Segoe UI', 10), bg='#95a5a6', fg='white',
                            relief='flat', padx=12, pady=4, cursor='hand2')
        back_btn.pack(side='right')
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg='#7f8c8d'))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg='#95a5a6'))
        
        # Filter section
        filter_frame = tk.LabelFrame(main_container, text=" Filter Options ", 
                                    font=("Segoe UI", 10, "bold"), 
                                    bg='#f5f5f7', fg='#2c3e50', relief='groove')
        filter_frame.pack(fill='x', pady=(0, 15))
        
        # Filter inputs
        tk.Label(filter_frame, text="Name:", bg='#f5f5f7', font=("Segoe UI", 9)).grid(row=0, column=0, padx=5, pady=8, sticky='e')
        self.name_var = tk.StringVar()
        name_entry = tk.Entry(filter_frame, textvariable=self.name_var, font=("Segoe UI", 9), relief='solid', bd=1)
        name_entry.grid(row=0, column=1, padx=5, pady=8, sticky='ew')

        tk.Label(filter_frame, text="Model:", bg='#f5f5f7', font=("Segoe UI", 9)).grid(row=0, column=2, padx=5, pady=8, sticky='e')
        self.model_var = tk.StringVar()
        model_entry = tk.Entry(filter_frame, textvariable=self.model_var, font=("Segoe UI", 9), relief='solid', bd=1)
        model_entry.grid(row=0, column=3, padx=5, pady=8, sticky='ew')

        tk.Label(filter_frame, text="Min Qty:", bg='#f5f5f7', font=("Segoe UI", 9)).grid(row=0, column=4, padx=5, pady=8, sticky='e')
        self.min_qty_var = tk.StringVar()
        min_qty_entry = tk.Entry(filter_frame, textvariable=self.min_qty_var, width=8, font=("Segoe UI", 9), relief='solid', bd=1)
        min_qty_entry.grid(row=0, column=5, padx=5, pady=8, sticky='w')

        tk.Label(filter_frame, text="Max Qty:", bg='#f5f5f7', font=("Segoe UI", 9)).grid(row=1, column=4, padx=5, pady=8, sticky='e')
        self.max_qty_var = tk.StringVar()
        max_qty_entry = tk.Entry(filter_frame, textvariable=self.max_qty_var, width=8, font=("Segoe UI", 9), relief='solid', bd=1)
        max_qty_entry.grid(row=1, column=5, padx=5, pady=8, sticky='w')
        
        # Action buttons
        button_frame = tk.Frame(filter_frame, bg='#f5f5f7')
        button_frame.grid(row=0, column=6, rowspan=2, padx=10, pady=8, sticky='e')
        
        search_btn = tk.Button(button_frame, text="Search", command=self.load_parts,
                              font=("Segoe UI", 9, "bold"), bg='#3498db', fg='white',
                              relief='flat', padx=15, pady=6, cursor='hand2')
        search_btn.pack(side='left', padx=5)
        search_btn.bind("<Enter>", lambda e: search_btn.config(bg='#2980b9'))
        search_btn.bind("<Leave>", lambda e: search_btn.config(bg='#3498db'))
        
        report_btn = tk.Button(button_frame, text="Generate PDF Report", command=self.generate_report,
                              font=("Segoe UI", 9, "bold"), bg='#2ecc71', fg='white',
                              relief='flat', padx=15, pady=6, cursor='hand2')
        report_btn.pack(side='left', padx=5)
        report_btn.bind("<Enter>", lambda e: report_btn.config(bg='#27ae60'))
        report_btn.bind("<Leave>", lambda e: report_btn.config(bg='#2ecc71'))
        
        # Configure column weights for responsive layout
        for i in range(6):
            filter_frame.columnconfigure(i, weight=1)
        filter_frame.columnconfigure(6, weight=2)
        
        # Table container with shadow effect
        table_container = tk.Frame(main_container, bg='#e0e0e0')
        table_container.pack(fill='both', expand=True)
        
        # Inner table frame
        table_inner = tk.Frame(table_container, bg='white', relief='flat', bd=0)
        table_inner.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Table
        columns = ("ID", "Name", "Model", "Size", "Buy Price", "Sell Price", "Qty", "Total Cost")
        self.tree = ttk.Treeview(table_inner, columns=columns, show="headings", height=18)
        
        # Style the treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="white",
                        foreground="#2c3e50",
                        rowheight=25,
                        fieldbackground="white",
                        font=('Segoe UI', 9))
        style.configure("Treeview.Heading",
                        background='#34495e',
                        foreground='white',
                        padding=8,
                        font=('Segoe UI', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#3498db')])
        
        # Configure columns
        col_widths = [50, 150, 120, 80, 90, 90, 60, 100]
        for idx, col in enumerate(columns):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths[idx], anchor='center' if col in ['ID', 'Qty'] else 'w')
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_inner, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_inner, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout for tree and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        table_inner.grid_rowconfigure(0, weight=1)
        table_inner.grid_columnconfigure(0, weight=1)
        
        # Status bar
        status_frame = tk.Frame(main_container, bg='#34495e', height=25)
        status_frame.pack(fill='x', pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Ready", bg='#34495e', fg='white', font=("Segoe UI", 9))
        self.status_label.pack(side='left', padx=10)
        
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

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()

            for r in rows:
                tag = "low_stock" if r[6] < 5 else ""
                self.tree.insert("", "end", values=r, tags=(tag,))

            self.tree.tag_configure("low_stock", background="#ffebee", foreground="#c62828")
            self.status_label.config(text=f"Loaded {len(rows)} records")
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading data: {str(e)}")
            self.status_label.config(text="Error loading data")

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

        try:
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
            self.status_label.config(text=f"Report generated: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
            self.status_label.config(text="Error generating report")