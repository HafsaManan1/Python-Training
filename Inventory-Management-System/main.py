import tkinter as tk
# import ttkbootstrap as tb
# from ttkbootstrap.toast import ToastNotification
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db import Database
from manager import UserManager, InventoryManager
from fpdf import FPDF, XPos, YPos
import os
import re
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Login:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.user_manager = UserManager(self.db)
        self.root.title("Login Page")
        self.root.state("zoomed")
        self.root.title("Inventory Management System")
        root.configure(background='#d9d9d9')
        self.password_visible = False
        self.create_login_window()

    def create_login_window(self):
        self.login_frame = tk.Frame(self.root, bg="#F0F0F0", bd=40, width=350)
        self.login_frame.pack(pady=(110), anchor=tk.CENTER)

        self.login_image = tk.PhotoImage(file="icon.png")

        tk.Label(self.login_frame, text="WELCOME", fg="#333333", bg="#F0F0F0", font=("Arial", 30, "bold")).pack(pady=(10))
        self.picture = tk.Label(self.login_frame, image=self.login_image)
        self.picture.pack(fill="both", expand="yes")

        tk.Label(self.login_frame, text="Username", font=("Arial", 14), fg="#333333", bg="#F0F0F0").pack(anchor="w")
        self.entry_username = tk.Entry(self.login_frame, width=25, font=("Arial", 12), bg="#e0e0e0")
        self.entry_username.insert(0,"Username")
        self.entry_username.bind("<FocusIn>", lambda e: self.entry_username.delete(0, tk.END))
        self.entry_username.pack(pady=10, ipady=3)

        tk.Label(self.login_frame, text="Password", font=("Arial", 14), fg="#333333", bg="#F0F0F0").pack(anchor="w")
        self.entry_password = tk.Entry(self.login_frame, show='●', width=25, font=("Arial", 12), bg="#e0e0e0")
        self.entry_password.insert(0,"Password")
        self.entry_password.bind("<FocusIn>", lambda e: self.entry_password.delete(0, tk.END))
        self.entry_password.pack(pady=10, ipady=3)

        self.show_password_icon = tk.PhotoImage(file="eye.png")  # Replace with your eye icon file path
        self.hide_password_icon = tk.PhotoImage(file="eye_hide.png")  # Replace with your hide icon file path
        self.eye_button = tk.Button(self.login_frame, image=self.show_password_icon, command=self.toggle_password_visibility, bd=0, bg="#e0e0e0")
        self.eye_button.place(x=205, y=260)  # Adjust position as needed

        tk.Button(self.login_frame, text="Login", command=self.login, fg="#ffffff", bg="#6a1b9a", font=("Arial", 12), width=25, height=1, borderwidth=0).pack(pady=10)
        self.root.bind('<Return>', self.login)

    def on_focus_in_username(self, event):
        if self.entry_username.get() == "Username":
            self.entry_username.delete(0, tk.END)
            self.entry.config(fg="#808080")

    def on_focus_in_password(self, event):
        if self.entry_password.get() == "Password":
            self.entry_password.delete(0, tk.END)
            self.entry_password.config(show="●",fg="#808080")

    def toggle_password_visibility(self):
        if self.password_visible:
            self.entry_password.config(show="●")
            self.eye_button.config(image=self.show_password_icon)
            self.password_visible = False
        else:
            self.entry_password.config(show="")
            self.eye_button.config(image=self.hide_password_icon)
            self.password_visible = True

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
                messagebox.showinfo("Login",f"Logging in as {self.user_name} (user)")
                self.login_frame.forget()
                self.root.unbind('<Return>')
                Dashboard_User(self.root,self.user_id,self.user_role)
            if self.user[3]=="admin":
                messagebox.showinfo("Login",f"Logging in as {self.user_name} (admin)")
                self.login_frame.forget()
                self.root.unbind('<Return>')
                Dashboard(self.root,self.user_id,self.user_role)
        else:
            messagebox.showerror("Login", "Invalid username or password.")

