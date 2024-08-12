import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db import Database
from manager import UserManager, InventoryManager
from fpdf import FPDF, XPos, YPos

class InventoryApp:
    def __init__(self, root):
        self.db = Database()
        self.user_manager = UserManager(self.db)
        self.inventory_manager = InventoryManager(self.db)
        self.root = root
        self.root.state("zoomed")
        self.root.title("Inventory Management System")
        root.configure(background='#347083')
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview",background= "#d3d3d3", foreground = "black", rowheight= 25, fieldbackground="d3d3d3")
        self.style.map("Treeview",background=[("selected","#347083")])
        self.user_role = None
        self.create_login_window()

    def create_login_window(self):

        self.login_frame = tk.Frame(self.root,bg="#347083")
        self.login_frame.pack(pady=20)
        
        tk.Label(self.login_frame, text="LOGIN",fg="#FFFFFF",bg="#347083",font=("Arial",30)).pack(pady=10)

        tk.Label(self.login_frame, text="Username",font=("Arial"),fg="#FFFFFF",bg="#347083").pack(pady=10)
        self.entry_username = tk.Entry(self.login_frame,width=20)
        self.entry_username.pack()

        tk.Label(self.login_frame, text="Password",font=("Arial"),fg="#FFFFFF",bg="#347083").pack(pady=10)
        self.entry_password = tk.Entry(self.login_frame, show='●',width=20)
        self.entry_password.pack()

        tk.Button(self.login_frame, text="Login", command=self.login,fg="#006CA5",bg="#FFFFFF").pack(pady=20)
        self.root.bind('<Return>', self.login)

    def login(self, event=None):
        username = self.entry_username.get()
        password = self.entry_password.get()
        user = self.user_manager.validate_user(username, password)
        if user:
            self.create_inventory_window()
        else:
            messagebox.showerror("Login", "Invalid username or password.")
        
    def create_inventory_window(self):
        self.login_frame.destroy()
        self.inventory_frame = tk.Frame(self.root,bg="#347083")
        self.inventory_frame.pack(pady=10)

        tk.Label(self.inventory_frame, text="INVENTORY MANAGEMENT", font=("Arial",20,"bold"),bg="#347083",fg="#FFFFFF").grid(row=0,columnspan=8,pady=5)

        tk.Label(self.inventory_frame, text="Name",bg="#347083",fg="#FFFFFF").grid(row=1, column=0)
        self.entry_item_name = tk.Entry(self.inventory_frame)
        self.entry_item_name.grid(row=1, column=1)

        tk.Label(self.inventory_frame, text="Quantity",bg="#347083",fg="#FFFFFF").grid(row=1, column=2)
        self.entry_quantity = tk.Entry(self.inventory_frame)
        self.entry_quantity.grid(row=1, column=3)

        tk.Label(self.inventory_frame, text="Price",bg="#347083",fg="#FFFFFF").grid(row=1, column=4)
        self.entry_price = tk.Entry(self.inventory_frame)
        self.entry_price.grid(row=1, column=5)

        tk.Button(self.inventory_frame, text="Add", command=self.add_item).grid(row=3, column=2, pady=10)
        tk.Button(self.inventory_frame, text="Update", command=self.update_item).grid(row=3, column=3, pady=10)
        tk.Button(self.inventory_frame, text="Delete", command=self.delete_item).grid(row=3, column=4, pady=10)
        tk.Button(self.inventory_frame, text="Clear", command=self.clear_entries).grid(row=3, column=5, pady=10)
        tk.Button(self.inventory_frame, text="Logout", command=self.logout).grid(row=0, column=7, pady=5, padx=10)

    
        
        self.tree = ttk.Treeview(self.root, columns=('ID', 'Name', 'Quantity', 'Price'), show='headings',height=40)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Quantity', text='Quantity')
        self.tree.heading('Price', text='Price')
        self.tree.column('ID', width=70, anchor='center')
        self.tree.column('Name', width=170)
        self.tree.column('Quantity', width=170, anchor='center')
        self.tree.column('Price', width=170, anchor='center')
        self.tree.pack(pady=50)
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        self.refresh_inventory()

    def on_item_select(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.entry_item_name.delete(0, tk.END)
            self.entry_item_name.insert(0, values[1])
            self.entry_quantity.delete(0, tk.END)
            self.entry_quantity.insert(0, values[2])
            self.entry_price.delete(0, tk.END)
            self.entry_price.insert(0, values[3])

    def add_item(self):
        name = self.entry_item_name.get()
        quantity = int(self.entry_quantity.get())
        price = float(self.entry_price.get())
        self.inventory_manager.add_item(name, quantity, price)
        self.refresh_inventory()
        self.clear_entries()

    def update_item(self):
        selected_item = self.tree.focus()
        item_id = self.tree.item(selected_item, 'values')[0]
        name = self.entry_item_name.get()
        quantity = int(self.entry_quantity.get())
        price = float(self.entry_price.get())
        self.inventory_manager.update_item(item_id, name, quantity, price)
        self.refresh_inventory()
        self.clear_entries()

    def delete_item(self):
        selected_item = self.tree.focus()
        item_id = self.tree.item(selected_item, 'values')[0]
        self.inventory_manager.delete_item(item_id)
        self.refresh_inventory()
        self.clear_entries()

    def refresh_inventory(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.inventory_manager.get_all_items():
            self.tree.insert('', 'end', values=row)

    def clear_entries(self):
        self.entry_item_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)

    def logout(self):

        self.root.destroy()
        root = tk.Tk()
        app = InventoryApp(root)
        root.mainloop()



if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

