def create_user(username, password):
    db["users"][username] = {
        "password": hash_password(password),
        "accounts": {}
    }
    save_db(db)

def create_account(username, account_name):
    db["users"][username]["accounts"][account_name] = {
        "saldo": 0,
        "transactions": [],
        "loans": {
            "active": False
        }
    }
    save_db(db)