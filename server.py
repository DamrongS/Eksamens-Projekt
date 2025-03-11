import json
import uuid
import hashlib
import tkinter as tk
from tkinter import messagebox, ttk

DATABASE_FILE = "database.json"

# [[ using the json library to open our database file ]]
def load_database():
    try:
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": {}}

# [[ using the json library to save our data to the database file ]]
def save_database(db):
    with open(DATABASE_FILE, "w") as file:
        json.dump(db, file, indent=4)

# [[ using the hashlib library to hash our passwords including a salt ID ]]
def superSecretHashingAlgorithm(password, salt):
    combined = password + salt
    hashed = hashlib.sha256(combined.encode()).hexdigest()
    return hashed

# [[ using the uuid library to generate a unique userId and saltId for every user ]]
def register_user(username, surname, lastname, password):
    database = load_database()
    userId = str(uuid.uuid4())
    salt = str(uuid.uuid4())
    hashedPassword = superSecretHashingAlgorithm(password, salt)

    # Setup initial data
    database["users"][userId] = {
        "username": username,
        "surname": surname,
        "lastname": lastname,
        "password": hashedPassword,
        "salt": salt,
        "accounts": 
            {
                f"{username}'s Account": AddAcountToUser()
            },
        "transactions": [],
        "loans": []
    }

    # Save the initial data to the database
    save_database(database)
    messagebox.showinfo("Success", f"User {username} registered successfully!")
    return userId

def AddAcountToUser():
    return {
        "balance": 0
    }

# [[ logs the user in ]]
def login_user(username, password, root):
    database = load_database()
    for userId, userData in database["users"].items():
        if userData["username"] == username:
            salt = userData["salt"]
            hashedPassword = userData["password"]
            if superSecretHashingAlgorithm(password, salt) == hashedPassword:
                #messagebox.showinfo("Login Success", f"Welcome {userData['surname']} {userData['lastname']}!")
                root.destroy()
                return userId
            else:
                #messagebox.showerror("Error", "Invalid password!")
                return None
    #messagebox.showerror("Error", "Invalid username!")
    return None

# [[ logs the admin into the admin panel ]]
def login_admin(username, password, root):
    if username == "admin" and password == "1234":
        #messagebox.showinfo("Login Success", "Welcome admin!")
        root.destroy()
        admin_gui()
        return True
    else:
        messagebox.showerror("Error", "Invalid credentials!")
        return None

# [[ visualizes the selected account ]]
def visualize_account(user_id):
    database = load_database()
    user_data = database["users"].get(user_id, {})

    if not user_data:
        messagebox.showerror("Error", "User not found!")
        return

    account_window = tk.Toplevel()
    account_window.title(f"Account Details - {user_data['username']}")
    account_window.geometry("400x400")

    tk.Label(account_window, text=f"Username: {user_data['username']}").pack(pady=5)
    tk.Label(account_window, text=f"Surname: {user_data['surname']}").pack(pady=5)
    tk.Label(account_window, text=f"Lastname: {user_data['lastname']}").pack(pady=5)
    tk.Label(account_window, text=f"Accounts: {user_data['accounts']}").pack(pady=5)
    tk.Label(account_window, text=f"Transactions: {user_data['transactions']}").pack(pady=5)
    tk.Label(account_window, text=f"Loans: {user_data['loans']}").pack(pady=5)

# [[ tkinter admin gui ]]
def admin_gui():
    admin_window = tk.Toplevel()
    admin_window.title("Admin Panel")
    admin_window.geometry("1200x800")

    tk.Label(admin_window, text="All Bank Accounts", font=("Arial", 16)).pack(pady=10)

    tree = ttk.Treeview(admin_window, columns=("ID", "Username", "Surname", "Lastname"), show="headings")
    tree.heading("ID", text="User ID")
    tree.heading("Username", text="Username")
    tree.heading("Surname", text="Surname")
    tree.heading("Lastname", text="Lastname")
    tree.pack(pady=20, fill="both", expand=True)

    search_entry = tk.Entry(admin_window)
    search_entry.pack(pady=5)

    # search function
    def search():
        query = search_entry.get().lower()
        tree.delete(*tree.get_children())
        database = load_database()
        for userId, userData in database["users"].items():
            if query in userData["username"].lower() or query in userData["surname"].lower() or query in userData["lastname"].lower():
                tree.insert("", "end", values=(userId, userData["username"], userData["surname"], userData["lastname"]))

    tk.Button(admin_window, text="Search", command=search).pack(pady=5)

    # refresh function
    def refresh():
        tree.delete(*tree.get_children())
        database = load_database()
        for userId, userData in database["users"].items():
            tree.insert("", "end", values=(userId, userData["username"], userData["surname"], userData["lastname"]))

    tk.Button(admin_window, text="Refresh", command=refresh).pack(pady=5)

    # create user function
    def create_user():
        create_window = tk.Toplevel()
        create_window.title("Create User")
        create_window.geometry("400x300")

        tk.Label(create_window, text="Username:").pack(pady=5)
        username = tk.Entry(create_window)
        username.pack(pady=5)

        tk.Label(create_window, text="Surname:").pack(pady=5)
        surname = tk.Entry(create_window)
        surname.pack(pady=5)

        tk.Label(create_window, text="Lastname:").pack(pady=5)
        lastname = tk.Entry(create_window)
        lastname.pack(pady=5)

        tk.Label(create_window, text="Password:").pack(pady=5)
        password = tk.Entry(create_window, show="*")
        password.pack(pady=5)

        # submit user creation function
        def submit():
            register_user(username.get(), surname.get(), lastname.get(), password.get())
            refresh()
            create_window.destroy()

        tk.Button(create_window, text="Create", command=submit).pack(pady=10)

    tk.Button(admin_window, text="Create User", command=create_user).pack(pady=5)
    tree.bind("<Double-1>", lambda event: visualize_account(tree.item(tree.selection(), "values")[0] if tree.selection() else None))

    # delete function
    def delete_user():
        selected_item = tree.selection()
        if selected_item:
            user_id = tree.item(selected_item, "values")[0]
            database = load_database()
            del database["users"][user_id]
            save_database(database)
            refresh()
            #messagebox.showinfo("Success", "User deleted successfully!")
        else:
            messagebox.showerror("Error", "Please select a user to delete!")

    tk.Button(admin_window, text="Delete User", command=delete_user).pack(pady=5)
    refresh()

# [[ authentication gui ]]
def create_gui():
    root = tk.Tk()
    root.title("User Authentication")
    root.geometry("400x600")

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
        login_admin(username, password, root)

    tk.Button(root, text="Login", command=handle_login).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
