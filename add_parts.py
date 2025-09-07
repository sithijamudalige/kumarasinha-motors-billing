import tkinter as tk
from tkinter import messagebox, ttk
from db_parts import insert_part

class AddParts(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame
        self.configure(bg='#f5f7fa')  # Light blue-gray background
        
        # Create a main container with padding
        main_container = tk.Frame(self, bg='#f5f7fa', padx=25, pady=25)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(main_container, bg='#f5f7fa')
        header.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(header, text="Add New Part", font=("Arial", 20, "bold"), 
                bg='#f5f7fa', fg='#2c3e50').pack(pady=10)
        
        # Form container with a subtle border and shadow effect
        form_container = tk.Frame(main_container, bg='white', relief=tk.RAISED, bd=2)
        form_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a canvas and scrollbar for the form
        canvas = tk.Canvas(form_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white', padx=20, pady=20)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.entries = {}
        
        # Field definitions: (Label Text, Dictionary Key, is_required)
        fields = [
            ("Part Name *", "part_name", True),
            ("Part Model *", "part_model", True),
            ("Part Size", "part_size", False),         # Can be empty
            ("Buy Price *", "buy_price", True),        # Must be float
            ("Quantity *", "quantity", True),          # Must be integer
            ("Selling Price *", "selling_price", True) # Must be float
        ]
        
        # Create form fields dynamically with better styling
        for i, (label_text, field_key, is_required) in enumerate(fields):
            field_frame = tk.Frame(scrollable_frame, bg='white', pady=10)
            field_frame.pack(fill=tk.X, padx=20, pady=8)
            
            # Create label with asterisk for required fields
            label = tk.Label(field_frame, text=label_text, font=("Arial", 11), 
                            bg='white', fg='#34495e', anchor='w')
            label.pack(fill=tk.X)
            
            # Add special formatting for numeric fields
            if field_key in ['buy_price', 'selling_price']:
                entry_frame = tk.Frame(field_frame, bg='white')
                entry_frame.pack(fill=tk.X, pady=(5, 0))
                
                # Add a dollar sign prefix for price fields
                prefix = tk.Frame(entry_frame, width=30, height=36, bg='#ecf0f1')
                prefix.pack_propagate(False)
                prefix.pack(side=tk.LEFT)
                tk.Label(prefix, text="LKR ", bg='#ecf0f1', fg='#7f8c8d', 
                        font=("Arial", 12)).place(relx=0.5, rely=0.5, anchor='center')
                
                entry = tk.Entry(entry_frame, font=("Arial", 11), relief=tk.FLAT, 
                                bg='#f8f9fa', fg='#2c3e50', highlightthickness=1,
                                highlightcolor='#3498db', highlightbackground='#e0e0e0')
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
                
            elif field_key == 'quantity':
                entry = tk.Entry(field_frame, font=("Arial", 11), relief=tk.FLAT, 
                                bg='#f8f9fa', fg='#2c3e50', highlightthickness=1,
                                highlightcolor='#3498db', highlightbackground='#e0e0e0')
                entry.pack(fill=tk.X, pady=(5, 0), ipady=5)
                
            else:
                entry = tk.Entry(field_frame, font=("Arial", 11), relief=tk.FLAT, 
                                bg='#f8f9fa', fg='#2c3e50', highlightthickness=1,
                                highlightcolor='#3498db', highlightbackground='#e0e0e0')
                entry.pack(fill=tk.X, pady=(5, 0), ipady=5)
                
            self.entries[field_key] = entry
            
            # Add a subtle separator between fields
            if i < len(fields) - 1:
                sep = tk.Frame(scrollable_frame, height=1, bg='#eaeaea')
                sep.pack(fill=tk.X, padx=20, pady=5)
        
        # Add note about optional field
        note_frame = tk.Frame(scrollable_frame, bg='white')
        note_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        tk.Label(note_frame, text="* Required field", font=("Arial", 9), 
                bg='white', fg='#7f8c8d', anchor='w').pack(fill=tk.X)
        tk.Label(note_frame, text="Part Size can be left empty", font=("Arial", 9), 
                bg='white', fg='#7f8c8d', anchor='w').pack(fill=tk.X)
        
        # Button container
        button_frame = tk.Frame(main_container, bg='#f5f7fa', pady=20)
        button_frame.pack(fill=tk.X)
        
        # Style for buttons
        style = ttk.Style()
        style.configure('Primary.TButton', font=('Arial', 11, 'bold'), 
                        padding=10, background='#3498db', foreground='white')
        style.configure('Secondary.TButton', font=('Arial', 11), 
                        padding=10, background='#95a5a6', foreground='white')
        
        # Buttons with better styling
        ttk.Button(button_frame, text="Add Part", command=self.save_part, 
                  style='Primary.TButton').pack(side=tk.RIGHT, padx=10)
        ttk.Button(button_frame, text="Back", 
                  command=lambda: switch_frame("Parts_management"),
                  style='Secondary.TButton').pack(side=tk.RIGHT)
        
        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Set focus to first field
        self.after(100, lambda: self.entries["part_name"].focus_set())

    def save_part(self):
        try:
            # Get values from form
            part_name = self.entries["part_name"].get().strip()
            part_model = self.entries["part_model"].get().strip()
            part_size = self.entries["part_size"].get().strip()  # Can be empty
            buy_price = float(self.entries["buy_price"].get())
            quantity = int(self.entries["quantity"].get())
            selling_price = float(self.entries["selling_price"].get())

            # Validate required inputs
            if not part_name:
                messagebox.showerror("Input Error", "Part Name is required.")
                self.entries["part_name"].focus_set()
                return
                
            if not part_model:
                messagebox.showerror("Input Error", "Part Model is required.")
                self.entries["part_model"].focus_set()
                return
                
            if buy_price <= 0:
                messagebox.showerror("Input Error", "Buy Price must be positive.")
                self.entries["buy_price"].focus_set()
                return
                
            if quantity < 0:
                messagebox.showerror("Input Error", "Quantity cannot be negative.")
                self.entries["quantity"].focus_set()
                return
                
            if selling_price <= 0:
                messagebox.showerror("Input Error", "Selling Price must be positive.")
                self.entries["selling_price"].focus_set()
                return

            # Prepare tuple for DB (part_size can be empty)
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
            messagebox.showerror("Database Error", f"Failed to add part: {str(e)}")
