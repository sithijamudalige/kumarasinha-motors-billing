# billing_system.py
import tkinter as tk
from tkinter import ttk, messagebox
import init_db  # Your database backend
from print_bill import print_or_save_bill


class BillingSystem(tk.Frame):
    def __init__(self, master, show_frame_callback=None):
        super().__init__(master)
        self.master = master
        self.show_frame_callback = show_frame_callback
        self.bill_items = []
        self.total_amount = 0.0
        
        # Configure colors
        self.primary_color = "#3498db"
        self.secondary_color = "#2c3e50"
        self.accent_color = "#e74c3c"
        self.success_color = "#27ae60"
        self.light_bg = "#ecf0f1"
        self.dark_text = "#2c3e50"
        self.light_text = "#ffffff"
        
        self.configure(bg=self.light_bg)
        self.create_widgets()
        
        # Bind resize event
        self.bind("<Configure>", self.on_resize)
        self.current_width = 0

    def create_widgets(self):
        parts = init_db.get_all_parts()
        self.parts_dict = {}
        for part_id, name, model, price in parts:
            self.parts_dict.setdefault(name, []).append((part_id, model, price))

        self.customer_number_var = tk.StringVar()
        self.part_name_var = tk.StringVar()
        self.part_model_var = tk.StringVar()
        self.qty_var = tk.StringVar()

        # Configure grid weights for responsiveness
        for i in range(7):
            self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(4, weight=1)  # Bill list area gets most space
        
        # Header Frame
        header_frame = tk.Frame(self, bg=self.secondary_color, height=80)
        header_frame.grid(row=0, column=0, columnspan=7, sticky="ew", padx=10, pady=(10, 20))
        header_frame.grid_propagate(False)
        
        title_label = tk.Label(header_frame, text="BILLING SYSTEM", font=("Arial", 20, "bold"), 
                              fg=self.light_text, bg=self.secondary_color)
        title_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Customer Information Frame
        customer_frame = tk.LabelFrame(self, text=" Customer Information ", font=("Arial", 12, "bold"),
                                      bg=self.light_bg, fg=self.secondary_color, padx=10, pady=10)
        customer_frame.grid(row=1, column=0, columnspan=7, padx=10, pady=5, sticky="ew")
        customer_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(customer_frame, text="Customer Number:", background=self.light_bg, 
                 font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        customer_entry = ttk.Entry(customer_frame, textvariable=self.customer_number_var, font=("Arial", 10))
        customer_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Parts Selection Frame
        parts_frame = tk.LabelFrame(self, text=" Parts Selection ", font=("Arial", 12, "bold"),
                                   bg=self.light_bg, fg=self.secondary_color, padx=10, pady=10)
        parts_frame.grid(row=2, column=0, columnspan=7, padx=10, pady=5, sticky="ew")
        
        # Configure parts frame columns for responsiveness
        for i in range(7):
            parts_frame.grid_columnconfigure(i, weight=1 if i in [1, 3] else 0)
        
        ttk.Label(parts_frame, text="Select Part:", background=self.light_bg, 
                 font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.part_name_dropdown = ttk.Combobox(
            parts_frame, values=list(self.parts_dict.keys()), textvariable=self.part_name_var, 
            state="readonly", font=("Arial", 10)
        )
        self.part_name_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.part_name_dropdown.bind("<<ComboboxSelected>>", self.on_part_name_selected)

        ttk.Label(parts_frame, text="Select Model:", background=self.light_bg, 
                 font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.part_model_dropdown = ttk.Combobox(parts_frame, values=[], textvariable=self.part_model_var, 
                                               state="readonly", font=("Arial", 10))
        self.part_model_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(parts_frame, text="Quantity:", background=self.light_bg, 
                 font=("Arial", 10)).grid(row=0, column=4, padx=5, pady=5, sticky="w")
        ttk.Entry(parts_frame, textvariable=self.qty_var, width=10, font=("Arial", 10)).grid(row=0, column=5, padx=5, pady=5)

        add_btn = tk.Button(parts_frame, text="Add Part", command=self.add_item, bg=self.primary_color, 
                           fg=self.light_text, font=("Arial", 10, "bold"), relief="flat", padx=15, pady=5)
        add_btn.grid(row=0, column=6, padx=5, pady=5)
        
        # Custom Items Frame
        custom_frame = tk.LabelFrame(self, text=" Custom Items ", font=("Arial", 12, "bold"),
                                    bg=self.light_bg, fg=self.secondary_color, padx=10, pady=10)
        custom_frame.grid(row=3, column=0, columnspan=7, padx=10, pady=5, sticky="ew")
        
        # Configure custom frame columns for responsiveness
        for i in range(7):
            custom_frame.grid_columnconfigure(i, weight=1 if i in [1, 3] else 0)
        
        self.custom_name_var = tk.StringVar()
        self.custom_price_var = tk.StringVar()
        self.custom_qty_var = tk.StringVar()

        ttk.Label(custom_frame, text="Item Name:", background=self.light_bg, 
                 font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(custom_frame, textvariable=self.custom_name_var, font=("Arial", 10)).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(custom_frame, text="Price:", background=self.light_bg, 
                 font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(custom_frame, textvariable=self.custom_price_var, font=("Arial", 10)).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(custom_frame, text="Qty:", background=self.light_bg, 
                 font=("Arial", 10)).grid(row=0, column=4, padx=5, pady=5, sticky="w")
        ttk.Entry(custom_frame, textvariable=self.custom_qty_var, width=10, font=("Arial", 10)).grid(row=0, column=5, padx=5, pady=5)

        custom_btn = tk.Button(custom_frame, text="Add Custom", command=self.add_custom_item, bg=self.primary_color, 
                              fg=self.light_text, font=("Arial", 10, "bold"), relief="flat", padx=15, pady=5)
        custom_btn.grid(row=0, column=6, padx=5, pady=5)

        # Bill Items List Frame
        list_frame = tk.LabelFrame(self, text=" Bill Items ", font=("Arial", 12, "bold"),
                                  bg=self.light_bg, fg=self.secondary_color, padx=10, pady=10)
        list_frame.grid(row=4, column=0, columnspan=7, padx=10, pady=10, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        
        # Create style for treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background=self.secondary_color, foreground=self.light_text)
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.map("Treeview.Heading", background=[('active', self.primary_color)])
        
        # Define columns with responsive widths
        self.bill_list = ttk.Treeview(list_frame, columns=("Name", "Model", "Qty", "Price", "Total"), show="headings", height=12)
        
        # Set column headings and initial widths
        columns = [("Name", 200), ("Model", 150), ("Qty", 80), ("Price", 100), ("Total", 120)]
        for col, width in columns:
            self.bill_list.heading(col, text=col)
            self.bill_list.column(col, width=width, anchor="center" if col in ("Qty", "Price", "Total") else "w")

        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.bill_list.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=self.bill_list.xview)
        self.bill_list.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for treeview and scrollbars
        self.bill_list.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Payment Frame
        payment_frame = tk.LabelFrame(self, text=" Payment Details ", font=("Arial", 12, "bold"),
                                     bg=self.light_bg, fg=self.secondary_color, padx=10, pady=10)
        payment_frame.grid(row=5, column=0, columnspan=7, padx=10, pady=5, sticky="ew")
        for i in range(7):
            payment_frame.grid_columnconfigure(i, weight=1)

        self.total_label = tk.Label(payment_frame, text="Total: Rs 0.00", font=("Arial", 14, "bold"), 
                                   fg=self.success_color, bg=self.light_bg)
        self.total_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.cash_var = tk.StringVar()
        ttk.Label(payment_frame, text="Cash Received:", background=self.light_bg, 
                 font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(payment_frame, textvariable=self.cash_var, font=("Arial", 10), width=15).grid(row=0, column=3, padx=5, pady=5)

        calc_btn = tk.Button(payment_frame, text="Calculate Change", command=self.calculate_change, 
                            bg=self.primary_color, fg=self.light_text, font=("Arial", 10, "bold"), 
                            relief="flat", padx=10, pady=5)
        calc_btn.grid(row=0, column=4, padx=5, pady=5)

        self.change_label = tk.Label(payment_frame, text="Change: Rs 0.00", font=("Arial", 14, "bold"), 
                                    fg=self.secondary_color, bg=self.light_bg)
        self.change_label.grid(row=0, column=5, columnspan=2, padx=5, pady=5, sticky="w")

        # Action Buttons Frame
        action_frame = tk.Frame(self, bg=self.light_bg, pady=10)
        action_frame.grid(row=6, column=0, columnspan=7, padx=10, pady=10, sticky="e")
        action_frame.grid_columnconfigure(0, weight=1)
        
        # Create a subframe for buttons to keep them together
        button_frame = tk.Frame(action_frame, bg=self.light_bg)
        button_frame.pack(side="right")
        
        clear_btn = tk.Button(button_frame, text="Clear Bill", command=self.clear_bill, 
                             bg=self.accent_color, fg=self.light_text, font=("Arial", 10, "bold"), 
                             relief="flat", padx=15, pady=5)
        clear_btn.pack(side="left", padx=5)
        
        print_btn = tk.Button(button_frame, text="Print Bill", command=self.print_bill, 
                             bg=self.success_color, fg=self.light_text, font=("Arial", 10, "bold"), 
                             relief="flat", padx=15, pady=5)
        print_btn.pack(side="left", padx=5)
        
        back_btn = tk.Button(button_frame, text="Back to Dashboard", command=self.go_back, 
                            bg=self.secondary_color, fg=self.light_text, font=("Arial", 10, "bold"), 
                            relief="flat", padx=15, pady=5)
        back_btn.pack(side="left", padx=5)

    def on_resize(self, event):
        # Only adjust layout if width has changed significantly
        if abs(event.width - self.current_width) < 50:
            return
            
        self.current_width = event.width
        
        # Responsive adjustments based on window width
        if event.width < 1000:
            # Compact layout for smaller screens
            font_size = 9
            button_padx = 10
            self.bill_list.column("Name", width=150)
            self.bill_list.column("Model", width=100)
        elif event.width < 1200:
            # Medium layout
            font_size = 10
            button_padx = 15
            self.bill_list.column("Name", width=180)
            self.bill_list.column("Model", width=130)
        else:
            # Expanded layout for large screens
            font_size = 10
            button_padx = 20
            self.bill_list.column("Name", width=220)
            self.bill_list.column("Model", width=160)
            
        # Update font sizes for better readability
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", font_size))
        
        # Update button sizes
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(padx=button_padx)

    def on_part_name_selected(self, event):
        models = [model for _, model, _ in self.parts_dict.get(self.part_name_var.get(), [])]
        self.part_model_var.set('')
        self.part_model_dropdown['values'] = models

    def add_item(self):
        try:
            part_name = self.part_name_var.get()
            part_model = self.part_model_var.get().strip()
            qty = int(self.qty_var.get())
            if not part_name or qty <= 0:
                messagebox.showerror("Error", "Please select part and enter valid quantity")
                return

            parts = self.parts_dict.get(part_name, [])
            if part_model:
                match = next(((pid, model, price) for pid, model, price in parts if model == part_model), None)
                if not match:
                    messagebox.showerror("Error", "Model not found")
                    return
            else:
                match = (parts[0][0], parts[0][1], parts[0][2])
                part_model = match[1]

            part_id, _, price = match

            # 🔹 Check stock before selling
            current_stock = init_db.get_part_quantity(part_id)
            if current_stock is None:
                messagebox.showerror("Error", "Part not found in database")
                return
            if qty > current_stock:
                messagebox.showerror("Error", f"Not enough stock! Available: {current_stock}")
                return

            total = price * qty
            self.bill_items.append((part_name, part_model, qty, price, total))
            self.total_amount += total

            self.bill_list.insert("", "end", values=(part_name, part_model, qty, f"{price:.2f}", f"{total:.2f}"))
            self.total_label.config(text=f"Total: Rs {self.total_amount:.2f}")

            # 🔹 Save sale + update stock
            user = init_db.get_last_logged_user() or "Unknown"
            init_db.insert_sale(part_id, part_name, qty, price, user)
            init_db.update_part_quantity(part_id, current_stock - qty)

            # Clear input fields
            self.qty_var.set("")

        except ValueError:
            messagebox.showerror("Error", "Invalid quantity")

    def add_custom_item(self):
        try:
            name = self.custom_name_var.get().strip()
            price = float(self.custom_price_var.get())
            qty = int(self.custom_qty_var.get())
            if not name or price <= 0 or qty <= 0:
                messagebox.showerror("Error", "Enter valid custom item")
                return

            total = price * qty
            self.bill_items.append((name, "", qty, price, total))
            self.total_amount += total

            self.bill_list.insert("", "end", values=(name, "", qty, f"{price:.2f}", f"{total:.2f}"))
            self.total_label.config(text=f"Total: Rs {self.total_amount:.2f}")
            
            # Clear input fields
            self.custom_name_var.set("")
            self.custom_price_var.set("")
            self.custom_qty_var.set("")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid custom item details")

    def calculate_change(self):
        try:
            cash = float(self.cash_var.get())
            change = cash - self.total_amount
            if change < 0:
                self.change_label.config(text=f"Change: Rs {change:.2f} (Insufficient!)", fg=self.accent_color)
            else:
                self.change_label.config(text=f"Change: Rs {change:.2f}", fg=self.success_color)
        except ValueError:
            messagebox.showerror("Error", "Invalid cash amount")

    def clear_bill(self):
        for item in self.bill_list.get_children():
            self.bill_list.delete(item)
        self.bill_items.clear()
        self.total_amount = 0.0
        self.total_label.config(text="Total: Rs 0.00")
        self.change_label.config(text="Change: Rs 0.00", fg=self.secondary_color)
        self.cash_var.set("")
        self.customer_number_var.set("")

    def print_bill(self):
        customer_num = self.customer_number_var.get().strip()
        if not customer_num:
            messagebox.showerror("Error", "Enter customer number")
            return
        if not self.bill_items:
            messagebox.showerror("Error", "Bill is empty")
            return
        try:
            cash = float(self.cash_var.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid cash amount")
            return

        change = cash - self.total_amount
        print_or_save_bill(customer_num, self.bill_items, self.total_amount, cash, change)
        
        # Show success message
        messagebox.showinfo("Success", "Bill printed successfully!")
        
        # Clear the bill after printing
        self.clear_bill()

    def go_back(self):
        if self.show_frame_callback:
            self.show_frame_callback("user_dashboard")
        else:
            messagebox.showinfo("Back", "No callback set")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Billing System")
    root.geometry("1200x800")  # Default size for desktop
    root.minsize(900, 600)     # Minimum size to maintain usability
    root.state('zoomed')       # Start maximized on desktop
    app = BillingSystem(root)
    app.pack(fill="both", expand=True)
    root.mainloop()