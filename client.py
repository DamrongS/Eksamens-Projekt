import json
import uuid
import hashlib
import tkinter as tk
from tkinter import messagebox, ttk
import remotes

def create_gui():
    root = tk.Tk()
    root.title("User Authentication")
    root.geometry("400x300")

    tk.Label(root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password:").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    # handles login
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        remotes.login_client(username, password, root)

    tk.Button(root, text="Login", command=handle_login).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()