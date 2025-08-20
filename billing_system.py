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
        self.create_widgets()

    def create_widgets(self):
        parts = init_db.get_all_parts()
        self.parts_dict = {}
        for part_id, name, model, price in parts:
            self.parts_dict.setdefault(name, []).append((part_id, model, price))

        self.customer_number_var = tk.StringVar()
        self.part_name_var = tk.StringVar()
        self.part_model_var = tk.StringVar()
        self.qty_var = tk.StringVar()

        ttk.Label(self, text="Customer Number:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.customer_number_var).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self, text="Select Part:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.part_name_dropdown = ttk.Combobox(
            self, values=list(self.parts_dict.keys()), textvariable=self.part_name_var, state="readonly"
        )
        self.part_name_dropdown.grid(row=1, column=1, padx=5, pady=5)
        self.part_name_dropdown.bind("<<ComboboxSelected>>", self.on_part_name_selected)

        ttk.Label(self, text="Select Model (optional):").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.part_model_dropdown = ttk.Combobox(self, values=[], textvariable=self.part_model_var, state="normal")
        self.part_model_dropdown.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(self, text="Quantity:").grid(row=1, column=4, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.qty_var, width=10).grid(row=1, column=5, padx=5, pady=5)

        ttk.Button(self, text="Add", command=self.add_item).grid(row=1, column=6, padx=5, pady=5)

        self.custom_name_var = tk.StringVar()
        self.custom_price_var = tk.StringVar()
        self.custom_qty_var = tk.StringVar()

        ttk.Label(self, text="Custom Name:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.custom_name_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Price:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.custom_price_var).grid(row=2, column=3, padx=5, pady=5)

        ttk.Label(self, text="Qty:").grid(row=2, column=4, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.custom_qty_var, width=10).grid(row=2, column=5, padx=5, pady=5)

        ttk.Button(self, text="Add Custom", command=self.add_custom_item).grid(row=2, column=6, padx=5, pady=5)

        self.bill_list = ttk.Treeview(self, columns=("Name", "Model", "Qty", "Price", "Total"), show="headings")
        for col in ("Name", "Model", "Qty", "Price", "Total"):
            self.bill_list.heading(col, text=col)
            self.bill_list.column(col, width=150 if col in ("Name", "Model") else 80, anchor="w")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.bill_list.yview)
        self.bill_list.configure(yscrollcommand=self.scrollbar.set)
        self.bill_list.grid(row=3, column=0, columnspan=6, padx=5, pady=10, sticky="nsew")
        self.scrollbar.grid(row=3, column=6, sticky="ns", pady=10)

        ttk.Button(self, text="Clear Bill", command=self.clear_bill).grid(row=4, column=4, padx=5, pady=5, sticky="e")
        ttk.Button(self, text="Print", command=self.print_bill).grid(row=4, column=5, padx=5, pady=5, sticky="e")
        ttk.Button(self, text="Back", command=self.go_back).grid(row=4, column=6, padx=5, pady=5, sticky="e")

        self.total_label = ttk.Label(self, text="Total: Rs 0.00", font=("Arial", 14))
        self.total_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.cash_var = tk.StringVar()
        ttk.Label(self, text="Cash:").grid(row=5, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.cash_var).grid(row=5, column=3, padx=5, pady=5)
        ttk.Button(self, text="Calculate Change", command=self.calculate_change).grid(row=5, column=4, padx=5, pady=5)

        self.change_label = ttk.Label(self, text="Change: Rs 0.00", font=("Arial", 14))
        self.change_label.grid(row=5, column=5, padx=5, pady=5, sticky="w")

        for i in range(7):
            self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(3, weight=1)

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
        except ValueError:
            messagebox.showerror("Error", "Invalid custom item details")

    def calculate_change(self):
        try:
            cash = float(self.cash_var.get())
            change = cash - self.total_amount
            self.change_label.config(text=f"Change: Rs {change:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Invalid cash amount")

    def clear_bill(self):
        for item in self.bill_list.get_children():
            self.bill_list.delete(item)
        self.bill_items.clear()
        self.total_amount = 0.0
        self.total_label.config(text="Total: Rs 0.00")
        self.change_label.config(text="Change: Rs 0.00")
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

    def go_back(self):
        if self.show_frame_callback:
            self.show_frame_callback("user_dashboard")
        else:
            messagebox.showinfo("Back", "No callback set")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Billing System")
    root.geometry("900x600")
    root.minsize(800, 500)
    app = BillingSystem(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
