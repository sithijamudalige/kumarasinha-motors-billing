# main.py
import tkinter as tk
import traceback
import sys
import init_db

from welcome import WelcomeScreen
from login import LoginScreen
from signup import SignUpScreen
from user_dashboard import UserDashboard
from adminlogin import AdminLoginScreen 
from admin_dashboard import AdminDashboard
from user_management import UserManagement
from parts_management import PartsManagement
from add_parts import AddParts
from billing_system import BillingSystem 
from inventory_creation import InventoryCreation
from view_reports import ViewReports
from view_parts_table import ViewPartsTable
from view_login_history import ViewLoginHistory
from view_sales_history import ViewSalesHistory
# from dashboard import UserDashboard  # Uncomment if you create this later

class POSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("POS Login System")
        self.logged_user = None
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.6)
        

        self.geometry(f"{window_width}x{window_height}")
        self.resizable(True, True)  # Enable resizing if needed

        self.current_frame = None
        self.show_frame("welcome")
        self.current_frame.pack(fill="both", expand=True)
    def show_frame(self, screen_name, user=None):
        # Destroy current frame
        if self.current_frame:
            self.current_frame.destroy()
        if user:
           self.logged_user = user
    
        if screen_name == "user_dashboard":
            if user is None:
                # get last logged-in user from DB
                user = init_db.get_last_logged_user()
                self.current_user = user
            else:
                self.current_user = user
            self.current_frame = UserDashboard(self, self.show_frame, user)
        elif screen_name == "billing_system":
            self.current_frame = BillingSystem(self, self.show_frame)

        # Decide which screen to show
        if screen_name == "welcome":
            self.current_frame = WelcomeScreen(self, self.show_frame)
        elif screen_name == "login":
            self.current_frame = LoginScreen(self, self.show_frame)
        elif screen_name == "signup":
            self.current_frame = SignUpScreen(self, self.show_frame)
        elif screen_name == "user_dashboard":
         self.current_frame = UserDashboard(self, self.show_frame, user)
        elif screen_name == "adminlogin":
          self.current_frame = AdminLoginScreen(self, self.show_frame)  
        elif screen_name == "admin_dashboard":
          self.current_frame = AdminDashboard(self, self.show_frame,user)
        elif screen_name == "user_management":
          self.current_frame = UserManagement(self, self.show_frame)
        elif screen_name == "Parts_management":
           self.current_frame=PartsManagement(self,self.show_frame)
        elif screen_name=="add_parts":
           self.current_frame=AddParts(self,self.show_frame) 
        elif screen_name=="billing_system":
           self.current_frame=BillingSystem(self,self.show_frame)
        elif screen_name=="inventory_creation":
           self.current_frame=InventoryCreation(self,self.show_frame) 
        elif screen_name=="view_reports":
           self.current_frame=ViewReports(self,self.show_frame)      
        elif screen_name=="view_parts_table":
           self.current_frame=ViewPartsTable(self,self.show_frame)
        elif screen_name=="view_login_history":
           self.current_frame=ViewLoginHistory(self,self.show_frame)   
        elif screen_name=="view_sales_history":
           self.current_frame=ViewSalesHistory(self,self.show_frame)

        self.current_frame.pack(fill="both", expand=True)

def log_exception(exc_type, exc_value, exc_traceback):
    with open("error_log.txt", "a") as f:
        f.write("=== Exception Occurred ===\n")
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
sys.excepthook = log_exception
if __name__ == "__main__":
    app = POSApp()
    app.mainloop()
