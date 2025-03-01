import json
import uuid
import hashlib
import tkinter as tk
from tkinter import messagebox

DATABASE_FILE = "database.json"

def load_database():
    try:
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": {}}
    
def save_database(db):
    with open(DATABASE_FILE, "w") as file:
        json.dump(db, file, indent=4)

def superSecretHashingAlgorithm(password, salt):
    combined = password + salt
    hashed = hashlib.sha256(combined.encode()).hexdigest()
    return hashed

def register_user(username, surname, lastname, password):
    database = load_database()
    print("Database:", database)

    userId = str(uuid.uuid4())
    salt = str(uuid.uuid4())
    hashedPassword = superSecretHashingAlgorithm(password, salt)

    database["users"][userId] = {
        "username": username,
        "surname": surname,
        "lastname": lastname,
        "password": hashedPassword,
        "salt": salt,
        "account": {},
        "transaction": [],
        "loans": []
    }
    save_database(database)
    messagebox.showinfo("Success", f"User {username} registered successfully!")
    return userId

def login_user(username, password):
    database = load_database()
    for userId, userData in database["users"].items():
        if userData["username"] == username:
            salt = userData["salt"]
            hashedPassword = userData["password"]
            if superSecretHashingAlgorithm(password, salt) == hashedPassword:
                messagebox.showinfo("Login Success", f"Welcome {userData['surname']} {userData['lastname']}!")
                return userId
            else:
                messagebox.showerror("Error", "Invalid password!")
                return None
    messagebox.showerror("Error", "Invalid username!")
    return None

def login_admin(username, password):
    if username == "admin":
        if password == "1234":
            messagebox.showinfo("Login Success", f"Welcome admin!")
            return True
        else:
            messagebox.showerror("Error", "Invalid password!")
            return None
    messagebox.showerror("Error", "Invalid username!")
    return None

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

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        login_admin(username, password)

    tk.Button(root, text="Login", command=handle_login).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
