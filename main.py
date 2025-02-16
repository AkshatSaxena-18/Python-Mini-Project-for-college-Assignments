import tkinter as tk  # This module is used for creating GUI 
from tkinter import ttk, messagebox, Entry, Checkbutton, Button
import random   # This module takes a random element
import string   # For Password
import json     # Loading and Saving Password
import base64   # It is used for encryption and decryption

class PasswordManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Generator and Manager")
        self.master.geometry("400x500")

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.generator_frame = ttk.Frame(self.notebook)
        self.manager_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.generator_frame, text="Generator")
        self.notebook.add(self.manager_frame, text="Manager")

        self.passwords = {}  # Dictionary to store passwords
        self.setup_generator()
        self.setup_manager()
        self.load_passwords()

    def setup_generator(self):
        self.lengthVar = tk.StringVar(value="15")
        self.uppercaseVar = tk.BooleanVar(value=True)
        self.lowercaseVar = tk.BooleanVar(value=True)
        self.numbersVar = tk.BooleanVar(value=True)
        self.symbolsVar = tk.BooleanVar(value=True)
        self.passwordVar = tk.StringVar()

        ttk.Label(self.generator_frame, text="Password Length:").pack(pady=5)
        Entry(self.generator_frame, textvariable=self.lengthVar, width=5).pack()

        ttk.Checkbutton(self.generator_frame, text="Uppercase", variable=self.uppercaseVar).pack()
        ttk.Checkbutton(self.generator_frame, text="Lowercase", variable=self.lowercaseVar).pack()
        ttk.Checkbutton(self.generator_frame, text="Numbers", variable=self.numbersVar).pack()
        ttk.Checkbutton(self.generator_frame, text="Symbols", variable=self.symbolsVar).pack()

        Button(self.generator_frame, text="Generate Password", command=self.generate_password).pack(pady=10)
        Entry(self.generator_frame, textvariable=self.passwordVar, state="readonly", width=30).pack()
        Button(self.generator_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(pady=10)

    def setup_manager(self):
        self.serviceVar = tk.StringVar()
        self.usernameVar = tk.StringVar()
        self.password_man_Var = tk.StringVar()

        ttk.Label(self.manager_frame, text="Service:").pack(pady=5)
        ttk.Entry(self.manager_frame, textvariable=self.serviceVar, width=30).pack()

        ttk.Label(self.manager_frame, text="Username:").pack(pady=5)
        ttk.Entry(self.manager_frame, textvariable=self.usernameVar, width=30).pack()

        ttk.Label(self.manager_frame, text="Password:").pack(pady=5)
        ttk.Entry(self.manager_frame, textvariable=self.password_man_Var, width=30, show="*").pack()

        ttk.Button(self.manager_frame, text="Save Password", command=self.save_password).pack(pady=10)

        self.password_tree = ttk.Treeview(self.manager_frame, columns=("Service", "Username"), show="headings")
        self.password_tree.heading("Service", text="Service")
        self.password_tree.heading("Username", text="Username")
        self.password_tree.pack(pady=10)
        self.password_tree.bind("<Double-1>", self.on_tree_double_click)

    def generate_password(self):
        length = int(self.lengthVar.get())
        characters = ""

        if self.uppercaseVar.get():
            characters += string.ascii_uppercase  

        if self.lowercaseVar.get():
            characters += string.ascii_lowercase  

        if self.numbersVar.get():
            characters += string.digits  

        if self.symbolsVar.get():
            characters += string.punctuation

        if not characters:
            self.passwordVar.set("Please select at least one character type")
        else:
            password = ''.join(random.choice(characters) for _ in range(length))
            self.passwordVar.set(password)

    def copy_to_clipboard(self):
        self.master.clipboard_clear()    
        self.master.clipboard_append(self.passwordVar.get())
        self.master.update()

    def save_password(self):
        service = self.serviceVar.get()
        username = self.usernameVar.get()
        password = self.password_man_Var.get()

        if service and username and password:
            encrypted_password = self.encrypt(password)
            self.passwords[service] = {"username": username, "password": encrypted_password}
            self.save_passwords_to_file()
            self.update_password_tree()
            messagebox.showinfo("Success", "Password saved successfully!")
            self.serviceVar.set("")
            self.usernameVar.set("")
            self.password_man_Var.set("")
        else:
            messagebox.showerror("Error", "All fields are required")

    def load_passwords(self):
        try:
            with open("passwords.json", "r") as f:
                self.passwords = json.load(f)
            self.update_password_tree()
        except FileNotFoundError:
            self.passwords = {}

    def save_passwords_to_file(self):
        with open("passwords.json", "w") as f:
            json.dump(self.passwords, f)

    def update_password_tree(self):
        for item in self.password_tree.get_children():
            self.password_tree.delete(item)

        for service, data in self.passwords.items():
            self.password_tree.insert("", "end", values=(service, data["username"]))

    def on_tree_double_click(self, event):
        item = self.password_tree.selection()
        if item:
            selected_item = item[0]
            service = self.password_tree.item(selected_item, "values")[0]
            username = self.passwords[service]["username"]
            encrypted_password = self.passwords[service]["password"]
            password = self.decrypt(encrypted_password)
            messagebox.showinfo("Password", f"Service: {service}\nUsername: {username}\nPassword: {password}")

    def encrypt(self, password):
        return base64.b64encode(password.encode()).decode()

    def decrypt(self, encrypted_password):
        return base64.b64decode(encrypted_password.encode()).decode()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
