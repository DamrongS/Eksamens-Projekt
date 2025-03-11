import json
import uuid
import hashlib
import server

def login_client(username, password, root):
    print(server.login_user(username, password, root))
    return server.login_user(username, password, root)