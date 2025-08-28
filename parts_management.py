# parts_management.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from db_parts import get_all_parts, delete_part, update_quantity, update_part

class PartsManagement(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame

        tk.Label(self, text="Parts Management", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Back to Admin Dashboard", command=lambda: switch_frame("admin_dashboard")).pack(pady=10)
        tk.Button(self, text="Add Parts", command=lambda: switch_frame("add_parts")).pack(pady=10)

        self.parts_frame = tk.Frame(self)
        self.parts_frame.pack(pady=10)

        self.display_parts()

    def display_parts(self):
        for widget in self.parts_frame.winfo_children():
            widget.destroy()

        parts = get_all_parts()

        headers = ["ID", "Name", "Model", "Size", "Buy", "Qty", "Total", "Sell", "Add Date", "Add Time", "Upd Date", "Upd Time"]
        header = tk.Frame(self.parts_frame)
        header.pack()
        for col in headers:
            tk.Label(header, text=col, width=10, borderwidth=1, relief="solid").pack(side="left")

        for part in parts:
            row = tk.Frame(self.parts_frame)
            row.pack(pady=2)

            for val in part:
                tk.Label(row, text=val, width=10).pack(side="left")

            tk.Button(row, text="Edit", command=lambda p=part: self.edit_part(p)).pack(side="left")
            tk.Button(row, text="Qty", command=lambda p=part: self.update_part_quantity(p)).pack(side="left")
            tk.Button(row, text="Del", command=lambda p=part: self.remove_part(p)).pack(side="left")

    def remove_part(self, part):
        confirm = messagebox.askyesno("Confirm Delete", f"Delete part '{part[1]}'?")
        if confirm:
            delete_part(part[0])
            self.display_parts()

    def update_part_quantity(self, part):
        qty = simpledialog.askinteger("Update Quantity", f"Enter new quantity to add for {part[1]}")
        if qty is not None:
            update_quantity(part[0], qty)
            self.display_parts()

    def edit_part(self, part):
        edit_win = tk.Toplevel(self)
        edit_win.title("Edit Part")

        entries = []
        labels = ["Name", "Model", "Size", "Buy Price", "Sell Price"]
        defaults = [part[1], part[2], part[3], str(part[4]), str(part[7])]

        for i, label in enumerate(labels):
            tk.Label(edit_win, text=label).pack()
            e = tk.Entry(edit_win)
            e.insert(0, defaults[i])
            e.pack()
            entries.append(e)

        def save():
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
                messagebox.showerror("Error", "Buy Price and Sell Price must be numbers.")
                return

            update_part(part[0], updated_data)
            edit_win.destroy()
            self.display_parts()

        tk.Button(edit_win, text="Save", command=save).pack(pady=10)
