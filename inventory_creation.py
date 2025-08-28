import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Frame
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import os
from datetime import datetime

LETTERHEAD_PATH = r"C:\projects\POS_Project\KUMARASINGHE MOTORS letter head.pdf"

class InventoryCreation(tk.Frame):
    def __init__(self, master, show_frame_callback=None):
        super().__init__(master)
        self.master = master
        self.show_frame_callback = show_frame_callback
        self.items = []
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_style()
        
        self.create_widgets()
        
    def configure_style(self):
        # Configure colors
        self.bg_color = "#f5f7fa"
        self.header_bg = "#2c3e50"
        self.accent_color = "#3498db"
        self.light_accent = "#ecf0f1"
        self.success_color = "#2ecc71"
        self.warning_color = "#e74c3c"
        
        # Configure styles
        self.style.configure("Header.TLabel", 
                            background=self.header_bg, 
                            foreground="white", 
                            font=("Arial", 14, "bold"),
                            padding=10)
        
        self.style.configure("Section.TLabel", 
                            font=("Arial", 11, "bold"),
                            foreground=self.header_bg,
                            padding=(5, 10, 5, 5))
        
        self.style.configure("Accent.TButton", 
                            background=self.accent_color,
                            foreground="white",
                            font=("Arial", 10, "bold"),
                            focuscolor=self.accent_color)
        
        self.style.configure("Success.TButton", 
                            background=self.success_color,
                            foreground="white",
                            font=("Arial", 10, "bold"),
                            focuscolor=self.success_color)
        
        self.style.configure("Warning.TButton", 
                            background=self.warning_color,
                            foreground="white",
                            font=("Arial", 10, "bold"),
                            focuscolor=self.warning_color)
        
        self.style.configure("Treeview", 
                            background="white",
                            fieldbackground="white",
                            foreground="black",
                            rowheight=25)
        
        self.style.configure("Treeview.Heading", 
                            background=self.light_accent,
                            foreground=self.header_bg,
                            font=("Arial", 10, "bold"))
        
        self.style.map("Accent.TButton", 
                      background=[('active', '#2980b9')])
        self.style.map("Success.TButton", 
                      background=[('active', '#27ae60')])
        self.style.map("Warning.TButton", 
                      background=[('active', '#c0392b')])
        
        # Configure frame background
        self.configure(background=self.bg_color)

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg=self.header_bg)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=(0, 10))
        
        tk.Label(header_frame, text="Inventory Creation System", 
                bg=self.header_bg, fg="white", 
                font=("Arial", 16, "bold")).pack(pady=10)
        
        # Main content frame
        content_frame = tk.Frame(self, bg=self.bg_color)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        # Configure grid weights
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.columnconfigure(3, weight=1)
        content_frame.columnconfigure(5, weight=1)
        
        # Date & Vehicle Registration section
        info_frame = tk.LabelFrame(content_frame, text=" Document Information ", 
                                  font=("Arial", 10, "bold"), bg=self.bg_color,
                                  relief=tk.GROOVE, bd=1)
        info_frame.grid(row=0, column=0, columnspan=6, sticky="ew", padx=5, pady=10)
        
        tk.Label(info_frame, text="Date:", bg=self.bg_color, 
                font=("Arial", 9)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = tk.Entry(info_frame, textvariable=self.date_var, 
                             font=("Arial", 9), width=15, relief=tk.SOLID, bd=1)
        date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(info_frame, text="Vehicle Reg No:", bg=self.bg_color, 
                font=("Arial", 9)).grid(row=0, column=2, sticky="w", padx=(20,5), pady=5)
        self.reg_no_var = tk.StringVar()
        reg_entry = tk.Entry(info_frame, textvariable=self.reg_no_var, 
                            font=("Arial", 9), width=15, relief=tk.SOLID, bd=1)
        reg_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Item entry section
        item_frame = tk.LabelFrame(content_frame, text=" Add New Item ", 
                                  font=("Arial", 10, "bold"), bg=self.bg_color,
                                  relief=tk.GROOVE, bd=1)
        item_frame.grid(row=1, column=0, columnspan=6, sticky="ew", padx=5, pady=10)
        
        tk.Label(item_frame, text="Item Name:", bg=self.bg_color, 
                font=("Arial", 9)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.item_name_var = tk.StringVar()
        item_entry = tk.Entry(item_frame, textvariable=self.item_name_var, 
                             font=("Arial", 9), width=20, relief=tk.SOLID, bd=1)
        item_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(item_frame, text="Quantity:", bg=self.bg_color, 
                font=("Arial", 9)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.qty_var = tk.StringVar()
        qty_entry = tk.Entry(item_frame, textvariable=self.qty_var, 
                            font=("Arial", 9), width=10, relief=tk.SOLID, bd=1)
        qty_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        tk.Label(item_frame, text="Price:", bg=self.bg_color, 
                font=("Arial", 9)).grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.price_var = tk.StringVar()
        price_entry = tk.Entry(item_frame, textvariable=self.price_var, 
                              font=("Arial", 9), width=10, relief=tk.SOLID, bd=1)
        price_entry.grid(row=0, column=5, padx=5, pady=5, sticky="w")

        # Buttons for item management
        button_frame = tk.Frame(item_frame, bg=self.bg_color)
        button_frame.grid(row=0, column=6, columnspan=3, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Add Item", command=self.add_item, 
                  style="Success.TButton", width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_item, 
                  style="Warning.TButton", width=12).pack(side=tk.LEFT, padx=5)

        # Items table with scrollbar
        table_frame = tk.Frame(content_frame, bg=self.bg_color)
        table_frame.grid(row=2, column=0, columnspan=6, sticky="nsew", padx=5, pady=10)
        content_frame.rowconfigure(2, weight=1)
        
        # Create treeview with scrollbar
        self.tree = ttk.Treeview(table_frame, columns=("Item", "Qty", "Price", "Total"), 
                                show="headings", height=8)
        
        # Define headings
        for col, width in zip(("Item", "Qty", "Price", "Total"), (250, 80, 100, 120)):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=tk.CENTER if col != "Item" else tk.W)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid treeview and scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Total label
        total_frame = tk.Frame(content_frame, bg=self.bg_color)
        total_frame.grid(row=3, column=0, columnspan=6, sticky="ew", padx=5, pady=10)
        
        self.total_label = tk.Label(total_frame, text="Total: 0.00", 
                                   font=("Arial", 14, "bold"), fg=self.header_bg, bg=self.bg_color)
        self.total_label.pack(side=tk.RIGHT, padx=10)

        # Action buttons
        action_frame = tk.Frame(content_frame, bg=self.bg_color)
        action_frame.grid(row=4, column=0, columnspan=6, sticky="ew", padx=5, pady=10)
        
        ttk.Button(action_frame, text="Generate PDF", command=self.generate_pdf, 
                  style="Success.TButton", width=15).pack(side=tk.RIGHT, padx=5)
        ttk.Button(action_frame, text="Back to Dashboard", command=self.go_back, 
                  style="Accent.TButton", width=15).pack(side=tk.RIGHT, padx=5)
        ttk.Button(action_frame, text="Clear All", command=self.clear_all, 
                  style="Warning.TButton", width=15).pack(side=tk.LEFT, padx=5)

    def add_item(self):
        try:
            name = self.item_name_var.get().strip()
            if not name:
                messagebox.showerror("Error", "Item name cannot be empty.")
                return
                
            qty = int(self.qty_var.get())
            price = float(self.price_var.get())
            total = qty * price
            self.items.append((name, qty, price, total))
            self.tree.insert("", "end", values=(name, qty, f"{price:.2f}", f"{total:.2f}"))
            self.update_total()
            self.clear_inputs()
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price.")

    def edit_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to edit.")
            return
        try:
            idx = self.tree.index(selected[0])
            name = self.item_name_var.get().strip()
            if not name:
                messagebox.showerror("Error", "Item name cannot be empty.")
                return
                
            qty = int(self.qty_var.get())
            price = float(self.price_var.get())
            total = qty * price
            self.items[idx] = (name, qty, price, total)
            self.tree.item(selected[0], values=(name, qty, f"{price:.2f}", f"{total:.2f}"))
            self.update_total()
            self.clear_inputs()
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price.")

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to delete.")
            return
        idx = self.tree.index(selected[0])
        del self.items[idx]
        self.tree.delete(selected[0])
        self.update_total()

    def update_total(self):
        total_sum = sum(item[3] for item in self.items)
        self.total_label.config(text=f"Total: {total_sum:.2f}")

    def clear_inputs(self):
        self.item_name_var.set("")
        self.qty_var.set("")
        self.price_var.set("")
        
    def clear_all(self):
        if self.items:
            if messagebox.askyesno("Confirm", "Are you sure you want to clear all items?"):
                self.items.clear()
                for item in self.tree.get_children():
                    self.tree.delete(item)
                self.update_total()
                self.clear_inputs()

    def generate_pdf(self):
        if not self.items:
            messagebox.showerror("Error", "No items to generate PDF.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="inventory_report.pdf"
        )
        if not output_path:
            return

        # Step 1: Create a PDF with reserved letterhead space
        temp_content_path = "temp_content.pdf"
        doc = SimpleDocTemplate(temp_content_path, pagesize=A4, topMargin=6.11*28.35)  # Letterhead height in points
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph(f"Date: {self.date_var.get()}", styles['Normal']))
        elements.append(Paragraph(f"Vehicle Reg No: {self.reg_no_var.get()}", styles['Normal']))
        elements.append(Spacer(1, 12))

        data = [["Item", "Qty", "Price", "Total"]]
        for name, qty, price, total in self.items:
            data.append([name, qty, f"{price:.2f}", f"{total:.2f}"])
        data.append(["", "", "Grand Total", f"{sum(item[3] for item in self.items):.2f}"])

        table = Table(data, colWidths=[200, 50, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))

        elements.append(table)
        doc.build(elements)

        # Step 2: Merge with letterhead
        letterhead_reader = PdfReader(LETTERHEAD_PATH)
        content_reader = PdfReader(temp_content_path)
        writer = PdfWriter()

        # Merge content page with letterhead
        page = letterhead_reader.pages[0]
        page.merge_page(content_reader.pages[0])
        writer.add_page(page)

        # Add extra pages if any
        for i in range(1, len(content_reader.pages)):
            writer.add_page(content_reader.pages[i])

        with open(output_path, "wb") as out_file:
            writer.write(out_file)

        os.remove(temp_content_path)
        messagebox.showinfo("Success", f"PDF saved to {output_path}")

    def go_back(self):
        if self.show_frame_callback:
            self.show_frame_callback("user_dashboard")