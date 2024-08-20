import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db import Database
from manager import UserManager, InventoryManager
from fpdf import FPDF, XPos, YPos
import os
import re
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

class InventoryApp:
    def __init__(self, root):
        self.db = Database()
        self.user_manager = UserManager(self.db)
        self.inventory_manager = InventoryManager(self.db)
        self.root = root
        self.root.state("zoomed")
        self.root.title("Inventory Management System")
        root.configure(background='#d9d9d9')
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview",background= "#ffffff", foreground = "black", rowheight= 25, fieldbackground="#ffffff")
        self.style.map("Treeview",background=[("selected","#6a1b9a")])
        self.sku_pattern = re.compile(r'^\d+$')  # SKU must be non-negative integers
        self.price_pattern = re.compile(r'^[+]?\d*\.?\d+$')  # Price must be positive float
        self.quantity_pattern = re.compile(r'^[+]?\d+$')  # Quantity must be positive integers
        self.item_name_pattern = re.compile(r'^[\w\s\-\(\)\[\]\{\}\.,\'"]+$')  # Item name can be alphabetic with special character

        self.flag = 0

        self.create_login_window()
    
    def create_login_window(self):
        self.login_frame = tk.Frame(self.root, bg="#d9d9d9", bd=40)
        self.login_frame.pack(pady=(120), anchor=tk.CENTER)

        tk.Label(self.login_frame, text="WELCOME", fg="#333333", bg="#d9d9d9", font=("Arial", 30, "bold")).pack(pady=(10))

        tk.Label(self.login_frame, text="Username", font=("Arial", 12), fg="#333333", bg="#d9d9d9").pack()
        self.entry_username = tk.Entry(self.login_frame, width=25, font=("Arial", 12), bg="#e0e0e0")
        self.entry_username.pack(pady=(10), ipady=3)

        tk.Label(self.login_frame, text="Password", font=("Arial", 12), fg="#333333", bg="#d9d9d9").pack()
        self.entry_password = tk.Entry(self.login_frame, show='●', width=25, font=("Arial", 12), bg="#e0e0e0")
        self.entry_password.pack(pady=(10), ipady=3)

        tk.Button(self.login_frame, text="Login",command=self.login, fg="#ffffff", bg="#6a1b9a", font=("Arial", 12), width=25, height=1, borderwidth=0).pack(pady=10)
        self.root.bind('<Return>', self.login)


    def login(self, event=None):
        username = self.entry_username.get()
        password = self.entry_password.get()
        self.user = self.user_manager.validate_user(username, password)

        if self.user:
            self.user_id = self.user[0]  
            self.user_name = self.user[1]
            self.user_manager.update_user_active_status(self.user_id, active=1)
            self.user_role = self.user[3] 
            if self.user[3]=="user":
                self.login_frame.destroy()
                InventoryApp_User(self.root,self.user_id,self.user_role)
            if self.user[3]=="admin":
                self.create_inventory_window(self.user_id)
        else:
            messagebox.showerror("Login", "Invalid username or password.")


    def validate_sku(self, sku):
        return bool(self.sku_pattern.match(sku))

    def validate_price(self, price):
        return bool(self.price_pattern.match(price)) and float(price) > 0

    def validate_quantity(self, quantity):
        return bool(self.quantity_pattern.match(quantity)) and int(quantity) >= 0

    def validate_item_name(self, name):
        return bool(self.item_name_pattern.match(name))
    
    def validate_sku_input(self, input_text):
        if input_text == ""  or (input_text.isdigit() and len(input_text) <= 5):
            return True
        return False
    
    def create_inventory_window(self,user_id):
        self.login_frame.destroy()
        self.user_id = user_id

        self.inventory_frame = ttk.Frame(self.root)
        self.inventory_frame.pack(expand=True, fill="both")

        side_bar = tk.Frame(self.inventory_frame, bg="#6a1b9a")
        side_bar.grid(column=0, sticky="ns")
        tk.Label(side_bar,text="", font=("Arial", 15),bg="#6a1b9a").grid(pady=80,sticky="w")
        self.add_user_button = tk.Button(side_bar, text="Add User", command=self.add_employees, fg="#ffffff", bg="#6a1b9a", font=("Arial", 15), width=10, height=1, borderwidth=0,anchor="w")
        self.add_user_button.grid(padx=20,pady=10)
        self.dashboard_button = tk.Button(side_bar, text="Dashboard", command=self.dashboard, fg="#ffffff", bg="#6a1b9a", font=("Arial", 15), width=10, height=1, borderwidth=0,anchor="w")
        self.dashboard_button.grid(padx=20,pady=10,sticky="w")
        tk.Button(side_bar, text="Add Account", command=self.add_account, fg="#ffffff", bg="#6a1b9a", font=("Arial", 15), width=10, height=1, borderwidth=0,anchor="w").grid(padx=20,pady=10,sticky="w")
        tk.Button(side_bar, text="Switch User", command=self.switch_user, fg="#ffffff", bg="#6a1b9a", font=("Arial", 15), width=10, height=1, borderwidth=0,anchor="w").grid(padx=20,pady=10,sticky="w")
        tk.Button(side_bar, text="Logout", command=self.logout, fg="#ffffff", bg="#6a1b9a", font=("Arial", 15), width=10, height=1, borderwidth=0,anchor="w").grid(padx=20,sticky="w",pady=10)
        
        self.inventory_frame.rowconfigure(0, weight=1)
        self.inventory_frame.columnconfigure(0, weight=0)
        self.inventory_frame.columnconfigure(1, weight=1)
    

        top = tk.Frame(self.inventory_frame,bg="#d9d9d9", width=200, height=100)
        top.grid(row=0,column=1,sticky="nsew",padx=20)

        title = tk.Label(top,text="INVENTORY MANAGEMENT", font=("Arial",20,"bold"),bg="#d9d9d9",fg="#000000")
        title.grid(row=0,column=0,pady=20,columnspan=2)
        #tk.Button(top, text="Print List", command=self.print_document, fg="#ffffff", bg="#6a1b9a", font=("Arial", 15), width=10, height=1, borderwidth=0).grid(padx=20,pady=10,row=0,column=1)

        left_frame = ttk.LabelFrame(top,text="Product Information")
        left_frame.grid(row=1,column=0,sticky="nwe",padx=50,pady=40)

        left_frame.grid_columnconfigure(0, minsize=120)  # Set column 0 width
        left_frame.grid_columnconfigure(1, minsize=120)

        validate_cmd = self.root.register(self.validate_sku_input)


        ttk.Label(left_frame,text="sku",).grid(row=0,column=0,sticky="w",pady=(10,0),padx=(10,10))
        self.entry_item_sku = ttk.Entry(left_frame,validate="key", validatecommand=(validate_cmd, "%P"))
        self.entry_item_sku.grid(row=1,column=0,sticky="ew",columnspan=2,padx=(10,10))


        ttk.Label(left_frame,text="Name").grid(row=2,column=0,sticky="w",pady=(10,0),padx=(10,10))
        self.entry_item_name = ttk.Entry(left_frame)
        self.entry_item_name.grid(row=3,column=0,sticky="ew",columnspan=2,padx=(10,10))

        ttk.Label(left_frame,text="Quantity").grid(row=4,column=0,sticky="w",pady=(10,0),padx=(10,10))
        self.entry_quantity = ttk.Spinbox(left_frame,from_=0, to=100000)
        self.entry_quantity.grid(row=5,column=0,sticky="ew",columnspan=2,padx=(10,10))

        ttk.Label(left_frame,text="Price").grid(row=6,column=0,sticky="w",pady=(10,0),padx=(10,10))
        self.entry_price = ttk.Entry(left_frame)
        self.entry_price.grid(row=7,column=0,sticky="ew",columnspan=2,padx=(10,10))

        tk.Button(left_frame, text="add", command=self.add_item, fg="#ffffff", bg="#6a1b9a", 
                font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=8, column=0, pady=10, padx=(20,5))
        tk.Button(left_frame, text="update", command=self.update_item, fg="#ffffff", bg="#6a1b9a", 
                font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=8, column=1, pady=10, padx=(5,20))
        tk.Button(left_frame, text="delete", command=self.delete_item, fg="#ffffff", bg="#6a1b9a", 
                font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=9, column=0, pady=10, padx=(20,5))
        tk.Button(left_frame, text="clear", command=self.clear_entries, fg="#ffffff", bg="#6a1b9a", 
                font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=9, column=1, pady=10, padx=(5,20))
        
        separator = ttk.Separator(left_frame)
        separator.grid(row=10,column=0,padx=(10,10),pady=10,sticky="ew",columnspan=2)

        ttk.Label(left_frame,text="Search").grid(row=11,column=0,sticky="w",pady=(10,0),padx=(10,10))
        self.search = ttk.Entry(left_frame)
        self.search.grid(row=12,column=0,sticky="ew",columnspan=2,padx=(10,10))

        self.sku_var = tk.BooleanVar()
        self.name_var = tk.BooleanVar()

        self.checkbox1 = tk.Checkbutton(left_frame,text="sku",bg="#d9d9d9",variable=self.sku_var).grid(row=13,column=0)
        self.checkbox2 = tk.Checkbutton(left_frame,text="Name",bg="#d9d9d9",variable=self.name_var).grid(row=13,column=1)

        tk.Button(left_frame, text="search", command=self.search_item, fg="#ffffff", bg="#6a1b9a", font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=14, column=0, pady=10,padx=(20,5))
        tk.Button(left_frame, text="refresh", command=self.refresh_inventory, fg="#ffffff", bg="#6a1b9a", font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=14, column=1,pady=10,padx=(5,20))

        right_frame = ttk.LabelFrame(top,text="Inventory List")
        right_frame.grid(row=1,column=1,padx=(40,20))
    
        inventory_menu =  tk.Menu(self.root,bg="#6a1b9a",fg="#ffffff", tearoff=0)
        inventory_menu.config(bg="#6a1b9a")
        self.root.config(menu=inventory_menu)
        file_menu = tk.Menu(inventory_menu,bg="#6a1b9a",fg="#ffffff", tearoff=0)
        file_menu.config(bg="#6a1b9a")
        inventory_menu.add_cascade(label='Menu',menu=file_menu)
        file_menu.add_cascade(label="Dashboard",command=self.dashboard)
        file_menu.add_cascade(label="print inventory",command=self.print_document)
        file_menu.add_cascade(label="Logout",command=self.logout)
        # #tk.Button(self.inventory_frame, text="print inventory", command=self.print_document, fg="#ffffff", bg="#6a1b9a", font=("Arial", 11), width=10, height=1, borderwidth=2).grid(row=5, column=8, pady=5, padx=10)
        
        scroll_bar = ttk.Scrollbar(right_frame, orient="vertical")
        scroll_bar.grid(column=1, sticky='ns', padx=(0, 10))
        self.tree = ttk.Treeview(right_frame, columns=('Sku', 'Name', 'Quantity', 'Price'), show='headings',height=17)
        self.tree.heading('Sku', text='Sku')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Quantity', text='Quantity')
        self.tree.heading('Price', text='Price')
        self.tree.column('Sku', width=70, anchor='center')
        self.tree.column('Name', width=170)
        self.tree.column('Quantity', width=170, anchor='center')
        self.tree.column('Price', width=170, anchor='center')
        self.tree.grid(row=0, column=0,padx=20,pady=10)
        scroll_bar.config(command=self.tree.yview)
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        self.refresh_inventory()
        
    def on_item_select(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.entry_item_sku.delete(0, tk.END)
            self.entry_item_sku.insert(0, values[0])
            self.entry_item_name.delete(0, tk.END)
            self.entry_item_name.insert(0, values[1])
            self.entry_quantity.delete(0, tk.END)
            self.entry_quantity.insert(0, values[2])
            self.entry_price.delete(0, tk.END)
            self.entry_price.insert(0, values[3])

    def add_item(self):
        sku = self.entry_item_sku.get()
        name = self.entry_item_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()
        if not self.validate_sku(sku):
            messagebox.showerror("Validation Error", "SKU must be a non-negative integer.")
            return
        
        if not self.validate_price(price):
            messagebox.showerror("Validation Error", "Price must be a positive float.")
            return

        if not self.validate_quantity(quantity):
            messagebox.showerror("Validation Error", "Quantity must be a positive integer.")
            return

        if not self.validate_item_name(name):
            messagebox.showerror("Validation Error", "Item name can only contain alphabets, numbers, and special characters.")
            return

        # Convert the validated inputs to the appropriate types
        quantity = int(quantity)
        price = float(price)

        self.inventory_manager.add_item(sku, name, quantity, price)
        self.refresh_inventory()
        self.clear_entries()

    def update_item(self):
        selected_item = self.tree.focus()
        sku = self.tree.item(selected_item, 'values')[0]
        name = self.entry_item_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()

        if not self.validate_sku(sku):
            messagebox.showerror("Validation Error", "SKU must be a non-negative integer.")
            return
        
        if not self.validate_price(price):
            messagebox.showerror("Validation Error", "Price must be a positive float.")
            return

        if not self.validate_quantity(quantity):
            messagebox.showerror("Validation Error", "Quantity must be non negative.")
            return

        if not self.validate_item_name(name):
            messagebox.showerror("Validation Error", "Item name can only contain alphabets, numbers, and special characters.")
            return

        # Convert the validated inputs to the appropriate types
        quantity = int(quantity)
        price = float(price)


        self.inventory_manager.update_item(sku, name, quantity, price)
        self.refresh_inventory()
        self.clear_entries()

    def delete_item(self):
        selected_item = self.tree.focus()
        if not selected_item:  # Check if any item is selected
            messagebox.showerror("Delete", "No item selected.")
            return

        # Retrieve SKU of the selected item
        sku = self.tree.item(selected_item, 'values')[0]

        # Ask for confirmation
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete item with SKU: {sku}?")
        if confirm:  # If the user clicks "Yes"
            self.inventory_manager.delete_item(sku)
            self.refresh_inventory()
            self.clear_entries()
            
    def refresh_inventory(self):
        self.search.delete(0, tk.END)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.inventory_manager.get_all_items():
            self.tree.insert('', 'end', values=row)

    def clear_entries(self):
        self.entry_item_sku.delete(0, tk.END)
        self.entry_item_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)

        #BUTTONS FUNCTIONS

    def search_item(self):
        if self.sku_var.get():
            search = int(self.search.get())  # Assuming 'search' is an Entry widget that takes the SKU number
            result = self.inventory_manager.get_item_sku(search)  # You will need to define this method in your inventory manager
        elif self.name_var.get():
            search = self.search.get()  # Assuming 'search' is an Entry widget that takes the item name
            result = self.inventory_manager.get_item_name(search)  # You will need to define this method in your inventory manager
        else:
            messagebox.showerror("Search", "Please select either SKU or Name to search by.")
            return

        if result: 
            for row in self.tree.get_children():
                self.tree.delete(row)
            self.tree.insert('', 'end', values=result)
        else:
            messagebox.showerror("Search", "No results found.")

    def logout(self):
        response = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?")
        if response:  
            self.user_manager.update_user_active_status(self.user_id, active=0)
            self.root.destroy()
            root = tk.Tk()
            app = InventoryApp(root)
            root.mainloop()

    def dashboard(self):
        self.inventory_frame.destroy()
        Dashboard(self.root, self.inventory_manager,self.create_inventory_window,self.user_id,self.user_role)

    def add_employees(self):
        self.inventory_frame.destroy()
        self.tree.destroy()
        Add_Employee(self.root,self.user_manager,self.create_inventory_window,self.user_id)

    def add_account(self):
        if len(self.user_manager.get_active_users())>=2:
            messagebox.showerror("Add Account","Can add more than 2 accounts")
        else:
            self.inventory_frame.destroy()
            self.create_login_window()

    # class InventoryApp:
    def switch_user(self):
        global flag
        active = self.user_manager.get_active_users()

        if len(active) == 1:
            messagebox.showerror("Switch Account", "Add another account first in order to switch.")
            return

        # Toggle the flag between 0 and 1
        flag = 1 - flag

        # Get the next active user based on the toggled flag
        user = active[flag]
        self.user_id = user[0]
        self.user_role = user[3]

        print(f"Switching to: {user[1]} ({self.user_role})")

        # Destroy the current window and initialize the appropriate interface
        self.root.destroy()
        

        if self.user_role == "admin":
            root = tk.Tk()
            InventoryApp(root).create_inventory_window(self.user_id)
            root.mainloop()
        elif self.user_role == "user":
            root = tk.Tk()
            InventoryApp_User(root, self.user_id,self.user_role).create_inventory_window(self.user_id)
            root.mainloop()


    # def switch_user(self):
    #     active_users = self.user_manager.get_active_users()
        
    #     if len(active_users) < 2:
    #         messagebox.showerror("Switch Account", "Please add a second account first in order to switch.")
    #         return

    #     # Determine which user to switch to based on the flag
    #     if self.flag == 0:
    #         self.flag = 1
    #     else:
    #         self.flag = 0

    #     next_user = active_users[self.flag]
    #     self.user_id = next_user[0]  # Update with the switched user ID
    #     self.user_name = next_user[1]
    #     self.user_role = next_user[3]

    #     # Clear current interface and load the correct one for the next user
    #     self.inventory_frame.destroy()
    #     if self.user_role == "admin":
    #         self.create_inventory_window()
    #     else:
    #         InventoryApp_User(self.root, self.user_id)


    def print_document(self):
        pdf = FPDF("P", "mm", "Letter")
        pdf.add_page()
        
        # Set the title
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "Inventory Report", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(10)

        # Set the column headers
        pdf.set_font("helvetica", "B", 12)

        # Widths of each column
        col_width = 60  # Adjust this based on your content
        table_width = col_width * 3
        start_x = (pdf.w - table_width) / 2  # Calculate starting X position

        pdf.set_x(start_x)
        pdf.cell(col_width, 10, "Name", 1)
        pdf.cell(col_width, 10, "Quantity", 1)
        pdf.cell(col_width, 10, "Price", 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Set the rows of the table
        pdf.set_font("helvetica", "", 12)
        for item in self.inventory_manager.get_all_items():
            name = item[1]
            quantity = item[2]
            price = item[3]
            
            pdf.set_x(start_x)  # Set the X position for each row
            pdf.cell(col_width, 10, name, 1)
            pdf.cell(col_width, 10, str(quantity), 1)
            pdf.cell(col_width, 10, f"{price}", 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Save the PDF
        pdf_path = "inventory_report.pdf"
        pdf.output(pdf_path)
        os.startfile(pdf_path, "print")

class InventoryApp_User(InventoryApp):
    def __init__(self,root,user_id,user_role):
        super().__init__(root)
        self.user_id = user_id
        self.user_role = user_role
        self.create_inventory_window(self.user_id)
        self.add_user_button.grid_remove()
        self.dashboard_button.grid_remove()

    def delete_item(self):
        messagebox.showerror("ERROR", "You do not have the permission to delete")

    def dashboard(self):
        self.inventory_frame.destroy()
        self.inventory_frame.destroy()
        self.inventory_frame.destroy()
        #self.tree.destroy()
        Dashboard(self.root, self.inventory_manager,self.create_inventory_window,self.user_id,self.user_role)
class Dashboard:
    def __init__(self,root,inventory_manager,create_inventory_window,user_id,user_role):
        self.root = root
        self.user_id = user_id
        self.user_role = user_role
        self.inventory_manager = inventory_manager
        self.create_inventory_window = create_inventory_window
        self.dashboard_frame = tk.Frame(self.root,bg="#d9d9d9")
        self.dashboard_frame.pack(fill="both",expand=True)
        tk.Label(self.dashboard_frame, text="DASHBOARD", font=("Arial",20,"bold"),bg="#d9d9d9",fg="#000000").pack(pady=20)
        tk.Button(self.dashboard_frame, text="Back", command=self.dashboard_back, 
        fg="#ffffff", bg="#6a1b9a", font=("Arial", 11), width=10, 
        height=1, borderwidth=2, relief= "raised").place(x=20, y=20)
        self.root.config(menu="")

        self.create_graphs()

    def create_graphs(self):
        items = self.inventory_manager.get_all_items()
        names = [item[1] for item in items] 
        quantities = [item[2] for item in items]  

        # Define pastel colors
        pastel_colors = ['#D7BDE2', '#C39BD3', '#BB8FCE', '#AF7AC5', '#A569BD', '#884EA0', '#76448A']
        # Bar Chart
        fig1 = Figure()
        plot1 = fig1.add_subplot(111)
        plot1.bar(names, quantities, color=pastel_colors[:len(names)])
        plot1.tick_params(axis='x', labelrotation=90)
        plot1.set_facecolor('#d9d9d9')  # Background color for the plot
        fig1.patch.set_facecolor('#d9d9d9')  # Background color for the entire figure
        canvas1 = FigureCanvasTkAgg(fig1, self.dashboard_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left")
        fig1.subplots_adjust(bottom=0.3)

        # Pie Chart
        fig2 = Figure()
        plot2 = fig2.add_subplot(111)
        plot2.pie(quantities, labels=names, autopct='%1.1f%%', colors=pastel_colors[:len(names)])
        plot2.set_facecolor('#d9d9d9')  # Background color for the plot
        fig2.patch.set_facecolor('#d9d9d9')  # Background color for the entire figure
        canvas2 = FigureCanvasTkAgg(fig2, self.dashboard_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="right")

        # Optionally adjust layout
        fig2.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    

    def dashboard_back(self):
        self.dashboard_frame.destroy()
        # if self.user_role == "admin":
        #     InventoryApp(root).create_inventory_window(self.user_id)
        # if self.user_role == "user":
        #     InventoryApp_User(root, self.user_id,self.user_role).create_inventory_window(self.user_id)
        self.create_inventory_window(self.user_id)


class Add_Employee:
    def __init__(self,root,user_manager,create_inventory_window,user_id):
        self.root = root
        self.user_id = user_id
        self.user_manager = user_manager
        self.create_inventory_window = create_inventory_window
        self.root.config(menu="")

        self.add_employees_frame = ttk.Frame(self.root)
        self.add_employees_frame.pack(expand=True, fill="both")
        tk.Label(self.add_employees_frame, text="USER MANAGEMENT", font=("Arial",20,"bold"),bg="#d9d9d9",fg="#000000").grid(row=0,columnspan=2,pady=30)
        tk.Button(self.add_employees_frame, text="Back", command=self.add_user_back, fg="#ffffff", bg="#6a1b9a", font=("Arial", 11), width=10, height=1, borderwidth=2).place(x=20, y=20)

        left_frame = ttk.LabelFrame(self.add_employees_frame,text="User Information")
        left_frame.grid(row=1,column=0,sticky="nwe",pady=100,padx=(160,40))

        left_frame.grid_columnconfigure(0, minsize=120)  # Set column 0 width
        left_frame.grid_columnconfigure(1, minsize=120)  # Set column 1 width

        ttk.Label(left_frame,text="Name").grid(row=0,column=0,sticky="w",pady=(10,0),padx=(10,10))
        self.entry_employee_name = ttk.Entry(left_frame)
        self.entry_employee_name.grid(row=1,column=0,sticky="ew",columnspan=2,padx=(10,10))

        ttk.Label(left_frame,text="Password").grid(row=2,column=0,sticky="w",pady=(10,0),padx=(10,10))
        self.entry_password = ttk.Entry(left_frame)
        self.entry_password.grid(row=3,column=0,sticky="ew",columnspan=2,padx=(10,10))

        ttk.Label(left_frame,text="Level").grid(row=4,column=0,sticky="w",pady=(10,0),padx=(10,10))
        self.level_var = tk.StringVar()
        self.combobox_level = ttk.Combobox(left_frame, textvariable=self.level_var,width=12,font=("Arial",11))
        self.combobox_level['values'] = ("user", "admin")  # Options for the combobox
        self.combobox_level.grid(row=5, column=0,sticky="ew",columnspan=2,padx=(10,10))
        self.combobox_level.current(0)

        tk.Button(left_frame, text="add", command=self.add_user, fg="#ffffff", bg="#6a1b9a", 
                font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=6, column=0, pady=10, padx=(20,5))
        tk.Button(left_frame, text="update", command=self.update_user, fg="#ffffff", bg="#6a1b9a", 
                font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=6, column=1, pady=10, padx=(5,20))
        tk.Button(left_frame, text="delete", command=self.delete_user, fg="#ffffff", bg="#6a1b9a", 
                font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=7, column=0, pady=10, padx=(20,5))
        tk.Button(left_frame, text="clear", command=self.clear_users, fg="#ffffff", bg="#6a1b9a", 
                font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=7, column=1, pady=10, padx=(5,20))


        right_frame = ttk.LabelFrame(self.add_employees_frame,text="User List")
        right_frame.grid(row=1,column=1,padx=(40,20),pady=40)

        scroll_bar = ttk.Scrollbar(right_frame, orient="vertical")
        scroll_bar.grid(column=1, sticky='ns', padx=(0, 10))
        self.user_tree = ttk.Treeview(right_frame, columns=('ID','Name', 'Password', 'Level'), show='headings',height=17)
        self.user_tree.heading('ID', text='ID')
        self.user_tree.heading('Name', text='Name')
        self.user_tree.heading('Password', text='Password')
        self.user_tree.heading('Level', text='Level')
        self.user_tree.column('Name', width=120)
        self.user_tree.column('Password', width=120, anchor='center')
        self.user_tree.column('Level', width=120, anchor='center')
        self.user_tree.grid(row=0, column=0,pady=10, padx=10)
        scroll_bar.config(command=self.user_tree.yview)
        self.user_tree.bind('<<TreeviewSelect>>', self.on_user_select)
        self.refresh_users()

    def add_user(self):
        user_name = self.entry_employee_name.get()
        password = self.entry_password.get()
        level = self.level_var.get()
        self.user_manager.add_user(user_name, password, level)
        self.refresh_users()
        self.clear_users()

    def update_user(self):
        selected_user = self.user_tree.focus()
        user_id = self.user_tree.item(selected_user, 'values')[0]
        name = self.entry_employee_name.get()
        password = self.entry_password.get()
        level = self.level_var.get()
        self.user_manager.update_user(user_id, name, password, level)
        self.refresh_users()
        self.clear_users()

    def delete_user(self):
        selected_user = self.user_tree.focus()
        user_id = self.user_tree.item(selected_user, 'values')[0]
        self.user_manager.delete_user(user_id)
        self.refresh_users()
        self.clear_users()

    def refresh_users(self):
        for row in self.user_tree.get_children():
            self.user_tree.delete(row)
        for row in self.user_manager.get_all_users():
            self.user_tree.insert('', 'end', values=row)

    def clear_users(self):
        self.entry_employee_name.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        
    def add_user_back(self):
        self.add_employees_frame.destroy()
        self.user_tree.destroy()
        self.create_inventory_window(self.user_id)

    def on_user_select(self, event):
        selected_user = self.user_tree.focus()
        if selected_user:
            values = self.user_tree.item(selected_user, 'values')
            self.entry_employee_name.delete(0, tk.END)
            self.entry_employee_name.insert(0, values[1])
            self.entry_password.delete(0, tk.END)
            self.entry_password.insert(0, values[2])


if __name__ == "__main__":
    flag = 0
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

