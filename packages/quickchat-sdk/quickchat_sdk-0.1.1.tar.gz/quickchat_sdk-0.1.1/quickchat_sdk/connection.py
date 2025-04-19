import uuid
import requests
import websocket
import threading
import time

ws_connection = None
ws_ready = threading.Event()

def connect(connectionID=None):
    if connectionID == None:
        connectionID = str(uuid.uuid4())
        
    def run_ws():
        global ws_connection

        url = 'https://raw.githubusercontent.com/QC1159/Websocket/refs/heads/main/websocketURL.js'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch WebSocket URL: {response.status_code}")

        websocket_url = 'wss://' + response.text.strip()

        print(f"Connecting to {websocket_url}")

        from .message import handle_message  # defer to avoid circular import

        def on_message(ws, message):
            handle_message(message)

        def on_error(ws, error):
            print(f"Error: {error}")

        def on_close(ws, close_status_code, close_reason):
            print("Connection closed")

        def on_open(ws):
            print("Connection established")
            ws.send("3001" + connectionID)

        ws_connection = websocket.WebSocketApp(
            websocket_url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws_connection.on_open = on_open

        ws_ready.set()
        ws_connection.run_forever()

    thread = threading.Thread(target=run_ws, daemon=True)
    thread.start()

    ws_ready.wait()
    time.sleep(1)
    print("WebSocket is initialized and running in the background.")
    return connectionID

def disconnect():
    global ws_connection

    if ws_connection:
        print("Disconnecting WebSocket...")
        ws_connection.close()
        ws_connection = None
        ws_ready.clear()
    else:
        print("WebSocket is not connected.")

def get_connection():
    return ws_connection
