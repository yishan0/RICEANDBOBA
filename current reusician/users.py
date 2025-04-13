#users dictionary
users = {
    "testuser": "testpass"
}

def append_user(username, password):
    users[username] = password

def get_user(username):
    return users.get(username)