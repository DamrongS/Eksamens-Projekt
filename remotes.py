import json
import uuid
import hashlib
import server

def login_client(username, password, root):
    print(server.login_user(username, password))
    if server.login_user(username, password):
        root.destroy()
        return True
    else:
        return False