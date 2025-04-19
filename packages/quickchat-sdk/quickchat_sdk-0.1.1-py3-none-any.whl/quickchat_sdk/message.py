from .connection import get_connection

message_listeners = []

def onRecieve(func):
    message_listeners.append(func)

def handle_message(message):
    if message.startswith("1303"):
        for listener in message_listeners:
            index = message.find("[:pwd:]")
            message = message[index + len("[:pwd:]"):] if index != -1 else ""
            listener(message)

def send(username, message):
    conn = get_connection()
    conn.send("0202" + username)
    conn.send("0301" + message)
