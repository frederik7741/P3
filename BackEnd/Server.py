import socket
import threading
import time

# Global counter
counter = 0

def client_handler(connection):
    global counter
    while True:
        try:
            # Increment the counter
            counter += 1
            # Send the counter value as a string, followed by a newline character
            connection.sendall(f"{counter}\n".encode('utf-8'))
            # Wait a bit before sending the next value
            time.sleep(1)
        except:
            break  # Exit the loop if sending failed (e.g., client disconnected)
    connection.close()

def start_server(host='127.0.0.1', port=6789):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server listening on {host}:{port}")

    while True:
        connection, address = server_socket.accept()
        print(f"Connected to {address}")
        client_thread = threading.Thread(target=client_handler, args=(connection,))
        client_thread.start()

if __name__ == '__main__':
    start_server()
