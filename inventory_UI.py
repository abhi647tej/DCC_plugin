import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import requests
import threading

class InventoryUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management")
        self.root.geometry("500x500")

        # Table for inventory display
        self.tree = ttk.Treeview(root, columns=("Name", "Quantity"), show='headings')
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Buttons
        self.refresh_button = tk.Button(root, text="Refresh Inventory", command=self.refresh_inventory)
        self.refresh_button.pack(pady=5)
        
        self.add_button = tk.Button(root, text="Add Item", command=self.add_item)
        self.add_button.pack(pady=5)

        self.update_button = tk.Button(root, text="Update Quantity", command=self.update_quantity)
        self.update_button.pack(pady=5)

        self.remove_button = tk.Button(root, text="Remove Item", command=self.remove_item)
        self.remove_button.pack(pady=5)
        
        self.buy_button = tk.Button(root, text="Buy Item", command=self.buy_item)
        self.buy_button.pack(pady=5)
        
        self.return_button = tk.Button(root, text="Return Item", command=self.return_item)
        self.return_button.pack(pady=5)

        self.refresh_inventory()

    def threaded_request(self, func, *args):
        thread = threading.Thread(target=func, args=args)
        thread.start()

    def refresh_inventory(self):
        try:
            response = requests.get("http://127.0.0.1:5000/get-inventory")
            inventory = response.json().get("inventory", [])
            self.tree.delete(*self.tree.get_children())
            for item in inventory:
                self.tree.insert("", tk.END, values=(item['name'], item['quantity']))
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Failed to connect to server!")

    def add_item(self):
        name = simpledialog.askstring("Input", "Enter item name:")
        quantity = simpledialog.askinteger("Input", "Enter quantity:")
        if name and quantity is not None:
            self.threaded_request(self.send_request, "add-item", {"name": name, "quantity": quantity})

    def update_quantity(self):
        name = simpledialog.askstring("Input", "Enter item name to update:")
        quantity = simpledialog.askinteger("Input", "Enter new quantity:")
        if name and quantity is not None:
            self.threaded_request(self.send_request, "update-quantity", {"name": name, "quantity": quantity})

    def remove_item(self):
        name = simpledialog.askstring("Input", "Enter item name to remove:")
        if name:
            self.threaded_request(self.send_request, "remove-item", {"name": name})
    
    def buy_item(self):
        name = simpledialog.askstring("Input", "Enter item name to buy:")
        quantity = simpledialog.askinteger("Input", "Enter quantity to buy:")
        if name and quantity is not None:
            self.threaded_request(self.send_request, "update-quantity", {"name": name, "quantity": quantity})
    
    def return_item(self):
        name = simpledialog.askstring("Input", "Enter item name to return:")
        quantity = simpledialog.askinteger("Input", "Enter quantity to return:")
        if name and quantity is not None:
            self.threaded_request(self.send_request, "update-quantity", {"name": name, "quantity": -quantity})
    
    def send_request(self, endpoint, data):
        try:
            response = requests.post(f"http://127.0.0.1:5000/{endpoint}", json=data)
            if response.status_code == 200:
                self.refresh_inventory()
            else:
                messagebox.showerror("Error", f"Failed to process request: {endpoint}")
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Failed to connect to server!")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryUI(root)
    root.mainloop()
