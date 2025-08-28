import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from datetime import datetime
from tkcalendar import DateEntry

DB_NAME = "inventory.db"

class ViewLoginHistory(tk.Frame):
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
        
        title_label = tk.Label(header_frame, text="Login History", 
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
        
        # Username filter
        tk.Label(filter_frame, text="Username:", bg='#f5f5f7', 
                font=("Segoe UI", 9)).grid(row=0, column=0, padx=5, pady=8, sticky='e')
        self.username_var = tk.StringVar()
        username_entry = tk.Entry(filter_frame, textvariable=self.username_var, 
                                 font=("Segoe UI", 9), relief='solid', bd=1, width=15)
        username_entry.grid(row=0, column=1, padx=5, pady=8, sticky='w')
        
        # From Date filter
        tk.Label(filter_frame, text="From Date:", bg='#f5f5f7', 
                font=("Segoe UI", 9)).grid(row=0, column=2, padx=5, pady=8, sticky='e')
        self.from_date = DateEntry(filter_frame, width=12, background='#3498db',
                                  foreground='white', borderwidth=1, 
                                  date_pattern="yyyy-mm-dd", font=("Segoe UI", 9))
        self.from_date.grid(row=0, column=3, padx=5, pady=8, sticky='w')
        
        # To Date filter
        tk.Label(filter_frame, text="To Date:", bg='#f5f5f7', 
                font=("Segoe UI", 9)).grid(row=0, column=4, padx=5, pady=8, sticky='e')
        self.to_date = DateEntry(filter_frame, width=12, background='#3498db',
                                foreground='white', borderwidth=1, 
                                date_pattern="yyyy-mm-dd", font=("Segoe UI", 9))
        self.to_date.grid(row=0, column=5, padx=5, pady=8, sticky='w')
        
        # Action buttons
        button_frame = tk.Frame(filter_frame, bg='#f5f5f7')
        button_frame.grid(row=0, column=6, padx=10, pady=8, sticky='e')
        
        search_btn = tk.Button(button_frame, text="Search", command=self.search,
                              font=("Segoe UI", 9, "bold"), bg='#3498db', fg='white',
                              relief='flat', padx=12, pady=5, cursor='hand2')
        search_btn.pack(side='left', padx=3)
        search_btn.bind("<Enter>", lambda e: search_btn.config(bg='#2980b9'))
        search_btn.bind("<Leave>", lambda e: search_btn.config(bg='#3498db'))
        
        clear_btn = tk.Button(button_frame, text="Clear", command=self.load_history,
                             font=("Segoe UI", 9), bg='#95a5a6', fg='white',
                             relief='flat', padx=12, pady=5, cursor='hand2')
        clear_btn.pack(side='left', padx=3)
        clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg='#7f8c8d'))
        clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg='#95a5a6'))
        
        # Configure column weights for responsive layout
        for i in range(7):
            filter_frame.columnconfigure(i, weight=1)
        
        # Table container with shadow effect
        table_container = tk.Frame(main_container, bg='#e0e0e0')
        table_container.pack(fill='both', expand=True)
        
        # Inner table frame
        table_inner = tk.Frame(table_container, bg='white', relief='flat', bd=0)
        table_inner.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Table
        columns = ("ID", "Username", "Login Time")
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
        col_widths = [80, 150, 250]
        for idx, col in enumerate(columns):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths[idx], anchor='center' if col == 'ID' else 'w')
        
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
        
        # Report button frame
        report_frame = tk.Frame(main_container, bg='#f5f5f7')
        report_frame.pack(fill='x', pady=(15, 5))
        
        report_btn = tk.Button(report_frame, text="Generate PDF Report", command=self.generate_report,
                              font=("Segoe UI", 10, "bold"), bg='#2ecc71', fg='white',
                              relief='flat', padx=20, pady=8, cursor='hand2')
        report_btn.pack()
        report_btn.bind("<Enter>", lambda e: report_btn.config(bg='#27ae60'))
        report_btn.bind("<Leave>", lambda e: report_btn.config(bg='#2ecc71'))
        
        # Status bar
        status_frame = tk.Frame(main_container, bg='#34495e', height=25)
        status_frame.pack(fill='x', pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Ready", bg='#34495e', fg='white', font=("Segoe UI", 9))
        self.status_label.pack(side='left', padx=10)
        
        # For filtered data storage
        self.filtered_rows = None

        # Load data
        self.load_history()

    def load_history(self):
        """Load all login history records"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, login_time FROM login_history ORDER BY login_time DESC")
            rows = cursor.fetchall()
            conn.close()

            for r in rows:
                self.tree.insert("", "end", values=r)

            self.filtered_rows = rows  # store for report
            self.status_label.config(text=f"Loaded {len(rows)} login records")
            
            # Clear filters
            self.username_var.set("")
            # Reset dates to today
            today = datetime.now().date()
            self.from_date.set_date(today)
            self.to_date.set_date(today)
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading login history: {str(e)}")
            self.status_label.config(text="Error loading data")

    def search(self):
        """Apply filters to login history"""
        username = self.username_var.get().strip()
        from_date = self.from_date.get_date().strftime("%Y-%m-%d")
        to_date = self.to_date.get_date().strftime("%Y-%m-%d")

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

        try:
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
            self.status_label.config(text=f"Found {len(rows)} matching records")
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Error searching login history: {str(e)}")
            self.status_label.config(text="Search error")

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

        try:
            # Create PDF
            c = canvas.Canvas(file_path, pagesize=landscape(A4))
            width, height = landscape(A4)

            # Header
            c.setFont("Helvetica-Bold", 16)
            c.drawString(30, height - 40, "Login History Report")
            c.setFont("Helvetica", 10)
            c.drawString(30, height - 60, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Add filter info if any filters are applied
            y_offset = 80
            filter_info = ""
            if self.username_var.get():
                filter_info += f"Username: {self.username_var.get()} "
            if self.from_date.get_date().strftime("%Y-%m-%d") != datetime.now().date().strftime("%Y-%m-%d") or \
               self.to_date.get_date().strftime("%Y-%m-%d") != datetime.now().date().strftime("%Y-%m-%d"):
                filter_info += f"Date Range: {self.from_date.get_date().strftime('%Y-%m-%d')} to {self.to_date.get_date().strftime('%Y-%m-%d')}"
            
            if filter_info:
                c.drawString(30, height - y_offset, f"Filters: {filter_info}")
                y_offset += 20

            # Table headers
            y = height - y_offset - 20
            headers = ["ID", "Username", "Login Time"]
            col_widths = [80, 150, 250]

            x = 30
            for i, h in enumerate(headers):
                c.drawString(x, y, h)
                x += col_widths[i]
            y -= 20

            # Draw line under headers
            c.line(30, y + 15, 30 + sum(col_widths), y + 15)

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
            self.status_label.config(text=f"Report generated: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
            self.status_label.config(text="Error generating report")