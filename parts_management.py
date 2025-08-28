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

        tk.Label(
            header_frame, text="Parts Management", font=("Segoe UI", 18, "bold"),
            bg='#3a7ca5', fg='white'
        ).pack(side='left', padx=25, pady=20)

        # Navigation buttons
        nav_frame = tk.Frame(header_frame, bg='#3a7ca5')
        nav_frame.pack(side='right', padx=20)

        tk.Button(
            nav_frame, text="Back to Admin", command=lambda: switch_frame("admin_dashboard"),
            bg='#5c9ead', fg='white', font=("Segoe UI", 9, "bold"), width=15, height=1,
            relief='flat', cursor='hand2', activebackground='#4a8c9d'
        ).pack(side='right', padx=5)

        tk.Button(
            nav_frame, text="Add New Part", command=lambda: switch_frame("add_parts"),
            bg='#2a9d8f', fg='white', font=("Segoe UI", 9, "bold"), width=12, height=1,
            relief='flat', cursor='hand2', activebackground='#21867a'
        ).pack(side='right', padx=5)

        # Search and filter section
        filter_frame = tk.Frame(self, bg='#f8f9fa', padx=20, pady=10)
        filter_frame.pack(fill='x', pady=(0, 10))

        search_container = tk.Frame(filter_frame, bg='#f8f9fa')
        search_container.pack(side='left')

        tk.Label(
            search_container, text="Search Parts:", font=("Segoe UI", 10, "bold"),
            bg='#f8f9fa', fg='#495057'
        ).pack(anchor='w')

        search_box = tk.Frame(search_container, bg='#dee2e6', padx=2, pady=2)
        search_box.pack(pady=(5, 0))

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_box, textvariable=self.search_var, width=30,
            font=("Segoe UI", 10), relief='flat', bg='white'
        )
        search_entry.pack(side='left')
        search_entry.bind('<KeyRelease>', self.filter_parts)

        search_icon = tk.Label(search_box, text="🔍", bg='#dee2e6', font=("Segoe UI", 10))
        search_icon.pack(side='left', padx=(5, 5))

        tk.Button(
            filter_frame, text="Clear Filters", command=self.clear_filter,
            bg='#6c757d', fg='white', font=("Segoe UI", 9), width=12, relief='flat',
            cursor='hand2', activebackground='#5a6268'
        ).pack(side='right', padx=5)

        # Stats summary
        self.summary_frame = tk.Frame(self, bg='#e9ecef', height=60)
        self.summary_frame.pack(fill='x', padx=20, pady=(0, 15))
        self.summary_frame.pack_propagate(False)
        self.update_summary()

        # Parts table frame
        table_container = tk.Frame(
            self, bg='#ffffff', relief='flat', highlightthickness=1,
            highlightbackground='#ced4da'
        )
        table_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Create a treeview widget for the table
        columns = (
            "id", "name", "model", "size", "buy_price", "quantity", "total_value",
            "sell_price", "add_date", "add_time", "update_date", "update_time", "actions"
        )

        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=15)

        # Define column headings and widths
        headings = [
            "ID", "Name", "Model", "Size", "Buy Price", "Qty", "Total Value",
            "Sell Price", "Add Date", "Add Time", "Update Date", "Update Time", "Actions"
        ]
        widths = [40, 150, 120, 80, 80, 60, 100, 80, 100, 80, 100, 80, 120]

        for col, heading, width in zip(columns, headings, widths):
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor='center')

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)

        # Ensure button frames move on scroll
        def _on_yscroll(first, last):
            scrollbar.set(first, last)
            self.update_button_positions()

        self.tree.configure(yscrollcommand=_on_yscroll)

        # Pack tree and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Move buttons when the tree is resized or scrolled
        self.tree.bind("<Configure>", self.update_button_positions)
        self.tree.bind("<ButtonRelease-1>", self.update_button_positions)
        self.tree.bind("<Motion>", self.update_button_positions)
        self.tree.bind("<MouseWheel>", self.update_button_positions)  # Windows/macOS
        self.tree.bind("<Button-4>", self.update_button_positions)    # Linux scroll up
        self.tree.bind("<Button-5>", self.update_button_positions)    # Linux scroll down

        # Store part data separately
        self.part_data = {}
        self.action_buttons = {}  # item_id -> {"frame": Frame, "buttons": [btns...]}

        # Initialize parts display
        self.display_parts()

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

            tk.Label(
                stat_frame, text=label, font=("Segoe UI", 9),
                bg='#e9ecef', fg='#6c757d'
            ).pack(pady=(10, 0))
            tk.Label(
                stat_frame, text=value, font=("Segoe UI", 14, "bold"),
                bg='#e9ecef', fg=color
            ).pack(pady=(0, 10))

    def filter_parts(self, event=None):
        search_term = self.search_var.get().lower().strip()

        # Reattach all known items first
        for item in list(self.part_data.keys()):
            try:
                self.tree.reattach(item, '', 'end')
            except Exception:
                pass

        # If no search, just refresh positions
        if not search_term:
            self.update_button_positions()
            return

        # Hide items that don't match
        for item, part in self.part_data.items():
            match_found = any(search_term in str(value).lower() for value in part if value is not None)
            if not match_found:
                try:
                    self.tree.detach(item)
                except Exception:
                    pass
                widgets = self.action_buttons.get(item)
                if widgets:
                    widgets["frame"].place_forget()

        # Reposition frames for visible rows
        self.update_button_positions()

    def clear_filter(self):
        self.search_var.set("")
        for item in list(self.part_data.keys()):
            try:
                self.tree.reattach(item, '', 'end')
            except Exception:
                pass
        self.update_button_positions()

    def display_parts(self):
        # Clear existing items and data
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.part_data.clear()

        # Remove all action button frames
        for widgets in self.action_buttons.values():
            try:
                widgets["frame"].destroy()
            except Exception:
                pass
        self.action_buttons.clear()

        parts = get_all_parts()

        if not parts:
            # Create a placeholder if no parts exist
            self.tree.insert("", "end", values=("No parts found", "", "", "", "", "", "", "", "", "", "", "", ""))
            # Update summary even if empty
            self.update_summary()
            return

        for part in parts:
            # Format values for display
            formatted_values = []
            for i, value in enumerate(part):
                if i in [4, 6, 7]:  # Format currency fields
                    try:
                        formatted_values.append(f"${float(value):.2f}" if value else "$0.00")
                    except (ValueError, TypeError):
                        formatted_values.append("$0.00")
                else:
                    formatted_values.append(str(value) if value else "")

            # Add empty string for actions column
            formatted_values.append("")

            # Insert into treeview
            item_id = self.tree.insert("", "end", values=formatted_values)

            # Store the original part data separately
            self.part_data[item_id] = part

            # Set tag for row coloring based on quantity
            qty = part[5] if part[5] else 0
            try:
                qty_int = int(qty)
            except (ValueError, TypeError):
                qty_int = 0

            if qty_int == 0:
                self.tree.item(item_id, tags=("out_of_stock",))
            elif qty_int < 5:
                self.tree.item(item_id, tags=("low_stock",))

        # Configure tag colors
        self.tree.tag_configure("out_of_stock", background="#ffeaea")
        self.tree.tag_configure("low_stock", background="#fff3cd")

        # Add action buttons to each row
        self.add_action_buttons()

        # Update summary after displaying parts
        self.update_summary()

    def add_action_buttons(self):
        # Add small frame with buttons, overlaid on "actions" column
        for item in self.tree.get_children():
            part = self.part_data.get(item)
            if not part:
                continue

            # Use a fixed background (avoid ttk cget background)
            btn_frame = tk.Frame(self.tree, bg="#ffffff", bd=0, highlightthickness=0)

            edit_btn = tk.Button(
                btn_frame, text="Edit",
                command=lambda p=part: self.edit_part(p),
                bg='#5c9ead', fg='white', font=("Segoe UI", 8, "bold"),
                width=4, relief='flat', cursor='hand2', activebackground='#4a8c9d'
            )

            qty_btn = tk.Button(
                btn_frame, text="Qty",
                command=lambda p=part: self.update_part_quantity(p),
                bg='#f4a261', fg='white', font=("Segoe UI", 8, "bold"),
                width=4, relief='flat', cursor='hand2', activebackground='#e76f51'
            )

            del_btn = tk.Button(
                btn_frame, text="Del",
                command=lambda p=part: self.remove_part(p),
                bg='#e76f51', fg='white', font=("Segoe UI", 8, "bold"),
                width=4, relief='flat', cursor='hand2', activebackground='#d6543a'
            )

            edit_btn.pack(side='left', padx=1)
            qty_btn.pack(side='left', padx=1)
            del_btn.pack(side='left', padx=1)

            # Store both frame and buttons
            self.action_buttons[item] = {"frame": btn_frame, "buttons": [edit_btn, qty_btn, del_btn]}

            # Position the frame after initial render
            def position_buttons(i=item, f=btn_frame):
                bbox = self.tree.bbox(i, "actions")
                if bbox:
                    f.place(in_=self.tree, x=bbox[0] + 2, y=bbox[1] + 2,
                            width=bbox[2] - 4, height=bbox[3] - 4)
            self.after(100, position_buttons)

        # Ensure we do one more pass to correct positions
        self.after(200, self.update_button_positions)

    def update_button_positions(self, event=None):
        # Reposition or hide frames based on whether item is visible
        for item, widgets in list(self.action_buttons.items()):
            frame = widgets.get("frame")
            if not frame:
                continue
            bbox = self.tree.bbox(item, "actions")
            if bbox:
                frame.place(in_=self.tree, x=bbox[0] + 2, y=bbox[1] + 2,
                            width=bbox[2] - 4, height=bbox[3] - 4)
            else:
                frame.place_forget()

    def remove_part(self, part):
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete part '{part[1]}'?",
            icon='warning'
        )
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

        qty = simpledialog.askinteger(
            "Update Quantity",
            f"Current quantity for '{part[1]}': {current_qty_int}\n\nEnter new quantity to add:",
            minvalue=0, initialvalue=0
        )
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

        tk.Label(
            header, text=f"Edit Part: {part[1]}", font=("Segoe UI", 14, "bold"),
            bg='#3a7ca5', fg='white'
        ).pack(pady=20)

        # Main frame
        main_frame = tk.Frame(edit_win, bg='#f8f9fa', padx=25, pady=20)
        main_frame.pack(fill='both', expand=True)

        entries = []
        labels = ["Name", "Model", "Size", "Buy Price", "Sell Price"]
        defaults = [part[1], part[2], part[3], str(part[4]), str(part[7])]

        for i, label in enumerate(labels):
            field_frame = tk.Frame(main_frame, bg='#f8f9fa')
            field_frame.pack(fill='x', pady=10)

            tk.Label(
                field_frame, text=label, width=12, anchor='w',
                font=("Segoe UI", 10, "bold"), bg='#f8f9fa', fg='#495057'
            ).pack(side='left')

            e = tk.Entry(
                field_frame, font=("Segoe UI", 10), relief='flat',
                bg='white', highlightthickness=1, highlightcolor='#3a7ca5',
                highlightbackground='#ced4da'
            )
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

        tk.Button(
            button_frame, text="Save Changes", command=save_changes,
            bg='#2a9d8f', fg='white', font=("Segoe UI", 10, "bold"), width=15,
            relief='flat', cursor='hand2', activebackground='#21867a', padx=10, pady=6
        ).pack(side='left', padx=10)

        tk.Button(
            button_frame, text="Cancel", command=edit_win.destroy,
            bg='#6c757d', fg='white', font=("Segoe UI", 10), width=10,
            relief='flat', cursor='hand2', activebackground='#5a6268', padx=10, pady=6
        ).pack(side='left', padx=10)