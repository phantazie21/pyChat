import socket
import rsa
import threading

users = []

#Summary: Sending a message for a client
def broadcast(_client, room, msg):
    for client in users:
        if client[0] != _client and client[1] == room:
            client[0].send(msg.encode())

#Summary: Handle a single client's messages
def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            print(msg.decode())
            room = msg.decode().split(":")[0]
            broadcast(client, room, msg.decode().lstrip(f"{room}:"))
        except Exception as e:
            print(e)

#Summary: Main function that runs continously
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 1337))
    while True:
        try:
            server.listen()
            client, _ = server.accept()
            client.send("__room__".encode())
            room = client.recv(1024).decode()
            users.append([client, room])
            threading.Thread(target=handle, args=(client,)).start()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()