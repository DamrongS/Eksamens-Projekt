import json
import uuid
import hashlib
import server

def login_client(username, password, root):
    root.destroy()
    if server.login_user(username, password):
        return True
    else:
        return False