class Dashboard:
    def __init__(self,root,user_id,user_role):
        self.root = root
        self.db = Database()
        self.inventory_manager = InventoryManager(self.db)
        self.user_manager = UserManager(self.db)
        self.user_id = user_id
        self.user_role = user_role
        self.total_products = self.inventory_manager.get_total_item()[0]
        self.low_stock_products = self.inventory_manager.get_low_stock()[0]
        self.out_of_stock_products = self.inventory_manager.get_out_of_stock()[0]
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_dashboard_window()

    def on_closing(self):
        for id in self.user_manager.get_active_id():
            self.user_manager.update_user_active_status(id[0],0)
        self.root.destroy()

    def create_dashboard_window(self):
        self.dashboard_frame = tk.Frame(self.root,bg="#d9d9d9")
        self.dashboard_frame.pack(fill="both",expand=True)
        self.user = tk.PhotoImage(file="social.png")
        self.dashh = tk.PhotoImage(file="inventory.png")
        self.interaction = tk.PhotoImage(file="web.png")
        self.log_out = tk.PhotoImage(file="logoutt.png")
        self.add = tk.PhotoImage(file="pluss.png")
        self.image = Image.open("favicon.webp")
        self.logo = ImageTk.PhotoImage(self.image)
        self.side_bar = tk.Frame(self.dashboard_frame, bg="#6a1b9a")
        self.side_bar.pack(fill="y",side="left")

        tk.Button(self.side_bar, text=" Osol-Tech", fg="#ffffff", bg="#6a1b9a", activebackground="#6a1b9a",
                  font=("Arial", 18), width=170, height=50, borderwidth=0,anchor="w", compound="left",image=self.logo).pack(padx=20,pady=(10,80))
        self.add_user_button = tk.Button(self.side_bar, text=" Add User",image=self.user,compound="left", command=self.add_employees, fg="#ffffff", bg="#6a1b9a",activebackground="#6a1b9a", 
                                         font=("Arial", 14), width=170, height=50, borderwidth=0,anchor="w")
        self.add_user_button.pack(padx=20,pady=15)
        self.dashboard_button = tk.Button(self.side_bar, text=" Add Inventory", command=self.add_inventory, fg="#ffffff", bg="#6a1b9a",activebackground="#6a1b9a", font=("Arial", 14), width=170, height=50, borderwidth=0,anchor="w",compound="left",image=self.dashh)
        self.dashboard_button.pack(padx=20,pady=10)
        tk.Button(self.side_bar, text=" Add Account", command=self.add_account, fg="#ffffff", bg="#6a1b9a", activebackground="#6a1b9a",
                  font=("Arial", 14), width=170, height=50, borderwidth=0,anchor="w",compound="left",image=self.add).pack(padx=20,pady=10)
        tk.Button(self.side_bar, text=" Switch User", command=self.switch_user, fg="#ffffff", bg="#6a1b9a", activebackground="#6a1b9a",
                  font=("Arial", 14), width=170, height=50, borderwidth=0,anchor="w",compound="left",image=self.interaction).pack(padx=20,pady=10)
        tk.Button(self.side_bar, text=" Logout", command=self.logout, fg="#ffffff", bg="#6a1b9a", activebackground="#6a1b9a",
                  font=("Arial", 14), width=170, height=50, borderwidth=0,anchor="w", compound="left",image=self.log_out).pack(padx=20,pady=10)
        self.create_graphs()

    def create_graphs(self):
        items = self.inventory_manager.get_all_items()
        names = [item[1] for item in items] 
        quantities = [item[2] for item in items]  

        colors = ['#8e44ad', '#d4a5d6', '#e5b8c1', '#82c4c3', '#a7d19c', '#f1c659', '#ff847c']

        # Bar Chart
        tk.Label(self.dashboard_frame,text="INVENTORY DASHBOARD", font=("Arial",20,"bold"),bg="#d9d9d9",fg="#000000").pack(pady=20)
        fig1 = Figure(figsize=(5, 4))
        plot1 = fig1.add_subplot(111)
        plot1.bar(names, quantities, color=colors[:len(names)])
        plot1.tick_params(axis='x', labelrotation=90)
        plot1.set_facecolor('#d9d9d9')  # Background color for the plot
        fig1.patch.set_facecolor('#d9d9d9')  # Background color for the entire figure
        canvas1 = FigureCanvasTkAgg(fig1, self.dashboard_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left",fill="y")
        fig1.subplots_adjust(bottom=0.3)

        # Pie Chart
        fig2 = Figure(figsize=(2, 2))
        plot2 = fig2.add_subplot(111)
        plot2.pie(quantities, labels=names, autopct='%1.1f%%', colors=colors[:len(names)])
        plot2.set_facecolor('#d9d9d9')  # Background color for the plot
        fig2.patch.set_facecolor('#d9d9d9')  # Background color for the entire figure

        stats_text = f'Total Products: {self.total_products}\nLow Stock Products: {self.low_stock_products}\nOut of Stock Products: {self.out_of_stock_products}'
        plot2.text(-1.5, 1.5, stats_text, fontsize=12, verticalalignment='top',horizontalalignment="left", bbox=dict(facecolor='white', alpha=0.8))

        canvas2 = FigureCanvasTkAgg(fig2, self.dashboard_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(anchor="center",expand=True,fill="both")
           
    def add_inventory(self):
        self.dashboard_frame.destroy()
        if self.user_role == "admin":
            InventoryApp(self.root,self.dashboard_frame,self.user_id,self.user_role)

        if self.user_role == "user":
            InventoryApp_User(self.root,self.dashboard_frame,self.user_id,self.user_role)

    def add_account(self):
        if len(self.user_manager.get_active_users())>=2:
            messagebox.showerror("Add Account","Can't add more than 2 accounts")
        else:
            self.dashboard_frame.pack_forget()
            Login(self.root)

    def switch_user(self):
        global flag
        active = self.user_manager.get_active_users()

        if len(active) == 1:
            messagebox.showerror("Switch Account", "Add another account first in order to switch.")
            return
        current_user_id = self.user_id

        if active[flag][0] == current_user_id:
            flag = 1 - flag

        user = active[flag]
        self.user_id = user[0]
        self.user_role = user[3]
        messagebox.showinfo("Switching", f"Switching to: {user[1]} ({self.user_role})")
        self.dashboard_frame.pack_forget()

        if self.user_role == "admin":
            Dashboard(root,self.user_id,self.user_role)

        elif self.user_role == "user":
            Dashboard_User(root,self.user_id,self.user_role)
    
    def add_employees(self):
        self.dashboard_frame.pack_forget()
        Add_Employee(self.root,self.dashboard_frame)

    def logout(self):
        response = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?")
        if response:  
            self.user_manager.update_user_active_status(self.user_id, active=0)
            active_users = self.user_manager.get_active_users()

            if len(active_users)==1:
                self.dashboard_frame.pack_forget()
                user = active_users[0]
                self.user_id = user[0]
                self.user_role = user[3]

                if self.user_role == "admin":
                    Dashboard(self.root,self.user_id,self.user_role)

                elif self.user_role == "user":
                    Dashboard_User(self.root,self.user_id,self.user_role)
            else:
                self.dashboard_frame.pack_forget()
                Login(self.root)

class Dashboard_User(Dashboard):
    def __init__(self,root,user_id,user_role):
        super().__init__(root,user_role,user_id)
        self.root = root
        self.user_id = user_id
        self.user_role = user_role
        self.add_user_button.pack_forget()
    
class InventoryApp:
    def __init__(self,root,dashboard_frame,user_id,user_role):
        self.db = Database()
        self.user_manager = UserManager(self.db)
        self.inventory_manager = InventoryManager(self.db)
        self.root = root
        self.user_id = user_id
        self.user_role = user_role
        self.dashboard_frame = dashboard_frame
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview",background= "#ffffff", foreground = "black", rowheight= 25, fieldbackground="#ffffff")
        self.style.map("Treeview",background=[("selected","#6a1b9a")])
        self.sku_pattern = re.compile(r'^\d+$')  # Non-negative integers
        self.price_pattern = re.compile(r'^[+]?\d*\.?\d+$')  # Positive float
        self.quantity_pattern = re.compile(r'^[+]?\d+$')  # Positive integers
        self.item_name_pattern = re.compile(r'^[\w\s\-\(\)\[\]\{\}\.,\'"]+$')  # Alphabetic with special character
        self.flag = 0
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_inventory_window()

    def on_closing(self):
        for id in self.user_manager.get_active_id():
            self.user_manager.update_user_active_status(id[0],0)
        self.root.destroy()

    # def validate_sku(self, sku):
    #     return bool(self.sku_pattern.match(sku))

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
    
    def create_inventory_window(self):
        self.inventory_frame = ttk.Frame(self.root)
        self.inventory_frame.pack(expand=True, fill="both")
        
        self.inventory_frame.rowconfigure(0, weight=1)
        self.inventory_frame.columnconfigure(0, weight=0)
        self.inventory_frame.columnconfigure(1, weight=1)
    
        self.top = tk.Frame(self.inventory_frame,bg="#d9d9d9", width=200, height=100)
        self.top.grid(row=0,column=1,sticky="nsew",padx=20)

        self.title = tk.Label(self.top,text="    INVENTORY MANAGEMENT", font=("Arial",20,"bold"),bg="#d9d9d9",fg="#000000")
        self.title.grid(row=0,column=1,pady=20,columnspan=2,sticky="w")
        tk.Button(self.top, text="Back", command=self.inventory_back, fg="#ffffff", bg="#6a1b9a", font=("Arial", 11), width=10, height=1, borderwidth=2).place(x=20, y=20)
        
        self.left_frame = ttk.LabelFrame(self.top,text="Product Information")
        self.left_frame.grid(row=1,column=0,sticky="nwe",padx=(180,40),pady=50)

        self.left_frame.grid_columnconfigure(0, minsize=120)
        self.left_frame.grid_columnconfigure(1, minsize=120)

        self.validate_cmd = self.root.register(self.validate_sku_input)

        ttk.Label(self.left_frame,text="sku",).grid(row=0,column=0,sticky="w",pady=(10,0),padx=(10,10))
        self.entry_item_sku = ttk.Entry(self.left_frame,validate="key", validatecommand=(self.validate_cmd, "%P"))
        self.entry_item_sku.grid(row=1,column=0,sticky="ew",columnspan=2,padx=(10,10))


        ttk.Label(self.left_frame,text="Name").grid(row=2,column=0,sticky="w",pady=(10,0),padx=(10,10))
        self.entry_item_name = ttk.Entry(self.left_frame)
        self.entry_item_name.grid(row=3,column=0,sticky="ew",columnspan=2,padx=(10,10))

        ttk.Label(self.left_frame,text="Quantity").grid(row=4,column=0,sticky="w",pady=(10,0),padx=(10,10))
        self.entry_quantity = ttk.Spinbox(self.left_frame,from_=0, to=100000)
        self.entry_quantity.grid(row=5,column=0,sticky="ew",columnspan=2,padx=(10,10))

        ttk.Label(self.left_frame,text="Price").grid(row=6,column=0,sticky="w",pady=(10,0),padx=(10,10))
        self.entry_price = ttk.Entry(self.left_frame)
        self.entry_price.grid(row=7,column=0,sticky="ew",columnspan=2,padx=(10,10))

        tk.Button(self.left_frame, text="add", command=self.add_item, fg="#ffffff", bg="#6a1b9a", 
                font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=8, column=0, pady=10, padx=(20,5))
        tk.Button(self.left_frame, text="update", command=self.update_item, fg="#ffffff", bg="#6a1b9a", 
                font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=8, column=1, pady=10, padx=(5,20))
        tk.Button(self.left_frame, text="delete", command=self.delete_item, fg="#ffffff", bg="#6a1b9a", 
                font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=9, column=0, pady=10, padx=(20,5))
        tk.Button(self.left_frame, text="clear", command=self.clear_entries, fg="#ffffff", bg="#6a1b9a", 
                font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=9, column=1, pady=10, padx=(5,20))
        
        separator = ttk.Separator(self.left_frame)
        separator.grid(row=10,column=0,padx=(10,10),pady=10,sticky="ew",columnspan=2)

        ttk.Label(self.left_frame,text="Search").grid(row=11,column=0,sticky="w",pady=(10,0),padx=(10,10))
        self.search = ttk.Entry(self.left_frame)
        self.search.grid(row=12,column=0,sticky="ew",columnspan=2,padx=(10,10))

        self.sku_var = tk.BooleanVar()
        self.name_var = tk.BooleanVar()

        self.checkbox1 = tk.Checkbutton(self.left_frame,text="sku",bg="#d9d9d9",variable=self.sku_var).grid(row=13,column=0)
        self.checkbox2 = tk.Checkbutton(self.left_frame,text="Name",bg="#d9d9d9",variable=self.name_var).grid(row=13,column=1)

        tk.Button(self.left_frame, text="search", command=self.search_item, fg="#ffffff", bg="#6a1b9a", 
                  font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=14, column=0, pady=10,padx=(20,5))
        tk.Button(self.left_frame, text="refresh", command=self.refresh_inventory, fg="#ffffff", bg="#6a1b9a", 
                  font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=14, column=1,pady=10,padx=(5,20))

        self.right_frame = ttk.LabelFrame(self.top,text="Inventory List")
        self.right_frame.grid(row=1,column=1,padx=(40,20),pady=10)
    
        tk.Button(self.right_frame, text="Print List", command=self.print_document, fg="#ffffff", bg="#6a1b9a", 
                font=("Arial", 11), width=10, height=1, borderwidth=2).grid(row=0, column=0,sticky="e",padx=20,pady=5)
        self.scroll_bar = ttk.Scrollbar(self.right_frame, orient="vertical")
        self.scroll_bar.grid(column=1, sticky='ns', padx=(0, 10))
        self.tree = ttk.Treeview(self.right_frame, columns=('Sku', 'Name', 'Quantity', 'Price'), show='headings',height=17)
        self.tree.heading('Sku', text='Sku')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Quantity', text='Quantity')
        self.tree.heading('Price', text='Price')
        self.tree.column('Sku', width=70, anchor='center')
        self.tree.column('Name', width=170)
        self.tree.column('Quantity', width=170, anchor='center')
        self.tree.column('Price', width=170, anchor='center')
        self.tree.grid(row=1, column=0,padx=20,pady=10)
        self.scroll_bar.config(command=self.tree.yview)
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

        if not sku or not name or not quantity or not price:
            messagebox.showerror("Validation Error", "All fields are mandatory. Please fill in all fields.")
            return

        # if not self.validate_sku(sku):
        #     messagebox.showerror("Validation Error", "SKU must be a non-negative integer.")
        #     return

        if not self.validate_price(price):
            messagebox.showerror("Validation Error", "Price must be a positive float.")
            return

        if not self.validate_quantity(quantity):
            messagebox.showerror("Validation Error", "Quantity must be a positive integer.")
            return

        if not self.validate_item_name(name):
            messagebox.showerror("Validation Error", "Item name can only contain alphabets, numbers, and special characters.")
            return
        
        quantity = int(quantity)
        price = float(price)

        self.inventory_manager.add_item(sku, name, quantity, price)
        self.refresh_inventory()
        self.clear_entries()

    def update_item(self):
        selected_item = self.tree.focus()
        if not selected_item: 
            messagebox.showerror("Update", "No item selected.")
            return
        sku = self.tree.item(selected_item, 'values')[0]
        name = self.entry_item_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()

        if not sku or not name or not quantity or not price:
            messagebox.showerror("Validation Error", "All fields are mandatory. Please fill in all fields.")
            return
        # if not self.validate_sku(sku):
        #     messagebox.showerror("Validation Error", "SKU must be a non-negative integer.")
        #     return
        
        if not self.validate_price(price):
            messagebox.showerror("Validation Error", "Price must be a positive float.")
            return
        if not self.validate_quantity(quantity):
            messagebox.showerror("Validation Error", "Quantity must be non negative.")
            return
        if not self.validate_item_name(name):
            messagebox.showerror("Validation Error", "Item name can only contain alphabets, numbers, and special characters.")
            return
        
        quantity = int(quantity)
        price = float(price)
        self.inventory_manager.update_item(sku, name, quantity, price)
        self.refresh_inventory()
        self.clear_entries()

    def delete_item(self):
        selected_item = self.tree.focus()
        if not selected_item: 
            messagebox.showerror("Delete", "No item selected.")
            return
        sku = self.tree.item(selected_item, 'values')[0]

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
        self.refresh_inventory()

        #BUTTONS FUNCTIONS

    def search_item(self):
        if self.sku_var.get() and self.name_var.get():
            messagebox.showerror("Search", "Please select only one option sku or name.")

        if self.sku_var.get():
            search = self.search.get()  # Assuming 'search' is an Entry widget that takes the SKU number
            if not search:
                messagebox.showerror("Search", "Please enter sku to search.")
                return

            results = self.inventory_manager.get_item_sku(int(search))  # You will need to define this method in your inventory manager
        elif self.name_var.get():
            search = self.search.get()  # Assuming 'search' is an Entry widget that takes the item name
            if not search:
                messagebox.showerror("Search", "Please enter a name to search.")
                return
            results = self.inventory_manager.get_item_name(search)  # You will need to define this method in your inventory manager
        else:
            messagebox.showerror("Search", "Please select either SKU or Name to search by.")
            return

        if results: 
            for row in self.tree.get_children():
                self.tree.delete(row)
            for result in results:
                self.tree.insert('', 'end', values=result)
        else:
            messagebox.showerror("Search", "No results found.")

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
        col_width = 45  # Adjust this based on your content
        table_width = col_width * 4
        start_x = (pdf.w - table_width) / 2  # Calculate starting X position

        # Highlight the header row with a light lilac color (RGB: 230, 220, 235)
        pdf.set_fill_color(230, 220, 235)

        # Header row
        pdf.set_x(start_x)
        pdf.cell(col_width, 10, "SKU", 1, fill=True)
        pdf.cell(col_width, 10, "Name", 1, fill=True)
        pdf.cell(col_width, 10, "Quantity", 1, fill=True)
        pdf.cell(col_width, 10, "Price", 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)

        # Set the rows of the table
        pdf.set_font("helvetica", "", 12)
        for item in self.inventory_manager.get_all_items():
            sku = item[0]
            name = item[1]
            quantity = item[2]
            price = item[3]
            
            pdf.set_x(start_x)  # Set the X position for each row
            pdf.cell(col_width, 10, str(sku), 1)
            pdf.cell(col_width, 10, name, 1)
            pdf.cell(col_width, 10, str(quantity), 1)
            pdf.cell(col_width, 10, f"{price}", 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf_path = "inventory_report.pdf"
        pdf.output(pdf_path)
        os.startfile(pdf_path, "print")

    def inventory_back(self):
        self.inventory_frame.pack_forget()
        if self.user_role == "admin":
            Dashboard(self.root,self.user_id,self.user_role)
        if self.user_role == "user":
            Dashboard_User(self.root,self.user_id,self.user_role)

class InventoryApp_User(InventoryApp):
    def __init__(self,root,dashobard_frame,user_id,user_role):
        super().__init__(root, dashobard_frame,user_id,user_role)
    
    def delete_item(self):
        messagebox.showerror("ERROR", "You do not have the permission to delete")

class Add_Employee:
    def __init__(self,root,dashboard_frame):
        self.root = root
        self.db = Database()
        self.user_manager = UserManager(self.db)
        self.dashboard_frame = dashboard_frame
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview",background= "#ffffff", foreground = "black", rowheight= 25, fieldbackground="#ffffff")
        self.style.map("Treeview",background=[("selected","#6a1b9a")])
        self.username_pattern = r'^[a-zA-Z][a-zA-Z0-9_]{4,14}$'
        self.password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{5,20}$'

        self.add_employees_frame = ttk.Frame(self.root)
        self.add_employees_frame.pack(expand=True, fill="both")
        tk.Label(self.add_employees_frame, text="    USER MANAGEMENT", font=("Arial",20,"bold"),bg="#d9d9d9",fg="#000000").grid(row=0,column=1,pady=20,sticky="w")
        tk.Button(self.add_employees_frame, text="Back", command=self.add_user_back, fg="#ffffff", bg="#6a1b9a", font=("Arial", 11), width=10, height=1, borderwidth=2).place(x=20, y=20)

        left_frame = ttk.LabelFrame(self.add_employees_frame,text="User Information")
        left_frame.grid(row=1,column=0,sticky="nwe",pady=100,padx=(180,40)) 

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
        
        separator = ttk.Separator(left_frame)
        separator.grid(row=8,column=0,padx=(10,10),pady=10,sticky="ew",columnspan=2)

        ttk.Label(left_frame,text="Search By Username").grid(row=9,column=0,sticky="w",pady=(10,0),padx=(10,10))
        self.search = ttk.Entry(left_frame)
        self.search.grid(row=10,column=0,sticky="ew",columnspan=2,padx=(10,10))

        tk.Button(left_frame, text="Search", command=self.search_user, fg="#ffffff", bg="#6a1b9a", 
                  font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=11, column=0, pady=10,padx=(20,5))
        tk.Button(left_frame, text="refresh", command=self.refresh_users, fg="#ffffff", bg="#6a1b9a", 
                  font=("Arial", 11), width=7, height=1, borderwidth=2).grid(row=11, column=1,pady=10,padx=(5,20))

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

        if not user_name or not password or not level:
            messagebox.showerror("Validation Error", "All fields are mandatory. Please fill in all fields.")
            return
        
        if not re.match(self.username_pattern, user_name):
            messagebox.showerror("Invalid Username", "Username must start with a letter and be 5-15 characters long, containing only letters, numbers, or underscores.")
            return

        if not re.match(self.password_pattern, password):
            messagebox.showerror("Invalid Password", "Password must be 8-20 characters long, with at least one uppercase letter, one lowercase letter, one digit, and one special character.")
            return
        self.user_manager.add_user(user_name, password, level)
        self.refresh_users()
        self.clear_users()

    def update_user(self):
        selected_user = self.user_tree.focus()
        if not selected_user: 
            messagebox.showerror("Update", "No user selected.")
            return
        user_id = self.user_tree.item(selected_user, 'values')[0]
        user_name = self.entry_employee_name.get()
        password = self.entry_password.get()
        level = self.level_var.get()
        if not re.match(self.username_pattern, user_name):
            messagebox.showerror("Invalid Username", "Username must start with a letter and be 5-15 characters long, containing only letters, numbers, or underscores.")
            return
        if not re.match(self.password_pattern, password):
            messagebox.showerror("Invalid Password", "Password must be 8-20 characters long, with at least one uppercase letter, one lowercase letter, one digit, and one special character.")
            return
        self.user_manager.update_user(user_id, user_name, password, level)
        self.refresh_users()
        self.clear_users()

    def delete_user(self):
        selected_user = self.user_tree.focus()
        if not selected_user: 
            messagebox.showerror("Delete", "No user selected.")
            return
        user_id = self.user_tree.item(selected_user, 'values')[0]
        self.user_manager.delete_user(user_id)
        self.refresh_users()
        self.clear_users()

    def search_user(self):
        search_name = self.search.get()
        if not search_name:
            messagebox.showerror("Search", "Please enter a name to search.")
            return

        results = self.user_manager.search_users_by_name(search_name)

        for row in self.user_tree.get_children():
            self.user_tree.delete(row)

        if results:
            for row in results:
                self.user_tree.insert('', 'end', values=row)
        else:
            messagebox.showinfo("Search", "No users found matching the search criteria.")

    def refresh_users(self):
        for row in self.user_tree.get_children():
            self.user_tree.delete(row)
        for row in self.user_manager.get_all_users():
            self.user_tree.insert('', 'end', values=row)

    def clear_users(self):
        self.entry_employee_name.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.refresh_users()

    def on_user_select(self, event):
        selected_user = self.user_tree.focus()
        if selected_user:
            values = self.user_tree.item(selected_user, 'values')
            self.entry_employee_name.delete(0, tk.END)
            self.entry_employee_name.insert(0, values[1])
            self.entry_password.delete(0, tk.END)
            self.entry_password.insert(0, values[2])

    def add_user_back(self):
        self.add_employees_frame.pack_forget()
        self.dashboard_frame.pack(expand=True, fill="both")

if __name__ == "__main__":
    flag = 0
    root = tk.Tk()
    app = Login(root)
    root.mainloop()

