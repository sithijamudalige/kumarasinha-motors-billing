# parts_management.py
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from db_parts import get_all_parts, delete_part, update_quantity, update_part

class PartsManagement(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame
        self.configure(bg='#f8f9fa')
        
        # Header section
        header_frame = tk.Frame(self, bg='#3a7ca5', height=70)
        header_frame.pack(fill='x', pady=(0, 15))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Parts Management", font=("Segoe UI", 18, "bold"), 
                bg='#3a7ca5', fg='white').pack(side='left', padx=25, pady=20)
                
        # Navigation buttons
        nav_frame = tk.Frame(header_frame, bg='#3a7ca5')
        nav_frame.pack(side='right', padx=20)
        
        tk.Button(nav_frame, text="Back to Admin", command=lambda: switch_frame("admin_dashboard"),
                 bg='#5c9ead', fg='white', font=("Segoe UI", 9, "bold"), width=15, height=1,
                 relief='flat', cursor='hand2', activebackground='#4a8c9d').pack(side='right', padx=5)
                 
        tk.Button(nav_frame, text="Add New Part", command=lambda: switch_frame("add_parts"),
                 bg='#2a9d8f', fg='white', font=("Segoe UI", 9, "bold"), width=12, height=1,
                 relief='flat', cursor='hand2', activebackground='#21867a').pack(side='right', padx=5)
        
        # Search and filter section
        filter_frame = tk.Frame(self, bg='#f8f9fa', padx=20, pady=10)
        filter_frame.pack(fill='x', pady=(0, 10))
        
        search_container = tk.Frame(filter_frame, bg='#f8f9fa')
        search_container.pack(side='left')
        
        tk.Label(search_container, text="Search Parts:", font=("Segoe UI", 10, "bold"), 
                bg='#f8f9fa', fg='#495057').pack(anchor='w')
        
        search_box = tk.Frame(search_container, bg='#dee2e6', padx=2, pady=2)
        search_box.pack(pady=(5, 0))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_box, textvariable=self.search_var, width=30, 
                               font=("Segoe UI", 10), relief='flat', bg='white')
        search_entry.pack(side='left')
        search_entry.bind('<KeyRelease>', self.filter_parts)
        
        search_icon = tk.Label(search_box, text="🔍", bg='#dee2e6', font=("Segoe UI", 10))
        search_icon.pack(side='left', padx=(5, 5))
        
        tk.Button(filter_frame, text="Clear Filters", command=self.clear_filter,
                 bg='#6c757d', fg='white', font=("Segoe UI", 9), width=12, relief='flat',
                 cursor='hand2', activebackground='#5a6268').pack(side='right', padx=5)
        
        # Stats summary
        self.summary_frame = tk.Frame(self, bg='#e9ecef', height=60)
        self.summary_frame.pack(fill='x', padx=20, pady=(0, 15))
        self.summary_frame.pack_propagate(False)
        self.update_summary()
        
        # Parts table frame
        table_container = tk.Frame(self, bg='#ffffff', relief='flat', highlightthickness=1, 
                                  highlightbackground='#ced4da')
        table_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create a canvas and scrollbar for the table
        self.canvas = tk.Canvas(table_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)
        
        # Initialize parts display
        self.parts_frame = self.scrollable_frame
        self.display_parts()

    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def update_summary(self):
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
            
        parts = get_all_parts()
        total_parts = len(parts)
        total_value = sum(float(part[6]) for part in parts if part[6])
        low_stock = sum(1 for part in parts if part[5] and int(part[5]) < 5)
        
        stats = [
            ("Total Parts", total_parts, "#3a7ca5"),
            ("Total Value", f"${total_value:,.2f}", "#2a9d8f"),
            ("Low Stock Items", low_stock, "#e76f51")
        ]
        
        for i, (label, value, color) in enumerate(stats):
            stat_frame = tk.Frame(self.summary_frame, bg='#e9ecef')
            stat_frame.pack(side='left', expand=True, fill='both', padx=(20 if i == 0 else 0, 20))
            
            tk.Label(stat_frame, text=label, font=("Segoe UI", 9), 
                    bg='#e9ecef', fg='#6c757d').pack(pady=(10, 0))
            tk.Label(stat_frame, text=value, font=("Segoe UI", 14, "bold"), 
                    bg='#e9ecef', fg=color).pack(pady=(0, 10))
        
    def filter_parts(self, event=None):
        search_term = self.search_var.get().lower()
        
        for widget in self.parts_frame.winfo_children():
            if hasattr(widget, 'part_data'):
                part_data = widget.part_data
                # Check if search term matches any part field
                match_found = any(search_term in str(field).lower() for field in part_data)
                if search_term and not match_found:
                    widget.pack_forget()
                else:
                    widget.pack(fill='x', pady=(0, 1))
    
    def clear_filter(self):
        self.search_var.set("")
        self.display_parts()
        
    def display_parts(self):
        for widget in self.parts_frame.winfo_children():
            widget.destroy()

        parts = get_all_parts()
        
        if not parts:
            no_parts_frame = tk.Frame(self.parts_frame, bg='white', height=200)
            no_parts_frame.pack(fill='both', expand=True)
            no_parts_frame.pack_propagate(False)
            
            tk.Label(no_parts_frame, text="No parts found", font=("Segoe UI", 14), 
                    bg='white', fg='#6c757d').pack(pady=(80, 10))
            tk.Label(no_parts_frame, text="Add some parts to get started", 
                    font=("Segoe UI", 10), bg='white', fg='#adb5bd').pack()
            return

        # Create header with centered text and appropriate column widths
        headers = ["ID", "Name", "Model", "Size", "Buy Price", "Qty", "Total Value", "Sell Price", "Add Date", "Actions"]
        col_widths = [5, 20, 15, 10, 12, 8, 15, 12, 15, 15]  # Adjusted widths for better fit
        
        header_frame = tk.Frame(self.parts_frame, bg='#3a7ca5')
        header_frame.pack(fill='x', pady=(0, 5))
        
        for i, (col, width) in enumerate(zip(headers, col_widths)):
            tk.Label(header_frame, text=col, width=width, bg='#3a7ca5', fg='white', 
                    font=("Segoe UI", 10, "bold"), padx=5, pady=8, anchor='center').pack(side="left")

        for part in parts:
            # Determine row color based on stock level
            qty = part[5] if part[5] else 0
            try:
                qty_int = int(qty)
            except (ValueError, TypeError):
                qty_int = 0
                
            if qty_int == 0:
                row_color = '#ffeaea'  # Light red for out of stock
            elif qty_int < 5:
                row_color = '#fff3cd'  # Light yellow for low stock
            else:
                row_color = 'white'
                
            row = tk.Frame(self.parts_frame, bg=row_color, highlightbackground="#dee2e6", 
                          highlightthickness=1, padx=2, pady=2)
            row.pack(fill='x', pady=(0, 1))
            row.part_data = part  # Store part data for filtering
            
            # Display part data with proper formatting and alignment
            for i, (val, width) in enumerate(zip(part, col_widths)):
                if i >= 10:  # Skip some fields to fit the UI
                    continue
                    
                if i in [4, 6, 7]:  # Format currency fields
                    try:
                        display_text = f"${float(val):.2f}" if val else "$0.00"
                    except (ValueError, TypeError):
                        display_text = "$0.00"
                elif i == 5:  # Quantity - highlight if low
                    display_text = str(val) if val else "0"
                else:
                    display_text = str(val) if val else ""
                
                # Center align all cells except Name which is left-aligned
                anchor = 'w' if i == 1 else 'center'
                fg = '#e63946' if i == 5 and qty_int == 0 else ('#856404' if i == 5 and qty_int < 5 else '#2f3e46')
                
                tk.Label(row, text=display_text, width=width, anchor=anchor, 
                        bg=row_color, font=("Segoe UI", 9), fg=fg, padx=5).pack(side="left")

            # Action buttons
            action_frame = tk.Frame(row, bg=row_color)
            action_frame.pack(side="left", padx=5)
            
            tk.Button(action_frame, text="Edit", command=lambda p=part: self.edit_part(p),
                     bg='#5c9ead', fg='white', font=("Segoe UI", 8, "bold"), width=4, 
                     relief='flat', cursor='hand2', activebackground='#4a8c9d').pack(side='left', padx=1)
            
            tk.Button(action_frame, text="Qty", command=lambda p=part: self.update_part_quantity(p),
                     bg='#f4a261', fg='white', font=("Segoe UI", 8, "bold"), width=4, 
                     relief='flat', cursor='hand2', activebackground='#e76f51').pack(side='left', padx=1)
            
            tk.Button(action_frame, text="Delete", command=lambda p=part: self.remove_part(p),
                     bg='#e76f51', fg='white', font=("Segoe UI", 8, "bold"), width=5, 
                     relief='flat', cursor='hand2', activebackground='#d6543a').pack(side='left', padx=1)
        
        # Update summary after displaying parts
        self.update_summary()

    def remove_part(self, part):
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete part '{part[1]}'?",
                                     icon='warning')
        if confirm:
            delete_part(part[0])
            self.display_parts()
            messagebox.showinfo("Success", f"Part '{part[1]}' has been deleted successfully.")

    def update_part_quantity(self, part):
        current_qty = part[5] if part[5] else 0
        try:
            current_qty_int = int(current_qty)
        except (ValueError, TypeError):
            current_qty_int = 0
            
        qty = simpledialog.askinteger("Update Quantity", 
                                     f"Current quantity for '{part[1]}': {current_qty_int}\n\nEnter new quantity to add:",
                                     minvalue=0, initialvalue=0)
        if qty is not None:
            update_quantity(part[0], qty)
            self.display_parts()
            messagebox.showinfo("Success", f"Quantity for '{part[1]}' has been updated.")

    def edit_part(self, part):
        edit_win = tk.Toplevel(self)
        edit_win.title(f"Edit Part: {part[1]}")
        edit_win.geometry("450x400")
        edit_win.configure(bg='#f8f9fa')
        edit_win.resizable(False, False)
        
        # Center the window
        edit_win.transient(self)
        edit_win.grab_set()
        
        # Header
        header = tk.Frame(edit_win, bg='#3a7ca5', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text=f"Edit Part: {part[1]}", font=("Segoe UI", 14, "bold"), 
                bg='#3a7ca5', fg='white').pack(pady=20)
        
        # Main frame
        main_frame = tk.Frame(edit_win, bg='#f8f9fa', padx=25, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        entries = []
        labels = ["Name", "Model", "Size", "Buy Price", "Sell Price"]
        defaults = [part[1], part[2], part[3], str(part[4]), str(part[7])]
        
        for i, label in enumerate(labels):
            field_frame = tk.Frame(main_frame, bg='#f8f9fa')
            field_frame.pack(fill='x', pady=10)
            
            tk.Label(field_frame, text=label, width=12, anchor='w', 
                    font=("Segoe UI", 10, "bold"), bg='#f8f9fa', fg='#495057').pack(side='left')
            
            e = tk.Entry(field_frame, font=("Segoe UI", 10), relief='flat', 
                        bg='white', highlightthickness=1, highlightcolor='#3a7ca5',
                        highlightbackground='#ced4da')
            e.insert(0, defaults[i])
            e.pack(side='left', fill='x', expand=True, padx=(10, 0), ipady=3)
            entries.append(e)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg='#f8f9fa')
        button_frame.pack(pady=20)
        
        def save_changes():
            values = [e.get() for e in entries]
            try:
                updated_data = [
                    values[0] if values[0] else part[1],
                    values[1] if values[1] else part[2],
                    values[2] if values[2] else part[3],
                    float(values[3]) if values[3] else part[4],
                    float(values[4]) if values[4] else part[7],
                ]
            except ValueError:
                messagebox.showerror("Error", "Buy Price and Sell Price must be valid numbers.")
                return

            update_part(part[0], updated_data)
            edit_win.destroy()
            self.display_parts()
            messagebox.showinfo("Success", f"Part '{values[0]}' has been updated successfully.")

        tk.Button(button_frame, text="Save Changes", command=save_changes,
                 bg='#2a9d8f', fg='white', font=("Segoe UI", 10, "bold"), width=15, 
                 relief='flat', cursor='hand2', activebackground='#21867a', padx=10, pady=6).pack(side='left', padx=10)
        
        tk.Button(button_frame, text="Cancel", command=edit_win.destroy,
                 bg='#6c757d', fg='white', font=("Segoe UI", 10), width=10, 
                 relief='flat', cursor='hand2', activebackground='#5a6268', padx=10, pady=6).pack(side='left', padx=10)