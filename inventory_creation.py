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
        self.create_widgets()

    def create_widgets(self):
        # Date & Vehicle Registration
        tk.Label(self, text="Date:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        tk.Entry(self, textvariable=self.date_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Vehicle Reg No:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.reg_no_var = tk.StringVar()
        tk.Entry(self, textvariable=self.reg_no_var).grid(row=0, column=3, padx=5, pady=5)

        # Item entry section
        tk.Label(self, text="Item Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.item_name_var = tk.StringVar()
        tk.Entry(self, textvariable=self.item_name_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Quantity:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.qty_var = tk.StringVar()
        tk.Entry(self, textvariable=self.qty_var).grid(row=1, column=3, padx=5, pady=5)

        tk.Label(self, text="Price:").grid(row=1, column=4, sticky="w", padx=5, pady=5)
        self.price_var = tk.StringVar()
        tk.Entry(self, textvariable=self.price_var).grid(row=1, column=5, padx=5, pady=5)

        tk.Button(self, text="Add Item", command=self.add_item).grid(row=1, column=6, padx=5, pady=5)
        #tk.Button(self, text="Edit Selected", command=self.edit_item).grid(row=1, column=7, padx=5, pady=5)
        tk.Button(self, text="Delete Selected", command=self.delete_item).grid(row=1, column=8, padx=5, pady=5)

        # Items table
        self.tree = ttk.Treeview(self, columns=("Item", "Qty", "Price", "Total"), show="headings")
        for col in ("Item", "Qty", "Price", "Total"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=2, column=0, columnspan=9, padx=5, pady=5)

        # Total label
        self.total_label = tk.Label(self, text="Total: 0.00", font=("Arial", 14))
        self.total_label.grid(row=3, column=0, columnspan=4, pady=10, sticky="w")

        # Buttons
        tk.Button(self, text="Generate PDF", command=self.generate_pdf).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(self, text="Back", command=self.go_back).grid(row=4, column=1, padx=5, pady=5)

    def add_item(self):
        try:
            name = self.item_name_var.get().strip()
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
            messagebox.showerror("Error", "Select an item to edit.")
            return
        try:
            idx = self.tree.index(selected[0])
            name = self.item_name_var.get().strip()
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
            messagebox.showerror("Error", "Select an item to delete.")
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
