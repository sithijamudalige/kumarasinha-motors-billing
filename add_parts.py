import tkinter as tk
from tkinter import messagebox
from db_parts import insert_part

class AddParts(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame

        tk.Label(self, text="Add New Part", font=("Arial", 16)).pack(pady=10)

        self.entries = {}

        # Field definitions: (Label Text, Dictionary Key)
        fields = [
            ("Part Name", "part_name"),
            ("Part Model", "part_model"),
            ("Part Size", "part_size"),         # Accepts any value like '500ml', 'custom'
            ("Buy Price", "buy_price"),         # Must be float
            ("Quantity", "quantity"),           # Must be integer
            ("Selling Price", "selling_price")  # Must be float
        ]

        # Create form fields dynamically
        for label_text, field_key in fields:
            tk.Label(self, text=label_text).pack()
            entry = tk.Entry(self)
            entry.pack(pady=2)
            self.entries[field_key] = entry

        # Buttons
        tk.Button(self, text="Add Part", command=self.save_part).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: switch_frame("Parts_management")).pack(pady=5)

    def save_part(self):
        try:
            # Get values from form
            part_name = self.entries["part_name"].get().strip()
            part_model = self.entries["part_model"].get().strip()
            part_size = self.entries["part_size"].get().strip()
            buy_price = float(self.entries["buy_price"].get())
            quantity = int(self.entries["quantity"].get())
            selling_price = float(self.entries["selling_price"].get())

            # Prepare tuple for DB
            data = (part_name, part_model, part_size, buy_price, quantity, selling_price)

            # Insert into DB
            insert_part(data)

            # Success message
            messagebox.showinfo("Success", "Part added successfully!")

            # Clear all fields
            for entry in self.entries.values():
                entry.delete(0, tk.END)

            # Switch back to parts management screen
            self.switch_frame("Parts_management")

        except ValueError:
            messagebox.showerror("Input Error", "Buy price, quantity, and selling price must be valid numbers.")
        except Exception as e:
            messagebox.showerror("Unexpected Error", str(e))
