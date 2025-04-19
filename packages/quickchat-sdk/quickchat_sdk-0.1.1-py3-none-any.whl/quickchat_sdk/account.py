from .connection import get_connection

def signIn(username, password):
    get_connection().send("0002" + username + "[:pwd:]" + password)
